"""Pollster-name normalisation through the hand-editable config/institutes.csv.

Columns: institute_raw (as written in the source), institute (normalised name of the
pollster at the time), institute_family (the company across renamings, e.g. Sofres ->
TNS Sofres -> Kantar), match, sources.

As with candidates.csv, rows already filled are never overwritten. New raw names are
prefilled when they differ from an existing name only by case, spacing or punctuation
('IFOP', 'Ifop'); the rest must be filled by hand.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from .textparse import strip_accents

COLUMNS = ["institute_raw", "institute", "institute_family", "match", "sources"]


def _key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", strip_accents(name).lower())


def update_mapping(path: Path, polls: pd.DataFrame) -> pd.DataFrame:
    if path.exists():
        current = pd.read_csv(path, dtype=str, keep_default_na=False)
    else:
        current = pd.DataFrame(columns=COLUMNS)
    seen = (polls.drop_duplicates(["source", "page_poll_no", "institute"])
            .groupby("institute")["source"].agg(lambda s: ";".join(sorted(set(s)))))
    known = {r.institute_raw: r for r in current.itertuples()}
    by_key = {}
    for r in current.itertuples():
        if r.institute:
            by_key.setdefault(_key(r.institute_raw), r)
            by_key.setdefault(_key(r.institute), r)

    out = []
    for raw, sources in seen.items():
        old = known.get(raw)
        if old is not None and old.institute:
            out.append(dict(institute_raw=raw, institute=old.institute, institute_family=old.institute_family,
                            match=old.match or "manual", sources=sources))
            continue
        hit = by_key.get(_key(raw))
        if hit is not None:
            out.append(dict(institute_raw=raw, institute=hit.institute, institute_family=hit.institute_family,
                            match="spelling", sources=sources))
        else:
            out.append(dict(institute_raw=raw, institute="", institute_family="", match="", sources=sources))
    for raw, r in known.items():
        if raw not in seen.index:
            out.append(dict(institute_raw=raw, institute=r.institute, institute_family=r.institute_family,
                            match=r.match, sources=""))
    df = pd.DataFrame(out, columns=COLUMNS).sort_values("institute_raw", key=lambda s: s.str.lower())
    df.to_csv(path, index=False)
    return df.reset_index(drop=True)


def unmapped(mapping: pd.DataFrame) -> pd.DataFrame:
    return mapping[(mapping["institute"] == "") | (mapping["institute_family"] == "")]


def apply_mapping(df: pd.DataFrame, mapping: pd.DataFrame) -> pd.DataFrame:
    """Rename the parsers' `institute` to `institute_raw` and add the normalised columns."""
    m = mapping[["institute_raw", "institute", "institute_family"]]
    out = df.rename(columns={"institute": "institute_raw"}).merge(m, on="institute_raw", how="left")
    assert len(out) == len(df)
    return out
