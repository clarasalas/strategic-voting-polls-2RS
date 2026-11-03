"""Small plotting helpers shared by the study notebooks."""
from __future__ import annotations

import numpy as np

SPARSE_ALPHA = 0.35


def line(ax, x, y, sparse, **kw):
    """Plot y against x: full colour where the average rests on enough polls, pale where it is sparse."""
    x, y, sparse = np.asarray(x), np.asarray(y, float), np.asarray(sparse, bool)
    ax.plot(x, np.where(sparse, np.nan, y), **kw)
    kw.pop("label", None)
    # pale stretches, extended by one point each side so they join the full-colour line
    pale = np.where(sparse | np.roll(sparse, 1) | np.roll(sparse, -1), y, np.nan)
    ax.plot(x, pale, alpha=SPARSE_ALPHA, **kw)
