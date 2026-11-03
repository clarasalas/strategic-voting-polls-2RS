"""Left-right order of the candidates, as Wikipedia orders its poll-table columns.

The French Wikipedia lists the candidates of each poll table from left to right. A candidate's
position is their column's place among the candidate columns (0 = leftmost, 1 = rightmost),
averaged over the tables of the election's first-round section. Used to order and colour
figures (a palette after Spectral: red on the left, blue on the right), not as a measure of ideology.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from .html_tables import expand
from .wikipedia import _classify_columns, _heading_context, _n_header_rows, load_html


def column_positions(path: Path, election: int) -> pd.DataFrame:
    """One row per (table, candidate column): its label and relative position."""
    soup = BeautifulSoup(load_html(path)[0], "lxml")
    rows = []
    for table_no, table in enumerate(soup.find_all("table", class_="wikitable")):
        if "premier tour" not in _heading_context(table).get("h2", "").lower():
            continue
        grid = expand(table)
        cols = _classify_columns(grid, _n_header_rows(grid))
        cand = [info["label"] for c, info in sorted(cols.items()) if info["kind"] == "candidate"]
        for i, label in enumerate(cand):
            rows.append(dict(election=election, table=table_no, candidate_column=label,
                             position=i / (len(cand) - 1) if len(cand) > 1 else 0.5))
    return pd.DataFrame(rows)


def order(raw_dir: Path, sources: dict, polls: pd.DataFrame) -> pd.DataFrame:
    """(election, candidate) -> mean column position. `sources`: election -> raw page path.
    `polls`: rows with election, candidate, candidate_column (to map column labels to candidates)."""
    pos = pd.concat([column_positions(p, e) for e, p in sources.items()], ignore_index=True)
    label_to_cand = (polls.dropna(subset=["candidate_column"])
                     .groupby(["election", "candidate_column"])["candidate"].agg(lambda x: x.mode().iloc[0]))
    pos["candidate"] = [label_to_cand.get((e, l)) for e, l in zip(pos["election"], pos["candidate_column"])]
    return (pos.dropna(subset=["candidate"]).groupby(["election", "candidate"])["position"].mean()
            .rename("position").reset_index())


def _luminance(rgb) -> float:
    """Relative luminance (WCAG): perceived brightness, 0 black to 1 white."""
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


# Spectral's colours, left (red) to right (purple-blue), with its pale yellow and light green replaced
# by amber and a deeper green so every colour reads on white and neighbours stay distinct.
LEFT_RIGHT = ["#9e0142", "#d53e4f", "#f46d43", "#e09000", "#6aa84f", "#2a9d8f", "#3288bd", "#5e4fa2"]


def colours(candidates_left_to_right: list[str], max_luminance: float = 0.35) -> dict:
    """Evenly spaced colours along LEFT_RIGHT, in the given left-to-right order."""
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("left_right", LEFT_RIGHT)
    n = len(candidates_left_to_right)
    out = {}
    for i, c in enumerate(candidates_left_to_right):
        rgb = list(cmap(i / (n - 1) if n > 1 else 0.5)[:3])
        while _luminance(rgb) > max_luminance:
            rgb = [x * 0.95 for x in rgb]
        out[c] = tuple(rgb)
    return out
