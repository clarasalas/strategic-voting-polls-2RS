"""Official first-round results from strategic-voting-abm-2RS data/FR-electoral_data.csv.

The file has one row per candidate and both poll and result columns; only the
first-round result column is kept. Shares are converted from fractions to percent,
the unit the poll tables use.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .textparse import parse_number

REQUIRED = {"election_year", "party", "candidate", "electoral_share_R1"}


def parse_file(path: Path, commit: str) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str)
    df.columns = df.columns.str.strip()
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"results file lacks columns {sorted(missing)}; found {list(df.columns)}")
    if df.duplicated(["election_year", "party"]).any():
        raise ValueError("results file has duplicate (election_year, party) rows")
    out = pd.DataFrame({
        "election": df["election_year"].astype(int),
        "party": df["party"].str.strip(),
        "candidate_raw": df["candidate"].str.strip(),
        "share": df["electoral_share_R1"].map(lambda s: parse_number(s) * 100).round(4),
        "source": "results",
        "commit_hash": commit,
    })
    return out
