"""Candidate-name normalisation through the hand-editable config/candidates.csv.

The file maps (election, candidate_raw) -> candidate. It is regenerated on every run:
rows already present keep their `candidate` (hand edits win), new raw names are added
and prefilled where the match is unambiguous, and the `match` column says how a row
was filled ("results", "exact", "hint", "initial+surname", "surname", "rule";
"manual" for hand edits, blank when unfilled).
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from .textparse import strip_accents

OTHERS = "__others__"
COLUMNS = ["election", "candidate_raw", "candidate", "match", "sources"]


def _key(name: str) -> str:
    return re.sub(r"[^a-z]+", " ", strip_accents(name).lower()).strip()


def _base(raw: str) -> str:
    """'Arthaud (LO)' -> 'Arthaud'; 'Noël Mamère*' -> 'Noël Mamère*' (kept: the asterisk matters)."""
    return re.sub(r"\s*\([^)]*\)\s*$", "", raw).strip()


def _hint_fits(raw: str, hint) -> bool:
    """A header link title is a usable full name only if it ends with the label's name
    ('Arthaud (LO)' / 'Nathalie Arthaud'); not for 'Candidat LR' / 'Les Républicains'."""
    return isinstance(hint, str) and (_key(hint) + " ").endswith(" " + _key(_base(raw)) + " ")


def _canonical_pool(results: pd.DataFrame, polls: pd.DataFrame) -> tuple[dict, dict]:
    """Full names known per election, and across all elections, keyed by _key.
    Preference for spelling: results file, then Wikipedia header links, then raw full names."""
    per_election: dict[int, dict[str, str]] = {}
    overall: dict[str, str] = {}

    def add(election, name):
        if not name or len(name.split()) < 2 or name.startswith("[") or "." in name or name.startswith("Candidat"):
            return                                         # not a full name: 'J-M. Le Pen', 'Candidat LR'

        name = re.sub(r"\s*\([^)]*\)$", "", name).strip()
        k = _key(name)
        per_election.setdefault(int(election), {}).setdefault(k, name)
        overall.setdefault(k, name)

    for r in results.itertuples():
        add(r.election, r.candidate_raw)
    if "name_hint" in polls:
        hints = polls[["election", "candidate_raw", "name_hint"]].dropna().drop_duplicates()
        for e, raw, h in hints.itertuples(index=False):
            if _hint_fits(raw, h):
                add(e, h)
    for e, raw in polls[["election", "candidate_raw"]].drop_duplicates().itertuples(index=False):
        add(e, _base(raw))

    def drop_surnames(pool):
        # 'le pen' or 'dupont aignan' are surnames when a longer name ends with them
        return {k: v for k, v in pool.items() if not any(o != k and o.endswith(" " + k) for o in pool)}
    return {e: drop_surnames(p) for e, p in per_election.items()}, drop_surnames(overall)


def _surname_match(base: str, pool: dict[str, str]) -> tuple[str | None, str]:
    """'Arthaud' -> 'Nathalie Arthaud'; 'M. Le Pen' / 'J-M. Le Pen' -> by first initial."""
    m = re.fullmatch(r"((?:[A-ZÉ]\.?-?)+)\.?\s+(.+)", base)
    initial, surname = (m.group(1)[0], m.group(2)) if m else (None, base)
    sk = _key(surname)
    hits = [full for k, full in pool.items() if k.endswith(" " + sk)]
    if initial:
        hits = [h for h in hits if strip_accents(h)[0].upper() == strip_accents(initial).upper()]
    hits = sorted(set(hits))
    if len(hits) == 1:
        return hits[0], "initial+surname" if initial else "surname"
    return None, ""


def suggest(raw: str, election: int, hint: str | None, per_election: dict, overall: dict,
            official: set[str]) -> tuple[str | None, str]:
    if raw.strip().lower() == "autres":
        return OTHERS, "rule"
    base = _base(raw)
    if base.endswith("*") or base.startswith("Candidat"):
        return None, ""                                    # footnoted or generic label: decide by hand
    pool = per_election.get(election, {})
    k = _key(base)
    if k in pool:
        name = pool[k]
        return name, "results" if name in official else "exact"
    if _hint_fits(raw, hint) and (hk := _key(_base(hint))) in pool:
        return pool[hk], "hint"
    for p in (pool, overall):
        name, how = _surname_match(base, p)
        if name:
            return name, how
    return None, ""


def update_mapping(path: Path, polls: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    """Add any new (election, candidate_raw) to the mapping file, prefilled where obvious."""
    if path.exists():
        current = pd.read_csv(path, dtype=str, keep_default_na=False)
        current["election"] = current["election"].astype(int)
    else:
        current = pd.DataFrame(columns=COLUMNS)
    per_election, overall = _canonical_pool(results, polls)
    official = set(results["candidate_raw"])

    allraw = pd.concat([
        polls[["election", "source", "candidate_raw"] + (["name_hint"] if "name_hint" in polls else [])],
        results[["election", "source", "candidate_raw"]],
    ])
    if "name_hint" not in allraw:
        allraw["name_hint"] = None
    grouped = allraw.groupby(["election", "candidate_raw"], dropna=False).agg(
        sources=("source", lambda s: ";".join(sorted(set(s)))),
        hint=("name_hint", lambda s: next((x for x in s if isinstance(x, str)), None)),
    ).reset_index()

    known = {(int(r.election), r.candidate_raw): r for r in current.itertuples()}
    out = []
    for g in grouped.itertuples():
        old = known.get((int(g.election), g.candidate_raw))
        if old is not None and old.candidate:
            match = old.match or "manual"
            out.append(dict(election=g.election, candidate_raw=g.candidate_raw, candidate=old.candidate,
                            match=match, sources=g.sources))
            continue
        name, how = suggest(g.candidate_raw, int(g.election), g.hint, per_election, overall, official)
        out.append(dict(election=g.election, candidate_raw=g.candidate_raw, candidate=name or "",
                        match=how, sources=g.sources))
    # keep hand-entered rows whose raw name no longer occurs, so edits are never lost
    seen = {(int(r["election"]), r["candidate_raw"]) for r in out}
    for (e, raw), r in known.items():
        if (e, raw) not in seen:
            out.append(dict(election=e, candidate_raw=raw, candidate=r.candidate, match=r.match, sources=""))
    df = pd.DataFrame(out, columns=COLUMNS).sort_values(["election", "candidate_raw"]).reset_index(drop=True)
    df.to_csv(path, index=False)
    return df


def apply_mapping(df: pd.DataFrame, mapping: pd.DataFrame) -> pd.DataFrame:
    m = mapping[mapping["candidate"] != ""][["election", "candidate_raw", "candidate"]]
    out = df.drop(columns=["candidate"], errors="ignore").merge(m, on=["election", "candidate_raw"], how="left")
    assert len(out) == len(df)
    return out


def unmapped(mapping: pd.DataFrame) -> pd.DataFrame:
    return mapping[mapping["candidate"] == ""]
