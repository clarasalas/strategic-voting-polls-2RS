"""Structure of a vote distribution: concentration, gaps, cliff, roles.

Shares are in percent. HHI is computed two ways (Part 0 of docs/study_plan.md):
- rescaled: shares divided by their total, so HHI = 1 / ENP exactly as in the ABM
  (core_model.metrics.enp);
- raw: shares / 100 as they are, so a poll whose shares sum below 100 (missing small
  candidates) gets a lower HHI.
Below-threshold shares ('<0.5') count as half their bound.

The cliff is the ABM's (core_model/functions.py, coordination_measures): the largest drop between
consecutive sorted shares (magnitude, in points), its location (how many candidates sit above
it) and its bounded ratio d* / (d* + mean of the other drops), near 1 for a sharp cliff and
near 0.5 for a diffuse one. The gap between the 2nd and the 3rd is kept as gap_23.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

ROLES = ["leader", "2nd", "3rd", "other"]


def shares_of(rows: pd.DataFrame, below_threshold: float = 0.5) -> pd.Series:
    """candidate -> share for the tested candidates of one scenario (or one result)."""
    r = rows[rows["share_status"].isin(["value", "below_threshold"])]
    s = r["share"].where(r["share_status"] == "value", r["share_upper_bound"] * below_threshold)
    return pd.Series(s.to_numpy(dtype=float), index=r["candidate"].to_numpy()).fillna(0.0)


def hhi(shares, rescale: bool = True) -> float:
    s = np.asarray(shares, dtype=float)
    s = s / s.sum() if rescale else s / 100.0
    return float((s ** 2).sum())


def enp(shares) -> float:
    """Effective number of parties, as in the ABM: 1 / rescaled HHI."""
    return 1.0 / hhi(shares, rescale=True)


def roles(shares: pd.Series) -> pd.Series:
    """candidate -> role by rank; tied candidates share the higher role (two '2nd', no '3rd')."""
    rank = shares.rank(method="min", ascending=False).astype(int)
    return rank.map(lambda k: ROLES[k - 1] if k <= 3 else "other")


def cliff(shares) -> tuple[int, float, float]:
    """(location k*, magnitude d*, ratio r') exactly as in the ABM's _cliff_stats."""
    s = np.sort(np.asarray(shares, dtype=float))[::-1]
    if len(s) < 2:
        return 1, 0.0, 0.5
    drops = s[:-1] - s[1:]
    idx = int(np.argmax(drops))
    d_star = float(drops[idx])
    rest = np.concatenate([drops[:idx], drops[idx + 1:]])
    rest_mean = rest.mean() if len(rest) else 0.0
    ratio = d_star / (d_star + rest_mean) if (d_star + rest_mean) > 0 else 0.5
    return idx + 1, d_star, float(ratio)


def structure(shares: pd.Series, contention_points: float = 5.0) -> dict:
    """Concentration and gaps of one distribution. `shares` as from shares_of()."""
    s = shares.sort_values(ascending=False)
    v = s.to_numpy()
    top = lambda k: v[k] if len(v) > k else np.nan
    k_star, d_star, r_prime = cliff(v)
    return dict(
        n_candidates=len(v),
        total=float(v.sum()),
        hhi=hhi(v, rescale=True),
        hhi_raw=hhi(v, rescale=False),
        enp=enp(v),
        top2_share=float(v[:2].sum()),
        gap_12=top(0) - top(1),
        cliff=d_star,
        cliff_location=k_star,
        cliff_ratio=r_prime,
        gap_23=top(1) - top(2),
        gap_23_rel=(top(1) - top(2)) / top(1) if len(v) > 2 and top(1) > 0 else np.nan,
        gap_34=top(2) - top(3),
        # candidates within `contention_points` of the 2nd (the 2nd included)
        n_in_contention=int((v[1:] >= top(1) - contention_points).sum()) if len(v) > 1 else 0,
        first=s.index[0] if len(v) else None,
        second=s.index[1] if len(v) > 1 else None,
        third=s.index[2] if len(v) > 2 else None,
        fourth=s.index[3] if len(v) > 3 else None,
    )
