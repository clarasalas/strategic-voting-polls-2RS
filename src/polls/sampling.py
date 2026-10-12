"""Reproducible stratified random sample of polls for manual spot-checks.

Strata are pollsters. Each gets a share of n proportional to its number of polls
(largest-remainder rounding), with at least one poll per pollster when n allows;
polls are then drawn at random within each stratum. The seed fixes the draw.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def allocate(sizes: pd.Series, n: int) -> pd.Series:
    """Proportional allocation with a minimum of 1 per stratum (if n >= number of strata)."""
    sizes = sizes[sizes > 0].sort_index()
    if n >= sizes.sum():
        return sizes.copy()
    base = pd.Series(1 if n >= len(sizes) else 0, index=sizes.index)
    rest = n - base.sum()
    quota = (sizes - base).clip(lower=0) / (sizes - base).clip(lower=0).sum() * rest
    alloc = base + np.floor(quota).astype(int)
    remainder = (quota - np.floor(quota)).sort_values(ascending=False)
    for k in remainder.index[: n - alloc.sum()]:
        alloc[k] += 1
    return alloc.clip(upper=sizes)


def draw(frame: pd.DataFrame, n: int, seed: int, stratum: str = "institute") -> pd.DataFrame:
    """frame: one row per poll, sorted deterministically before drawing."""
    frame = frame.sort_values("poll_id").reset_index(drop=True)
    rng = np.random.default_rng(seed)
    alloc = allocate(frame.groupby(stratum).size(), n)
    picks = []
    for s, k in alloc.items():
        idx = frame.index[frame[stratum] == s].to_numpy()
        picks.extend(rng.choice(idx, size=int(k), replace=False))
    return frame.loc[sorted(picks)]
