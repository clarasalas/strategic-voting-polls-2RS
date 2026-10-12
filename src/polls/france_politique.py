"""Parse the france-politique.fr 2002 first-round poll page.

Layout: one table per institute series. Row 0 = '<institute>/<sponsor>' then one
fieldwork date per column; then one row per candidate; a '100' total row; sometimes a
footer row of sponsor abbreviations, explained in text after some tables
('LP : Le Point - LF : Le Figaro').

Cells: number (comma decimals), 'ns' (not tested), 'autres' (candidate counted in the
'Autres' row), or blank. The IFOP tables have an 'Autres' row holding the aggregate.

The file declares windows-1252, but some tables were pasted in as UTF-8, so text is
decoded as cp1252 and then repaired string by string.
"""
from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

from .html_tables import expand
from .textparse import ParseError, clean, parse_fp_date, parse_number

DEFAULT_YEAR = 2002   # columns without a year all fall in January-April 2002

# Abbreviations used in footer rows but not explained on the page.
EXTRA_ABBREVIATIONS = {"BFM": "BFM", "MIDI": "La Dépêche du Midi"}


def fix_mojibake(s: str) -> str:
    """'MÃ©gret' -> 'Mégret'. Leaves correctly decoded text unchanged."""
    if "Ã" not in s and "Â" not in s:
        return s
    try:
        return s.encode("cp1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def _text(el) -> str:
    return clean(fix_mojibake(el.get_text(" ")))


def _legend(soup) -> dict[str, str]:
    """'LP : Le Point - LF : Le Figaro - E1 : Europe 1' -> {'LP': 'Le Point', ...}."""
    out = dict(EXTRA_ABBREVIATIONS)
    for s in soup.find_all(string=True):
        if not isinstance(s, NavigableString) or s.find_parent("table") or s.find_parent(["script", "style"]):
            continue
        txt = clean(fix_mojibake(str(s)))
        for part in re.split(r"\s+-\s+", txt):
            m = re.fullmatch(r"([A-Z0-9]{1,5}|\*)\s*:\s*(.+)", part)
            if m and m.group(1) != "*":
                out[m.group(1)] = m.group(2)
    return out


def _expand_sponsors(footer: str, legend: dict) -> str | None:
    if not footer:
        return None
    return "/".join(legend.get(p.strip(), p.strip()) for p in footer.split("/"))


def parse_page(path: Path) -> tuple[list[dict], list[dict]]:
    raw = Path(path).read_bytes().decode("cp1252")
    soup = BeautifulSoup(raw, "lxml")
    legend = _legend(soup)
    rows, errors = [], []

    for table_no, table in enumerate(soup.find_all("table")):
        grid = [[c for c in r] for r in expand(table)]
        text = [[_text(c.el) if c else "" for c in r] for r in grid]
        header = text[0]
        series = header[0]
        institute, _, header_sponsor = series.partition("/")
        dates = header[1:]

        cand_rows, footer = [], None
        for r in text[1:]:
            label, cells = r[0], r[1:]
            if label:
                cand_rows.append((label, cells))
            elif all(re.fullmatch(r"\d+", c or "") for c in cells if c):
                continue                                   # '100' total row
            else:
                footer = cells

        for j, date_raw in enumerate(dates):
            loc = f"table {table_no} ({series}) col {j + 1}"
            try:
                span = parse_fp_date(date_raw, DEFAULT_YEAR)
            except ParseError as e:
                errors.append(dict(source="france_politique", election=2002, location=loc, raw=date_raw, reason=str(e)))
                span = None
            sponsors = [header_sponsor or None, _expand_sponsors(footer[j], legend) if footer else None]
            base = dict(
                election=2002, source="france_politique", institute=institute.strip(),
                sponsor="; ".join(s for s in sponsors if s) or None,
                fieldwork_start=span.start if span else None, fieldwork_end=span.end if span else None,
                publication_date=None, reported_date=None, date_raw=date_raw,
                sample_size=None, effective_base=None, population_base=None, mode=None, panel=None,
                rolling=None, upstream_source_url=None, notice_url=None, wiki_revision_id=None,
                table_label=series, source_poll_ref=loc, page_poll_no=(table_no, j), scenario_no=1,
                scenario_label=None,
            )
            for label, cells in cand_rows:
                cell = cells[j] if j < len(cells) else ""
                low = cell.lower()
                rec = dict(candidate_raw=label, candidate_column=label, name_hint=None, share_upper_bound=None)
                if low == "ns":
                    rec.update(share=None, share_status="not_tested")
                elif low == "autres":
                    rec.update(share=None, share_status="grouped_others")
                elif low == "":
                    rec.update(share=None, share_status="missing")
                else:
                    try:
                        rec.update(share=parse_number(cell), share_status="value")
                    except ParseError as e:
                        errors.append(dict(source="france_politique", election=2002,
                                           location=f"{loc} row {label}", raw=cell, reason=str(e)))
                        continue
                rows.append({**base, **rec})
    return rows, errors
