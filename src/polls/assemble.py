"""Turn parser rows into the output tables: column order, types, stable ids, final-list flag."""
from __future__ import annotations

import pandas as pd

from .candidates import OTHERS
from .textparse import slug

POLL_COLUMNS = [
    "election", "source", "poll_id", "scenario_id", "scenario_label",
    "institute", "institute_family", "institute_raw", "sponsor",
    "fieldwork_start", "fieldwork_end", "publication_date", "reported_date", "date_raw",
    "sample_size", "effective_base", "population_base", "mode", "panel", "rolling",
    "candidate_raw", "candidate", "candidate_column",
    "share", "share_status", "share_upper_bound", "final_list_scenario",
    "upstream_source_url", "notice_url", "wiki_revision_id", "table_label", "source_poll_ref",
]
RESULT_COLUMNS = ["election", "party", "candidate_raw", "candidate", "share", "source", "commit_hash"]
SOURCE_CODE = {"wikipedia": "wp", "france_politique": "fp", "nsppolls": "nsp"}
SHARE_STATUSES = {"value", "not_tested", "grouped_others", "below_threshold", "missing"}


def to_frame(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    for c in ("fieldwork_start", "fieldwork_end", "publication_date", "reported_date"):
        df[c] = pd.to_datetime(df[c]).dt.date
    df["sample_size"] = pd.array(df["sample_size"], dtype="Int64")
    df["wiki_revision_id"] = pd.array(df["wiki_revision_id"], dtype="Int64")
    for c in ("panel", "rolling"):
        df[c] = pd.array(df[c], dtype="boolean")
    for c in ("effective_base", "share", "share_upper_bound"):
        df[c] = pd.to_numeric(df[c])
    bad = set(df["share_status"]) - SHARE_STATUSES
    if bad:
        raise ValueError(f"unknown share_status values {bad}")
    return df


def assign_ids(df: pd.DataFrame) -> pd.DataFrame:
    """poll_id = <election>_<source>_<institute as written in the source>_<date>_<n>, where <date> is fieldwork_end,
    else the single reported date, and n counts polls sharing the rest of the id in the
    order they appear in the source. Deterministic for a pinned source."""
    polls = df.drop_duplicates(["election", "page_poll_no"], keep="first")[
        ["election", "source", "page_poll_no", "institute", "fieldwork_end", "reported_date"]].copy()
    when = polls["fieldwork_end"].where(polls["fieldwork_end"].notna(), polls["reported_date"])
    polls["stem"] = (polls["election"].astype(str) + "_" + polls["source"].map(SOURCE_CODE) + "_"
                     + polls["institute"].map(slug) + "_"
                     + when.map(lambda d: d.isoformat() if pd.notna(d) else "nodate"))
    polls["n"] = polls.groupby("stem").cumcount() + 1
    polls["poll_id"] = polls["stem"] + "_" + polls["n"].astype(str)
    out = df.merge(polls[["election", "page_poll_no", "poll_id"]], on=["election", "page_poll_no"], how="left")
    out["scenario_id"] = out["poll_id"] + "_s" + out["scenario_no"].astype(str)
    assert out["poll_id"].notna().all()
    return out


def flag_final_list(df: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    """True when the scenario's tested candidates are exactly the official first-round list.
    A candidate counts as tested unless marked not_tested; the 'others' aggregate is ignored."""
    official = results.groupby("election")["candidate"].apply(frozenset).to_dict()
    tested = df[(df["share_status"] != "not_tested") & (df["candidate"] != OTHERS)]
    sets = tested.groupby(["election", "scenario_id"])["candidate"].apply(frozenset)
    flag = {k: v == official.get(k[0]) for k, v in sets.items()}
    out = df.copy()
    out["final_list_scenario"] = [flag.get((e, s), False) for e, s in zip(out["election"], out["scenario_id"])]
    return out


def finalise(df: pd.DataFrame) -> pd.DataFrame:
    return df[POLL_COLUMNS].sort_values(
        ["election", "poll_id", "scenario_id", "candidate"], na_position="last").reset_index(drop=True)
