"""Expand HTML tables into a rectangular grid, resolving rowspan and colspan explicitly."""
from __future__ import annotations

from dataclasses import dataclass

from bs4 import Tag


@dataclass(frozen=True)
class GridCell:
    el: Tag            # the <td>/<th> this grid position comes from
    origin: tuple      # (row, col) of the top-left position of that element
    is_header: bool


def _span(el: Tag, attr: str) -> int:
    try:
        return max(1, int(str(el.get(attr, "1")).strip().rstrip(";") or 1))
    except ValueError:
        return 1


def expand(table: Tag) -> list[list[GridCell | None]]:
    """Return table rows as lists of GridCell, one entry per grid column.

    A cell spanning several rows/columns appears at every position it covers, with
    the same `origin`. Positions no cell covers (ragged rows) are None.
    Nested tables are ignored.
    """
    grid: dict[tuple[int, int], GridCell] = {}
    rows = [tr for tr in table.find_all("tr") if tr.find_parent("table") is table]
    for r, tr in enumerate(rows):
        c = 0
        for el in tr.find_all(["td", "th"], recursive=False):
            while (r, c) in grid:
                c += 1
            rs, cs = _span(el, "rowspan"), _span(el, "colspan")
            cell = GridCell(el=el, origin=(r, c), is_header=el.name == "th")
            for dr in range(rs):
                for dc in range(cs):
                    grid.setdefault((r + dr, c + dc), cell)
            c += cs
    if not grid:
        return []
    n_rows = len(rows)
    n_cols = max(c for _, c in grid) + 1
    return [[grid.get((r, c)) for c in range(n_cols)] for r in range(n_rows)]
