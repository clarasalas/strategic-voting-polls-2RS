"""Worklists for manual checks, written to validation/ and then filled in by hand.

A worklist is written only if the file doesn't exist yet, so filled-in answers are
never overwritten. If it exists, the poll list is compared with what the notebook
would write now and any difference is reported.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

FILL = ["document_url", "dates_ok", "sample_size_ok", "shares_ok", "notes"]   # yes / no / n.a.


def shares_text(polls: pd.DataFrame) -> pd.Series:
    """poll_id -> 's1: Chirac 19.5 | Jospin 18 | ...; s2: ...' (shares as parsed, for comparison by eye)."""
    def fmt(r):
        if r.share_status == "value":
            v = f"{r.share:g}"
        elif r.share_status == "below_threshold":
            v = f"<{r.share_upper_bound:g}"
        else:
            return None
        return f"{r.candidate} {v}"
    p = polls.assign(txt=[fmt(r) for r in polls.itertuples()]).dropna(subset=["txt"])
    p = p.assign(sc=p["scenario_id"].str.rsplit("_", n=1).str[-1])
    per_sc = p.groupby(["poll_id", "sc"])["txt"].agg(" | ".join).reset_index()
    return per_sc.groupby("poll_id").apply(lambda g: "; ".join(f"{s}: {t}" for s, t in zip(g["sc"], g["txt"])))


def read(path: Path) -> pd.DataFrame:
    """Read a worklist whatever the separator: a French-locale Excel saves CSV with ';'."""
    return pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig", sep=None, engine="python")


def write(path: Path, df: pd.DataFrame, key: str = "poll_id", fill=FILL) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        out = df.copy()
        for c in fill:
            if c not in out:
                out[c] = ""
        out.to_csv(path, index=False, encoding="utf-8-sig")   # BOM: Excel then shows accents correctly
        return f"written: {path.name} ({len(out)} rows to check)"
    existing = read(path)
    old, new = set(existing[key]), set(df[key].astype(str))
    filled = (existing[[c for c in fill if c in existing]] != "").any(axis=1).sum()
    msg = f"kept existing {path.name}: {filled}/{len(existing)} rows have answers"
    if old != new:
        msg += f"; WARNING: current list differs ({len(new - old)} new, {len(old - new)} no longer listed)"
    return msg
