"""Small plotting helpers shared by the study notebooks."""
from __future__ import annotations

import numpy as np


def line(ax, x, y, sparse, **kw):
    """Plot y against x, solid where the average rests on enough polls, dashed where it is sparse."""
    x, y, sparse = np.asarray(x), np.asarray(y, float), np.asarray(sparse, bool)
    solid, dashed = np.where(sparse, np.nan, y), np.where(sparse, y, np.nan)
    # extend the dashed stretches by one point each side, so they join the solid line
    dashed = np.where(sparse | np.roll(sparse, 1) | np.roll(sparse, -1), y, np.nan)
    ax.plot(x, solid, **kw)
    kw.pop("label", None)
    ax.plot(x, dashed, ls=(0, (2, 2)), **kw)
