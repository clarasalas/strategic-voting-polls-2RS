"""Poll input for the ABM's empirical mode, in the format it reads (data/polls_{year}.csv there).

One row per poll: source, date (last fieldwork day, dd/mm/yyyy), fieldwork (start to end, ISO dates),
rolling, below_threshold, then one column per modelled party (the ABM's party codes), shares as
published / 100 with a comma decimal. The ABM groups polls by ISO week, averages and rescales.

Built from the validated final dataset: each poll's ballot scenario, its candidates mapped to the
ABM's parties through their slot (the final candidacy) and that slot's party in the results. Extra
candidates who will not be on the ballot are dropped (the ABM rescales). Below-threshold shares
are half their bound, and listed in `below_threshold`. A poll that does not test every modelled
party is dropped, as the ABM's own builder does, and reported.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# The ABM's windows (tools/build_polls_from_wikipedia.py there)
WINDOWS = {2002: ("2002-03-01", "2002-04-18"), 2022: ("2022-03-07", "2022-04-08")}


def party_order(abm_root: Path, year: int) -> list[str]:
    p = pd.read_csv(abm_root / "data" / f"party_positions_{year}.csv")
    return p["party"].tolist()


def table(polls: pd.DataFrame, results: pd.DataFrame, parties: list[str], start: str, end: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(poll table in the ABM's format, dropped polls with the missing parties)."""
    year = int(polls["election"].iloc[0])
    party_of = results[results["election"] == year].set_index("candidate")["party"]
    d = polls[polls["ballot_scenario"] & (polls["share_status"] != "not_tested") & polls["slot"].notna()].copy()
    d = d[(d["date"] >= start) & (d["date"] <= end)]
    d["party_code"] = d["slot"].map(party_of)
    d = d[d["party_code"].isin(parties)]
    d["value"] = np.where(d["share_status"] == "value", d["share"], d["share_upper_bound"] * 0.5)
    rows, dropped = [], []
    for pid, g in d.groupby("poll_id"):
        shares = g.groupby("party_code")["value"].sum()
        missing = [p for p in parties if p not in shares.index]
        first = g.iloc[0]
        if missing:
            dropped.append(dict(year=year, poll_id=pid, source=first["institute_raw"], date=first["date"],
                                not_tested=" ".join(missing)))
            continue
        below = sorted(g.loc[g["share_status"] == "below_threshold", "party_code"].unique())
        row = dict(source=first["institute_raw"], date=pd.Timestamp(first["date"]).strftime("%d/%m/%Y"),
                   fieldwork=" to ".join(dict.fromkeys(str(x) for x in (first["fieldwork_start"], first["fieldwork_end"])
                                                      if pd.notna(x))) or str(first["reported_date"]),
                   rolling="yes" if str(first["rolling"]).lower() == "true" else "no",
                   below_threshold=" ".join(below), poll_id=pid)
        row.update({p: shares[p] / 100 for p in parties})
        rows.append(row)
    out = pd.DataFrame(rows)
    out["_d"] = pd.to_datetime(out["date"], format="%d/%m/%Y")
    out = out.sort_values(["_d", "source"], ascending=[False, True]).drop(columns="_d")
    return out, pd.DataFrame(dropped)


def weekly(tab: pd.DataFrame, parties: list[str]) -> pd.DataFrame:
    """The weekly signal as the ABM computes it: ISO-week means, each week rescaled to sum to 1."""
    d = tab.assign(_d=pd.to_datetime(tab["date"], format="%d/%m/%Y"))
    iso = d["_d"].dt.isocalendar()
    w = d.assign(year_week=list(zip(iso["year"], iso["week"]))).groupby("year_week")[parties].mean()
    return w.div(w.sum(axis=1), axis=0)


def write(tab: pd.DataFrame, parties: list[str], path: Path) -> None:
    """Write in the ABM's format: comma decimals, quoted."""
    cols = ["source", "date", "fieldwork", "rolling", "below_threshold"] + parties
    out = tab[cols].copy()
    for p in parties:
        out[p] = out[p].map(lambda v: f"{v:.4g}".replace(".", ","))
    path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(path, index=False)
