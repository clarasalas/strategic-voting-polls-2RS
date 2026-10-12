"""French number, share and date parsing shared by all parsers.

Every function either returns a parsed value or raises ParseError with a reason;
callers record the raw text in parse_errors.csv instead of dropping the row.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import date


class ParseError(ValueError):
    pass


SPACES = "     "
DASHES = {"-", "–", "—", "−", "‒"}


def clean(text: str) -> str:
    """Collapse all kinds of whitespace to single spaces and strip."""
    text = text.replace(" ", " ").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip()


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def slug(s: str) -> str:
    s = strip_accents(s).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


# --------------------------------------------------------------------------- numbers

def parse_number(text: str) -> float:
    """'1,5' -> 1.5, '20.5' -> 20.5, '1 002' -> 1002 (any space as thousands separator)."""
    t = text
    for ch in SPACES:
        t = t.replace(ch, "")
    t = t.replace(",", ".")
    if not re.fullmatch(r"\d+(\.\d+)?", t):
        raise ParseError(f"not a number: {text!r}")
    return float(t)


def parse_int(text: str) -> int:
    v = parse_number(text)
    if v != int(v):
        raise ParseError(f"not an integer: {text!r}")
    return int(v)


# --------------------------------------------------------------------------- shares

@dataclass(frozen=True)
class Share:
    share: float | None
    status: str                      # value / not_tested / grouped_others / below_threshold / missing
    upper_bound: float | None = None
    name: str | None = None          # candidate named inside the cell (e.g. "14 % Bertrand")


_NUM = r"\d+(?:[.,]\d+)?"
_VALUE_RE = re.compile(rf"^(?P<lt><\s*)?(?P<num>{_NUM})\s*%?$")
_VALUE_NAME_RE = re.compile(rf"(?P<lt><\s*)?(?P<num>{_NUM})\s*%?\s+(?P<name>[^\d<]+?)(?=\s*(?:<|\d|$))")


def parse_share_cell(text: str) -> list[Share]:
    """Parse one share cell. Usually returns one Share; several when a cell lists
    alternative candidates with their own value ("1,5 % Joly 6,5 % Hulot")."""
    t = clean(text)
    if t == "":
        return [Share(None, "missing")]
    if t in DASHES:
        return [Share(None, "not_tested")]
    m = _VALUE_RE.match(t)
    if m:
        return [_share(m)]
    out, pos = [], 0
    for m in _VALUE_NAME_RE.finditer(t):
        if t[pos:m.start()].strip():
            break
        out.append(_share(m, name=m.group("name").strip()))
        pos = m.end()
    if out and not t[pos:].strip():
        return out
    raise ParseError(f"unrecognised share cell: {text!r}")


_NAME_VALUE_RE = re.compile(rf"\s*(?P<name>[^:\d<]+?)\s*:\s*(?P<lt><\s*)?(?P<num>{_NUM})\s*%?")


def parse_extra_candidates_cell(text: str) -> list[Share]:
    """Cells of an 'Autres (candidats)' column, which list extra named candidates:
    '0,5 % Thouy', 'Yade : 1 % Guaino : <0,5 %'. A dash or blank means none."""
    t = clean(text)
    if t == "" or t in DASHES:
        return []
    out, pos = [], 0
    for m in _NAME_VALUE_RE.finditer(t):
        if t[pos:m.start()].strip():
            break
        out.append(_share(m, name=m.group("name").strip()))
        pos = m.end()
    if out and not t[pos:].strip():
        return out
    shares = parse_share_cell(t)
    if any(s.name is None for s in shares):
        raise ParseError(f"value without a candidate name in an 'Autres' column: {text!r}")
    return shares


def _share(m, name=None) -> Share:
    v = parse_number(m.group("num"))
    if m.group("lt"):
        return Share(None, "below_threshold", upper_bound=v, name=name)
    return Share(v, "value", name=name)


# --------------------------------------------------------------------------- dates

_MONTHS = [
    ("janv", 1), ("jan", 1), ("fév", 2), ("fev", 2), ("mars", 3), ("mar", 3), ("avr", 4),
    ("mai", 5), ("juin", 6), ("juil", 7), ("aoû", 8), ("aou", 8), ("sept", 9), ("sep", 9),
    ("oct", 10), ("nov", 11), ("déc", 12), ("dec", 12),
]


def month_number(word: str) -> int | None:
    w = word.lower().rstrip(".")
    for prefix, n in _MONTHS:
        if w.startswith(prefix):
            return n
    return None


_TOKEN_RE = re.compile(r"(\d{4})|(\d{1,2})(?:er)?|([A-Za-zÀ-ÿ]+\.?)")


def _parts(side: str):
    """'28 fév.' -> (28, 2, None); '2 mars 2021' -> (2, 3, 2021); '17' -> (17, None, None)."""
    day = month = year = None
    for m in _TOKEN_RE.finditer(side):
        if m.group(1):
            year = int(m.group(1))
        elif m.group(2):
            if day is not None:
                raise ParseError("two day numbers on one side")
            day = int(m.group(2))
        else:
            mn = month_number(m.group(3))
            if mn is None:
                raise ParseError(f"unknown word {m.group(3)!r}")
            month = mn
    if day is None:
        raise ParseError("no day")
    return day, month, year


@dataclass(frozen=True)
class DateSpan:
    start: date | None
    end: date | None
    single: date | None   # a lone date whose meaning (fieldwork or publication) the source doesn't state


def parse_fr_date(text: str, ctx_year: int | None, ctx_month: int | None = None) -> DateSpan:
    """Parse Wikipedia-style French dates.

    Ranges ('17 et 18 avril', 'du 28 février au 1er mars', '20-21 avr.', 'du 17 au 19')
    give start/end. A lone date ('20 avril', 'le 20') gives `single`.
    Missing month/year are taken from the other side of the range, then from the
    table context (`ctx_month`, `ctx_year`).
    """
    t = clean(text).lower()
    t = re.sub(r"^(du|le)\s+", "", t)
    sides = re.split(r"\s*(?:-|–|—|\bau\b|\bet\b)\s*", t)
    if len(sides) > 2 or not all(sides):
        raise ParseError(f"unrecognised date: {text!r}")
    parsed = [_parts(s) for s in sides]
    d2, m2, y2 = parsed[-1]
    m2 = m2 or ctx_month
    y2 = y2 or ctx_year
    if m2 is None or y2 is None:
        raise ParseError(f"date lacks month or year and the table gives none: {text!r}")
    end = _mk(y2, m2, d2, text)
    if len(parsed) == 1:
        return DateSpan(None, None, end)
    d1, m1, y1 = parsed[0]
    if m1 is None:
        m1 = m2 if d1 <= d2 else (m2 - 2) % 12 + 1   # "du 28 au 2" crosses a month
    if y1 is None:
        y1 = y2 if m1 <= m2 else y2 - 1                # "30 déc. - 2 janv." crosses a year
    start = _mk(y1, m1, d1, text)
    return DateSpan(start, end, None)


def _mk(y, m, d, text):
    try:
        return date(y, m, d)
    except ValueError as e:
        raise ParseError(f"invalid date in {text!r}: {e}") from None


_FP_RE = re.compile(
    r"^(?P<d1>\d{1,2})(?:\.(?P<m1>\d{1,2}))?(?:\s*[/-]\s*(?P<d2>\d{1,2}))?"
    r"\.(?P<m2>\d{1,2})(?:\.(?P<y>\d{4}))?$"
)


def parse_fp_date(text: str, default_year: int) -> DateSpan:
    """france-politique column headers: '06/07.09.2000', '28.02-01.03.2002', '13/15.02',
    '17.01.2002'. These are fieldwork dates, so a single day gives start = end."""
    t = clean(text).replace(" ", "")
    m = _FP_RE.match(t)
    if not m:
        raise ParseError(f"unrecognised france-politique date: {text!r}")
    y = int(m["y"]) if m["y"] else default_year
    m2 = int(m["m2"])
    if m["d2"] is None:               # single day, possibly written d.m: '17.01.2002'
        if m["m1"]:
            raise ParseError(f"unrecognised france-politique date: {text!r}")
        d = _mk(y, m2, int(m["d1"]), text)
        return DateSpan(d, d, None)
    end = _mk(y, m2, int(m["d2"]), text)
    m1 = int(m["m1"]) if m["m1"] else m2
    start = _mk(y if m1 <= m2 else y - 1, m1, int(m["d1"]), text)
    return DateSpan(start, end, None)
