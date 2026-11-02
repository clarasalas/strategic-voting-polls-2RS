"""Build the final poll table from the Wikipedia polls, with the hand-filled validation applied.

Base: the Wikipedia polls of all five elections (one source for every year), restricted to
the polls kept by thinning (notebook 02). Two sets of corrections are applied:

1. Cross-check (validation/crosscheck_disagreements.csv, 2002 and 2022). Where the other
   source is right (`Fp`, `NSPPolls`), its values replace Wikipedia's for the candidates that
   disagree in that scenario; a scenario that only the other source has is added. `Wikipedia`
   and `NA` change nothing, except the candidates listed in PARTIAL (rows whose notes say the
   other source is right for one candidate too).
2. Spot check (validation/spot_check_sample.csv), one-off errors only:
   - `share:` and `not in document:` (the latter only when the document is complete);
   - `candidate:` relabels, except the Green candidate before nomination (systematic);
   - `fieldwork:` where `dates_ok` is `no`, for elections whose data has fieldwork dates
     (2002, 2017, 2022), plus DATE_FIXES.
   Not applied, by decision (README, step 3): `missing:` candidates, `sample size:`, and the
   2007 and 2012 dates (publication dates, systematically a few days after fieldwork).

Every item is logged, applied or not, with the reason.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from . import worklists
from .crosscheck import ALIASES
from .textparse import strip_accents

OTHER_SOURCE = {"Fp": "france_politique", "france-politique": "france_politique", "NSPPolls": "nsppolls"}

# Disagreements answered `Wikipedia` whose notes say the other source is right for these candidates.
PARTIAL = {
    "2022_nsp_ifop_2020-06-19_1|2022_nsp_ifop_2020-06-19_1_s3": ["Jacques Cheminade"],
    "2022_nsp_ifop_2021-04-08_1|2022_nsp_ifop_2021-04-08_1_s8": ["Jean-Christophe Lagarde"],
}

# Spot-check dates applied outside 2002/2017/2022: a poll filed under the wrong date, not a
# publication-date lag. The October 2010 row has the shares of the May 2010 poll.
DATE_FIXES = {"2012_wp_ifop_2010-10-14_1"}

# Before nomination, Wikipedia files the Green share under the eventual candidate: systematic,
# so not corrected in the few polls checked by hand (see README).
SYSTEMATIC_RELABELS = {"Noël Mamère"}

VALID_ELECTIONS_FOR_DATES = {2002, 2017, 2022}

# A scenario only the other source has is added only if it lists at least this many candidates.
# (NSPPolls splits Ifop's June 2020 Bertrand hypothesis into 12 candidates and a 1-candidate stub.)
MIN_SCENARIO_SIZE = 5

# Spot-check items not applied until confirmed by hand: (poll_id, item key) -> reason.
HELD = {
    ("2022_wp_yougov_2022-04-07_1", "fieldwork"):
        "held: the notice of 8 April gives 28-31 March, the dates of the other YouGov poll, whose shares differ",
    ("2012_wp_csa_2012-04-17_1", "not in document"):
        "held: four candidates on the official ballot absent from a poll five days before the vote",
    ("2012_wp_ifop_2011-06-23_1", "share"):
        "held: s1 would sum to 105; Chevènement's 6.5 in s1 is probably Joly's (columns swapped)",
    ("2012_wp_ifop_2011-06-23_1", "not in document"):
        "held: s1 would sum to 105; Chevènement's 6.5 in s1 is probably Joly's (columns swapped)",
}

FINAL_COLUMNS = [
    "election", "poll_id", "scenario_id", "scenario_label", "institute", "institute_family", "institute_raw",
    "sponsor", "fieldwork_start", "fieldwork_end", "reported_date", "date", "sample_size", "rolling",
    "candidate", "share", "share_status", "share_upper_bound", "final_list_scenario",
    "corrected", "checked_against", "upstream_source_url", "notice_url", "wiki_revision_id", "source_poll_ref",
]


@dataclass
class Change:
    source: str            # "cross-check" or "spot check"
    ref: str               # check_id or poll_id of the worklist row
    poll_id: str
    item: str              # what the worklist says
    applied: bool
    reason: str = ""
    scenario_id: str = ""
    candidate: str = ""
    field: str = ""
    old: str = ""
    new: str = ""


@dataclass
class Builder:
    wp: pd.DataFrame
    log: list = field(default_factory=list)

    def __post_init__(self):
        self.wp = self.wp.copy()
        self.wp["corrected"] = False

    # ---- lookups -------------------------------------------------------------------------
    def rows(self, scenario_id, candidate=None):
        m = self.wp["scenario_id"] == scenario_id
        if candidate is not None:
            m &= self.wp["candidate"] == candidate
        return self.wp.index[m]

    def find_candidate(self, poll_id: str, surname: str) -> str | None:
        """Full candidate name in this poll for a surname written in the notes ('Le Pen', 'Dupont Aignan')."""
        key = _norm(surname)
        names = self.wp.loc[self.wp["poll_id"] == poll_id, "candidate"].unique()
        hits = [n for n in names if _norm(n).endswith(key)]
        return hits[0] if len(hits) == 1 else None

    def scenarios(self, poll_id: str, prefix: str | None, candidate: str | None = None) -> list[str]:
        sc = sorted(self.wp.loc[self.wp["poll_id"] == poll_id, "scenario_id"].unique(), key=_scenario_number)
        if prefix:
            return [s for s in sc if s.endswith(f"_{prefix}")]
        if candidate:   # no prefix: every scenario where the candidate is tested, else listed
            rows = self.wp[(self.wp["poll_id"] == poll_id) & (self.wp["candidate"] == candidate)]
            tested = set(rows.loc[rows["share_status"] != "not_tested", "scenario_id"])
            return [s for s in sc if s in (tested or set(rows["scenario_id"]))]
        return sc

    # ---- edits ---------------------------------------------------------------------------
    def set_share(self, change: Change, scenario_id, candidate, share, status, bound=None):
        idx = self.rows(scenario_id, candidate)
        new = _fmt(share, status, bound)
        if len(idx):
            i = idx[0]
            change.old = _fmt(self.wp.at[i, "share"], self.wp.at[i, "share_status"], self.wp.at[i, "share_upper_bound"])
            self.wp.loc[i, ["share", "share_status", "share_upper_bound"]] = [share, status, bound]
            self.wp.at[i, "corrected"] = True
        else:   # candidate not listed in this scenario on Wikipedia: add a row
            template = self.wp.loc[self.rows(scenario_id)[0]].copy()
            template[["candidate", "candidate_raw", "candidate_column"]] = [candidate, candidate, None]
            template[["share", "share_status", "share_upper_bound", "corrected"]] = [share, status, bound, True]
            self.wp = pd.concat([self.wp, template.to_frame().T], ignore_index=True)
            change.old = "absent"
        change.scenario_id, change.candidate, change.field, change.new = scenario_id, candidate, "share", new
        change.applied = change.old != new or change.applied
        if change.old == new:
            change.applied, change.reason = False, "already this value"
        self.log.append(change)

    def add_scenario(self, change: Change, poll_id: str, other_rows: pd.DataFrame):
        template = self.wp.loc[self.wp["poll_id"] == poll_id].iloc[0]
        n = max(_scenario_number(s) for s in self.wp.loc[self.wp["poll_id"] == poll_id, "scenario_id"]) + 1
        new = []
        for r in other_rows.itertuples():
            row = template.copy()
            row[["scenario_id", "scenario_label", "candidate", "candidate_raw", "candidate_column"]] = \
                [f"{poll_id}_s{n}", r.scenario_label, r.candidate, r.candidate_raw, None]
            row[["share", "share_status", "share_upper_bound", "corrected"]] = \
                [r.share, r.share_status, r.share_upper_bound, True]
            new.append(row)
        self.wp = pd.concat([self.wp, pd.DataFrame(new)], ignore_index=True)
        change.scenario_id, change.field, change.applied = f"{poll_id}_s{n}", "scenario", True
        change.new = f"added from the other source ({len(new)} candidates)"
        self.log.append(change)

    def set_dates(self, change: Change, poll_id: str, start: str, end: str):
        m = self.wp["poll_id"] == poll_id
        first = self.wp.loc[m].iloc[0]
        change.old = f"{_d(first.fieldwork_start)} to {_d(first.fieldwork_end)} (reported {_d(first.reported_date)})"
        self.wp.loc[m, ["fieldwork_start", "fieldwork_end"]] = [start, end]
        self.wp.loc[m, "corrected"] = True
        change.field, change.new, change.applied = "fieldwork", f"{start} to {end}", True
        self.log.append(change)

    def rename(self, change: Change, scenario_id: str, old: str, new: str):
        idx = self.rows(scenario_id, old)
        if len(self.rows(scenario_id, new)):
            change.applied, change.reason = False, f"{new} is already listed in this scenario"
        else:
            self.wp.loc[idx, ["candidate", "corrected"]] = [new, True]
            change.applied = True
        change.scenario_id, change.field, change.old, change.new = scenario_id, "candidate", old, new
        self.log.append(change)


# ---- cross-check ---------------------------------------------------------------------------
def apply_crosscheck(b: Builder, disagreements: pd.DataFrame, shares: dict[int, pd.DataFrame],
                     others: dict[str, pd.DataFrame]) -> None:
    for r in disagreements.itertuples():
        election = int(r.election)
        answer = r.correct_source.strip()
        wiki_poll = r.poll_id_wikipedia
        scenario_a = r.check_id.split("|", 1)[1]
        s = shares[election]
        pair = s[s["scenario_a"] == scenario_a]
        other = others[OTHER_SOURCE.get(answer, "nsppolls" if election == 2022 else "france_politique")]
        base = dict(source="cross-check", ref=r.check_id, poll_id=wiki_poll, applied=False)

        if answer in OTHER_SOURCE:
            todo = None   # every disagreeing candidate
        elif r.check_id in PARTIAL:
            todo = PARTIAL[r.check_id]
        else:
            b.log.append(Change(**base, item=f"correct source: {answer or 'blank'}",
                                reason="Wikipedia kept" if answer == "Wikipedia" else "no document: Wikipedia kept"))
            continue

        if (pair["verdict"] == "scenario only in a").all():
            ch = Change(**base, item=f"correct source: {answer}; scenario only in the other source")
            rows = other[other["scenario_id"] == scenario_a]
            if len(rows) < MIN_SCENARIO_SIZE:   # a fragment of another scenario, not a scenario
                ch.reason = f"not added: the other source's scenario has only {len(rows)} candidate(s)"
                b.log.append(ch)
            else:
                b.add_scenario(ch, wiki_poll, rows)
            continue
        scenario_b = pair["scenario_b"].dropna().iloc[0]
        a_rows = other[other["scenario_id"] == scenario_a]
        for d in pair[pair["verdict"].isin(["differ", "status differs", "candidate only in a", "candidate only in b"])].itertuples():
            wiki_names = [c for c in b.wp.loc[b.rows(scenario_b), "candidate"] if ALIASES.get(c, c) == d.candidate]
            a_match = a_rows[a_rows["candidate"].map(lambda c: ALIASES.get(c, c)) == d.candidate]
            name = wiki_names[0] if wiki_names else (a_match["candidate"].iloc[0] if len(a_match) else d.candidate)
            if todo is not None and name not in todo:
                continue
            ch = Change(**base, item=f"correct source: {answer}" + (" (from notes)" if todo else "")
                        + f"; {d.candidate}: {_fmt(d.share_a, d.status_a)} vs {_fmt(d.share_b, d.status_b)}")
            if d.status_a in ("absent", "not_tested") or not len(a_match):
                b.set_share(ch, scenario_b, name, None, "not_tested")
            else:
                a = a_match.iloc[0]
                b.set_share(ch, scenario_b, name, a.share, a.share_status,
                            a.share_upper_bound if a.share_status == "below_threshold" else None)


# ---- spot check ----------------------------------------------------------------------------
ITEM = re.compile(r"^(?:(s\d+) )?(fieldwork|published|sample size|share|missing|not in document|candidate|document|other): (.*)$")


def parse_notes(notes: str) -> list[tuple[str | None, str, str]]:
    out = []
    for part in [p.strip() for p in notes.split("; ") if p.strip()]:
        m = ITEM.match(part)
        if not m:
            raise ValueError(f"note item not in the standard format: {part!r}")
        out.append(m.groups())
    return out


def _share_value(text: str):
    """'23' -> (23.0, 'value', None); '<0.5' -> (None, 'below_threshold', 0.5)."""
    text = text.strip()
    if text.startswith("<"):
        return None, "below_threshold", float(text[1:])
    return float(text), "value", None


def apply_spot_check(b: Builder, spot: pd.DataFrame) -> None:
    for r in spot.itertuples():
        items = parse_notes(r.notes)
        partial_doc = any(k == "document" for _, k, _ in items)
        election = int(r.election)
        for prefix, key, value in items:
            base = dict(source="spot check", ref=r.poll_id, poll_id=r.poll_id,
                        item=f"{prefix + ' ' if prefix else ''}{key}: {value}", applied=False)
            if (r.poll_id, key) in HELD:
                b.log.append(Change(**base, reason=HELD[(r.poll_id, key)]))
                continue
            if key == "share":
                for entry in [e.strip() for e in value.split(", ")]:
                    surname, val = entry.rsplit(" ", 1)
                    name = b.find_candidate(r.poll_id, surname)
                    if not name:
                        b.log.append(Change(**{**base, "item": f"share: {entry}"}, reason=f"no candidate '{surname}' in the data"))
                        continue
                    share, status, bound = _share_value(val)
                    for sc in b.scenarios(r.poll_id, prefix, name):
                        b.set_share(Change(**{**base, "item": f"{prefix + ' ' if prefix else ''}share: {entry}"}),
                                    sc, name, share, status, bound)
            elif key == "not in document":
                for surname in [e.strip() for e in value.split(", ")]:
                    sub = {**base, "item": f"{prefix + ' ' if prefix else ''}not in document: {surname}"}
                    name = b.find_candidate(r.poll_id, surname)
                    if partial_doc or r.shares_ok != "no":
                        b.log.append(Change(**sub, reason="partial document: absence not conclusive"))
                    elif not name:
                        b.log.append(Change(**sub, reason=f"no candidate '{surname}' in the data"))
                    else:
                        for sc in b.scenarios(r.poll_id, prefix, name):
                            b.set_share(Change(**sub), sc, name, None, "not_tested")
            elif key == "candidate":
                old_s, new_s = [x.strip() for x in value.split("→")]
                old = b.find_candidate(r.poll_id, old_s)
                if old in SYSTEMATIC_RELABELS:
                    b.log.append(Change(**base, reason="systematic (Green candidate before nomination): not corrected"))
                    continue
                full_new = b.find_candidate(r.poll_id, new_s) or new_s
                for sc in b.scenarios(r.poll_id, prefix, old):
                    b.rename(Change(**base), sc, old, full_new)
            elif key == "fieldwork":
                if r.dates_ok != "no":
                    b.log.append(Change(**base, reason="dates_ok is not 'no': information only"))
                elif election not in VALID_ELECTIONS_FOR_DATES and r.poll_id not in DATE_FIXES:
                    b.log.append(Change(**base, reason="2007/2012 dates are publication dates: kept (decision)"))
                else:
                    start, _, end = value.partition(" to ")
                    b.set_dates(Change(**base), r.poll_id, start, end or start)
            else:
                reason = {"missing": "missing candidates are not added (decision)",
                          "sample size": "data keeps the base of respondents (decision)",
                          "published": "information only", "document": "information only",
                          "other": "information only"}[key]
                b.log.append(Change(**base, reason=reason))


# ---- assembly ------------------------------------------------------------------------------
def build(root: Path) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    interim, validation = root / "data" / "interim", root / "validation"
    wp = pd.read_csv(interim / "polls_wikipedia.csv", low_memory=False)
    others = {"france_politique": pd.read_csv(interim / "polls_france_politique.csv", low_memory=False),
              "nsppolls": pd.read_csv(interim / "polls_nsppolls.csv", low_memory=False)}
    shares = {y: pd.read_csv(interim / f"crosscheck_{y}_shares.csv") for y in (2002, 2022)}
    matches = pd.concat([pd.read_csv(interim / f"crosscheck_{y}_polls.csv") for y in (2002, 2022)])
    thinning = pd.read_csv(interim / "thinning.csv")
    disagreements = worklists.read(validation / "crosscheck_disagreements.csv")
    spot = worklists.read(validation / "spot_check_sample.csv")

    b = Builder(wp)
    apply_crosscheck(b, disagreements, shares, others)
    apply_spot_check(b, spot)
    log = pd.DataFrame([c.__dict__ for c in b.log])

    kept = set(thinning.loc[(thinning["source"] == "wikipedia") & thinning["kept"].astype(bool), "poll_id"])
    final = b.wp[b.wp["poll_id"].isin(kept)].copy()
    final["date"] = final["fieldwork_end"].fillna(final["reported_date"])
    cross = set(matches.loc[matches["status"].str.startswith("matched"), "poll_id_b"])
    spotted = set(spot["poll_id"])
    final["checked_against"] = [
        "; ".join(x for x, ok in (("other source", p in cross), ("original document", p in spotted)) if ok)
        for p in final["poll_id"]]
    final = final.sort_values(["election", "date", "institute", "poll_id", "scenario_id", "candidate"],
                              key=lambda c: c.map(_scenario_number) if c.name == "scenario_id" else c)
    final = final[FINAL_COLUMNS].reset_index(drop=True)
    final = final.astype({"share": float, "share_upper_bound": float, "corrected": bool, "election": int})
    final["sample_size"] = pd.array(pd.to_numeric(final["sample_size"]), dtype="Int64")
    return final, log, warnings(final, log)


def warnings(final: pd.DataFrame, log: pd.DataFrame) -> list[str]:
    out = []
    applied = log[log["applied"]]
    for (pid, sc, cand, fld), g in applied.groupby(["poll_id", "scenario_id", "candidate", "field"]):
        if not _compatible(set(g["new"])):
            out.append(f"conflicting corrections for {sc or pid} {cand} {fld}: {' / '.join(g['new'])} (last one kept)")
    polls = final.drop_duplicates("poll_id")
    dup = polls[polls.duplicated(["election", "institute", "fieldwork_start", "fieldwork_end"], keep=False)
                & polls["fieldwork_end"].notna()]
    for _, g in dup.groupby(["institute", "fieldwork_start", "fieldwork_end"]):
        out.append(f"same pollster and fieldwork dates: {', '.join(g['poll_id'])}")
    return out


# ---- helpers -------------------------------------------------------------------------------
def _norm(s: str) -> str:
    return re.sub(r"[^a-z]", "", strip_accents(str(s)).lower())


def _compatible(values: set) -> bool:
    """One value, or a number and a '<x' bound it satisfies ('0' and '<1')."""
    if len(values) <= 1:
        return True
    bounds = [float(v[1:]) for v in values if v.startswith("<")]
    nums = [float(v) for v in values if re.fullmatch(r"[\d.]+", v)]
    return len(bounds) + len(nums) == len(values) and len(set(nums)) <= 1 and all(n < b for n in nums for b in bounds)


def _scenario_number(s) -> int:
    return int(str(s).rsplit("_s", 1)[1])


def _fmt(share, status, bound=None) -> str:
    if status == "value":
        return f"{float(share):g}"
    if status == "below_threshold":
        return f"<{float(bound):g}" if bound == bound and bound is not None else "<threshold"
    return str(status)


def _d(x) -> str:
    return "" if pd.isna(x) else str(x)
