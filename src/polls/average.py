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
           min_polls: float = 3.0, adaptive_k: int | None = None, max_h: float = 45.0) -> pd.DataFrame:
    """days, values: one entry per poll. grid: days before the vote at which to evaluate.
    adaptive_k: the bandwidth is max(h, distance to the k-th nearest poll), so it widens smoothly
    where polls are sparse, up to max_h days (beyond, the day is left empty). `sparse` marks the
    days where the fixed bandwidth h would not have had min_polls."""
    days, values = np.asarray(days, float), np.asarray(values, float)
    ok = ~np.isnan(values)
    days, values = days[ok], values[ok]
    out = np.full((len(grid), 4), np.nan)
    for i, d in enumerate(grid):
        w0 = np.exp(-0.5 * ((days - d) / h) ** 2)
        sparse = w0.sum() < 1e-9 or w0.sum() ** 2 / (w0 ** 2).sum() < min_polls
        hd = h
        if adaptive_k:
            if len(days) < adaptive_k:
                continue
            hd = max(h, np.sort(np.abs(days - d))[adaptive_k - 1])
            if hd > max_h:
                continue
        w = np.exp(-0.5 * ((days - d) / hd) ** 2)
        if w.sum() < 1e-9:
            continue
        n_eff = w.sum() ** 2 / (w ** 2).sum()
        if n_eff < (2 if adaptive_k else min_polls):
            continue
        m = (w * values).sum() / w.sum()
        sd = np.sqrt((w * (values - m) ** 2).sum() / w.sum())
        out[i] = (m, sd, n_eff, float(sparse))
    out = pd.DataFrame(out, columns=["mean", "sd", "n_eff", "sparse"], index=pd.Index(grid, name="days_before"))
    out["sparse"] = out["sparse"] == 1.0
    return out


def by_candidate(table: pd.DataFrame, value: str, grid: np.ndarray, key: str = "slot", **kw) -> pd.DataFrame:
    """Poll average of `value` for each `key` in a one-row-per-(poll, key) table with days_before."""
    parts = []
    for k, g in table.groupby(key):
        s = smooth(g["days_before"].to_numpy(), g[value].to_numpy(), grid, **kw)
        parts.append(s.assign(**{key: k}).reset_index())
    return pd.concat(parts, ignore_index=True)


def leave_one_out(days: np.ndarray, values: np.ndarray, h: float = 10.0, min_polls: float = 3.0) -> np.ndarray:
    """For each poll, the kernel average of the *other* polls at its date (NaN if too few nearby).
    The poll is left out so that it does not pull the average toward itself."""
    days, values = np.asarray(days, float), np.asarray(values, float)
    w = np.exp(-0.5 * ((days[:, None] - days[None, :]) / h) ** 2)
    np.fill_diagonal(w, 0.0)
    w[:, np.isnan(values)] = 0.0
    s = w.sum(axis=1)
    n_eff = np.divide(s ** 2, (w ** 2).sum(axis=1), out=np.zeros_like(s), where=(w ** 2).sum(axis=1) > 0)
    mean = np.divide(w @ np.nan_to_num(values), s, out=np.full_like(s, np.nan), where=s > 1e-9)
    mean[n_eff < min_polls] = np.nan
    return mean
