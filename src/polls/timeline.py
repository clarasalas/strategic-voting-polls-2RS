"""Time axis shared by the study notebooks: days before the first round, and campaign phases.

Dates come from config/elections.yaml. A poll is placed at its `date` (end of fieldwork; in 2007
and 2012, the publication date).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

PHASES = ["before the official list", "official list to two weeks before", "last two weeks"]
LAST_WEEKS_DAYS = 14


def load(path: Path) -> pd.DataFrame:
    """One row per election: first_round, official_list (Timestamps)."""
    raw = yaml.safe_load(path.read_text())
    out = pd.DataFrame.from_dict(raw, orient="index")
    out.index = out.index.astype(int)
    return out.apply(pd.to_datetime)


def add_time(polls: pd.DataFrame, calendar: pd.DataFrame) -> pd.DataFrame:
    """Add days_before, weeks_before (1 = the last 7 days) and phase."""
    out = polls.copy()
    date = pd.to_datetime(out["date"])
    vote = out["election"].map(calendar["first_round"])
    listed = out["election"].map(calendar["official_list"])
    out["days_before"] = (vote - date).dt.days
    out["weeks_before"] = (out["days_before"] - 1) // 7 + 1
    phase = pd.Series(PHASES[1], index=out.index)
    phase[date < listed] = PHASES[0]
    phase[out["days_before"] <= LAST_WEEKS_DAYS] = PHASES[2]
    out["phase"] = pd.Categorical(phase, categories=PHASES, ordered=True)
    return out
