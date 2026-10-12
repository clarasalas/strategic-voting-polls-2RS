"""Parse first-round poll tables from French Wikipedia "Liste de sondages" pages.

The five pages share a skeleton (one wikitable per period, a 'Sondeur' column, a date
column, one column per candidate) but differ in details that are handled here:

- 2002/2007/2012: no sample size; 2012 puts the candidate's name in the cell when a
  party's candidate varies across scenarios ("24 % Aubry").
- 2017/2022: sample size, abstention/undecided columns (ignored), an "Autres
  (candidats)" column that lists extra named candidates ("0,5 % Thouy",
  "Yade : 1 % Guaino : <0,5 %"; it is not an aggregate "others" share),
  "(rolling)" after the pollster's name (2022), links to the poll's source in the
  pollster cell.
- Scenarios are rows sharing one rowspanned pollster cell.

Only tables under an h2 heading containing "premier tour" are read; second-round,
vote-transfer and sub-sample tables live under other h2 headings.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag

from .html_tables import expand
from .textparse import (
    ParseError, clean, month_number, parse_extra_candidates_cell, parse_fr_date, parse_int,
    parse_share_cell, strip_accents,
)

COMMISSION_DOMAIN = "commission-des-sondages.fr"

META_COLUMNS = {
    "sondeur": "institute",
    "date": "date",
    "dates": "date",
    "echantillon": "sample",
    "autres": "extra",          # overflow column of extra named candidates, not an aggregate
    "abstention": None,
    "indecis": None,
    "non exprime": None,
}


def load_html(path: Path) -> tuple[str, int]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))["parse"]
    return data["text"], int(data["revid"])


# --------------------------------------------------------------------------- context

def _heading_context(table: Tag) -> dict:
    """The h2, h3 (inside that h2) and h4 (inside that h3) that a table sits under."""
    ctx = {}
    for h in table.find_all_previous(["h2", "h3", "h4"]):
        level = h.name
        if level == "h2":
            ctx["h2"] = clean(h.get_text(" "))
            break
        if level == "h3" and "h3" not in ctx:
            ctx["h3"] = clean(h.get_text(" "))
        if level == "h4" and "h4" not in ctx and "h3" not in ctx:
            ctx["h4"] = clean(h.get_text(" "))
    cap = table.find("caption")
    ctx["caption"] = clean(cap.get_text(" ")) if cap else ""
    return ctx


def _context_year(ctx: dict, election: int) -> int | None:
    """Year from the caption, else h4, else h3. A label naming several years
    ('Années 2017-2020') gives None: dates in that table must carry their own year.
    No year anywhere (e.g. 'Sondages réalisés après la publication...') -> election year."""
    for key in ("caption", "h4", "h3"):
        years = set(re.findall(r"\b(19\d\d|20\d\d)\b", ctx.get(key, "")))
        if len(years) == 1:
            return int(years.pop())
        if len(years) > 1:
            return None
    return election


def _context_month(ctx: dict) -> int | None:
    for key in ("caption", "h4"):
        words = re.findall(r"[A-Za-zÀ-ÿ]+", ctx.get(key, ""))
        if not words or len(words) > 3:
            continue
        months = {month_number(w) for w in words if len(w) >= 3} - {None}
        if len(months) == 1:
            return months.pop()
    return None


def _table_label(ctx: dict) -> str:
    return " / ".join(v for k in ("h3", "h4", "caption") if (v := ctx.get(k)))


# --------------------------------------------------------------------------- links

def _reference_links(soup: BeautifulSoup) -> dict[str, list[str]]:
    """cite_note id -> external URLs cited in that footnote."""
    out = {}
    for li in soup.select("ol.references > li[id]"):
        out[li["id"]] = [a["href"] for a in li.find_all("a", class_="external", href=True)]
    return out


def _cell_links(el: Tag, refs: dict[str, list[str]]) -> list[str]:
    urls = [a["href"] for a in el.find_all("a", class_="external", href=True)]
    for sup in el.find_all("sup", class_="reference"):
        a = sup.find("a", href=True)
        if a and a["href"].startswith("#"):
            urls += refs.get(a["href"][1:], [])
    return urls


def _split_links(urls: list[str]) -> tuple[str | None, str | None]:
    notice = next((u for u in urls if COMMISSION_DOMAIN in u), None)
    upstream = next((u for u in urls if COMMISSION_DOMAIN not in u), None)
    return upstream, notice


def _text(el: Tag) -> str:
    """Cell text without footnote markers."""
    el = BeautifulSoup(str(el), "lxml").find(el.name)
    for sup in el.find_all("sup"):
        sup.decompose()
    return clean(el.get_text(" "))


# --------------------------------------------------------------------------- columns

def _n_header_rows(grid) -> int:
    """Header rows = the rows covered by the tallest cell of the first row."""
    return max(int(c.el.get("rowspan", 1) or 1) for c in grid[0] if c is not None)


def _candidate_label(text: str) -> str:
    """'Arthaud ( LO )' -> 'Arthaud (LO)'."""
    return re.sub(r"\(\s*(.*?)\s*\)", r"(\1)", text)


def _classify_columns(grid, n_header: int) -> dict[int, dict]:
    """Map each column to {'kind': institute/date/sample/extra/candidate/None, 'label', 'hint'}."""
    cols = {}
    for c in range(len(grid[0])):
        top = grid[0][c]
        if top is None:
            continue
        rowspan = int(top.el.get("rowspan", 1) or 1)
        if rowspan >= n_header or _text(top.el).lower().startswith("autres"):
            label = _text(top.el)
            key = strip_accents(label).lower()
            kind = next((v for k, v in META_COLUMNS.items() if key.startswith(k)), "unknown")
            cols[c] = {"kind": kind, "label": label, "hint": None}
        else:
            below = [grid[r][c] for r in range(1, n_header)
                     if grid[r][c] is not None and grid[r][c].is_header and grid[r][c].origin[0] > 0]
            label = _candidate_label(_text(below[-1].el) if below else _text(top.el))
            link = top.el.find("a", title=True)
            cols[c] = {"kind": "candidate", "label": label, "hint": link["title"] if link else None}
    return cols


# --------------------------------------------------------------------------- main

def parse_page(path: Path, election: int) -> tuple[list[dict], list[dict]]:
    """Return (rows, errors). One row per poll x scenario x candidate."""
    html, revid = load_html(path)
    soup = BeautifulSoup(html, "lxml")
    refs = _reference_links(soup)
    rows, errors = [], []

    def err(table_no, label, row_no, col, raw, reason):
        errors.append(dict(source="wikipedia", election=election, location=f"table {table_no} ({label}) row {row_no} col {col}",
                           raw=raw, reason=reason))

    poll_no = 0
    for table_no, table in enumerate(soup.find_all("table", class_="wikitable")):
        ctx = _heading_context(table)
        if "premier tour" not in ctx.get("h2", "").lower():
            continue
        label = _table_label(ctx)
        ctx_year, ctx_month = _context_year(ctx, election), _context_month(ctx)
        grid = expand(table)
        n_header = _n_header_rows(grid)
        cols = _classify_columns(grid, n_header)
        unknown = [v["label"] for v in cols.values() if v["kind"] == "unknown"]
        if unknown:
            raise ParseError(f"{election} table {table_no} ({label}): unclassified columns {unknown}")
        col_of = {v["kind"]: c for c, v in cols.items() if v["kind"] in ("institute", "date", "sample")}

        polls: dict[tuple, list[int]] = {}
        for r in range(n_header, len(grid)):
            row = grid[r]
            cells = [c for c in row if c is not None]
            if not cells or all(_text(c.el) == "" for c in cells):
                continue                                  # colour bar
            if len({c.origin for c in cells}) == 1:
                continue                                  # event annotation spanning the table
            inst = row[col_of["institute"]]
            if _text(inst.el).lower().startswith("résultat"):
                continue
            polls.setdefault(inst.origin, []).append(r)

        for origin, row_nos in polls.items():
            first = grid[row_nos[0]]
            inst_el = first[col_of["institute"]].el
            institute_raw = _text(inst_el)
            rolling = True if re.search(r"\(rolling\)", institute_raw, re.I) else None
            institute = clean(re.sub(r"\(rolling\)", "", institute_raw, flags=re.I))
            date_cell = first[col_of["date"]]
            date_raw = _text(date_cell.el)
            upstream, notice = _split_links(_cell_links(inst_el, refs) + _cell_links(date_cell.el, refs))
            base = dict(
                election=election, source="wikipedia", institute=institute, sponsor=None,
                fieldwork_start=None, fieldwork_end=None, publication_date=None, reported_date=None,
                date_raw=date_raw, sample_size=None, effective_base=None, population_base=None,
                mode=None, panel=None, rolling=rolling, upstream_source_url=upstream, notice_url=notice,
                wiki_revision_id=revid, table_label=label, source_poll_ref=f"table {table_no} row {row_nos[0]}",
            )
            loc = (table_no, label, row_nos[0])
            try:
                span = parse_fr_date(date_raw, ctx_year, ctx_month)
                base.update(fieldwork_start=span.start, fieldwork_end=span.end, reported_date=span.single)
            except ParseError as e:
                err(*loc, col_of["date"], date_raw, str(e))
            if "sample" in col_of:
                raw = _text(first[col_of["sample"]].el)
                if raw and raw not in "-–—" and raw.lower() != "non renseigné":
                    try:
                        base["sample_size"] = parse_int(raw)
                    except ParseError as e:
                        err(*loc, col_of["sample"], raw, str(e))

            scenarios = []
            for r in row_nos:
                cand = []
                # A share cell spanning several candidate columns is one combined figure
                # (2022: Ipsos's single "extrême gauche" share across Arthaud and Poutou),
                # not one value per candidate: read it once, labelled with all its columns.
                span_cols: dict[tuple, list[int]] = {}
                for c, info in cols.items():
                    if info["kind"] == "candidate" and grid[r][c] is not None:
                        span_cols.setdefault(grid[r][c].origin, []).append(c)
                for c, info in cols.items():
                    if info["kind"] not in ("candidate", "extra") or grid[r][c] is None:
                        continue
                    covered = span_cols.get(grid[r][c].origin, [c]) if info["kind"] == "candidate" else [c]
                    if c != covered[0]:
                        continue
                    if len(covered) > 1:
                        info = {**info, "label": " + ".join(cols[k]["label"] for k in covered), "hint": None}
                    raw = _text(grid[r][c].el)
                    parse = parse_extra_candidates_cell if info["kind"] == "extra" else parse_share_cell
                    try:
                        shares = parse(raw)
                    except ParseError as e:
                        err(table_no, label, r, c, raw, str(e))
                        continue
                    for s in shares:
                        name = s.name or info["label"]
                        hint = None if s.name else info["hint"]   # header link describes the column, not a name in the cell
                        cand.append(dict(candidate_raw=name, candidate_column=info["label"], name_hint=hint,
                                         share=s.share, share_status=s.status, share_upper_bound=s.upper_bound))
                if cand:
                    scenarios.append(cand)
            if not scenarios:
                err(*loc, "-", institute_raw, "poll has no candidate cells")
                continue
            poll_no += 1
            for k, cand in enumerate(scenarios, 1):
                for c in cand:
                    rows.append({**base, "page_poll_no": poll_no, "scenario_no": k, "scenario_label": None, **c})
    return rows, errors
