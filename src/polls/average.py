"""Poll average: a kernel-weighted mean of the polls around each day.

Each poll counts once (one share per candidate, from its ballot scenario). The average at day d
weights polls by a Gaussian kernel of their distance to d in days (bandwidth `h`); days with
fewer than `min_polls` effective polls nearby are left empty. The band is the kernel-weighted
standard deviation of the polls: how spread out the polls are around the average, not the
uncertainty of the average itself.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def smooth(days: np.ndarray, values: np.ndarray, grid: np.ndarray, h: float = 10.0,
           min_polls: float = 3.0) -> pd.DataFrame:
    """days, values: one entry per poll. grid: days before the vote at which to evaluate."""
    days, values = np.asarray(days, float), np.asarray(values, float)
    ok = ~np.isnan(values)
    days, values = days[ok], values[ok]
    out = np.full((len(grid), 3), np.nan)
    for i, d in enumerate(grid):
        w = np.exp(-0.5 * ((days - d) / h) ** 2)
        if w.sum() < 1e-9:
            continue
        n_eff = w.sum() ** 2 / (w ** 2).sum()
        if n_eff < min_polls:
            continue
        m = (w * values).sum() / w.sum()
        sd = np.sqrt((w * (values - m) ** 2).sum() / w.sum())
        out[i] = (m, sd, n_eff)
    return pd.DataFrame(out, columns=["mean", "sd", "n_eff"], index=pd.Index(grid, name="days_before"))


def by_candidate(table: pd.DataFrame, value: str, grid: np.ndarray, key: str = "slot", **kw) -> pd.DataFrame:
    """Poll average of `value` for each `key` in a one-row-per-(poll, key) table with days_before."""
    parts = []
    for k, g in table.groupby(key):
        s = smooth(g["days_before"].to_numpy(), g[value].to_numpy(), grid, **kw)
        parts.append(s.assign(**{key: k}).reset_index())
    return pd.concat(parts, ignore_index=True)
