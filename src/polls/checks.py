"""Consistency checks on the parsed tables. They report; they never modify or drop rows."""
from __future__ import annotations

from datetime import date

import pandas as pd

from .candidates import OTHERS

FIRST_ROUND = {2002: date(2002, 4, 21), 2007: date(2007, 4, 22), 2012: date(2012, 4, 22),
               2017: date(2017, 4, 23), 2022: date(2022, 4, 10)}
PREVIOUS_FIRST_ROUND = {2002: date(1995, 4, 23), 2007: date(2002, 4, 21), 2012: date(2007, 4, 22),
                        2017: date(2012, 4, 22), 2022: date(2017, 4, 23)}
SUM_RANGE = (98.0, 102.0)
SAMPLE_RANGE = (300, 30_000)


def share_sums(df: pd.DataFrame) -> pd.DataFrame:
    """Sum of numeric shares per poll x scenario, with counts of cells that carry no number."""
    g = df.groupby(["election", "source", "poll_id", "scenario_id"])
    out = pd.DataFrame({
        "institute": g["institute"].first(),
        "sum_shares": g["share"].sum(min_count=1),
        "n_values": g["share_status"].apply(lambda s: (s == "value").sum()),
        "n_below_threshold": g["share_status"].apply(lambda s: (s == "below_threshold").sum()),
        "n_grouped_others": g["share_status"].apply(lambda s: (s == "grouped_others").sum()),
        "n_missing": g["share_status"].apply(lambda s: (s == "missing").sum()),
        "has_others_row": g["candidate"].apply(lambda s: (s == OTHERS).any()),
    }).reset_index()
    lo, hi = SUM_RANGE
    out["flag"] = ~out["sum_shares"].between(lo, hi)
    return out


def date_checks(df: pd.DataFrame) -> pd.DataFrame:
    """One row per poll with any date problem."""
    p = df.drop_duplicates("poll_id")[["election", "source", "poll_id", "institute", "date_raw",
                                       "fieldwork_start", "fieldwork_end", "reported_date"]].copy()
    problems = []
    for r in p.itertuples():
        dates = [d for d in (r.fieldwork_start, r.fieldwork_end, r.reported_date) if pd.notna(d)]
        issue = []
        if not dates:
            issue.append("no parsed date")
        if pd.notna(r.fieldwork_start) and pd.notna(r.fieldwork_end) and r.fieldwork_start > r.fieldwork_end:
            issue.append("start after end")
        lo, hi = PREVIOUS_FIRST_ROUND[r.election], FIRST_ROUND[r.election]
        if any(not (lo < d <= hi) for d in dates):
            issue.append(f"outside ({lo}, {hi}]")
        if issue:
            problems.append({**r._asdict(), "issue": "; ".join(issue)})
    return pd.DataFrame(problems).drop(columns="Index", errors="ignore")


def sample_checks(df: pd.DataFrame) -> pd.DataFrame:
    p = df.drop_duplicates("poll_id")[["election", "source", "poll_id", "institute", "sample_size", "effective_base"]]
    lo, hi = SAMPLE_RANGE
    n = p["sample_size"]
    flagged = p[n.notna() & ~n.between(lo, hi)].copy()
    flagged["issue"] = f"sample_size outside [{lo}, {hi}]"
    eb = p[p["effective_base"].notna() & p["sample_size"].notna() & (p["effective_base"] > p["sample_size"])].copy()
    eb["issue"] = "effective_base > sample_size"
    return pd.concat([flagged, eb], ignore_index=True)


def poll_counts(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    polls = df.drop_duplicates("poll_id")
    by_election = polls.groupby(["election", "source"]).size().unstack(fill_value=0)
    by_institute = polls.groupby(["election", "source", "institute"]).size().rename("polls").reset_index()
    return by_election, by_institute
