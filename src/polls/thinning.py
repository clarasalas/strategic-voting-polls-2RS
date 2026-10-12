"""Remove sample overlap between releases of the same poll series (Erikson & Wlezien).

A series is one pollster working for one client. Within a series, releases are taken
from the latest backwards: a release is kept if its fieldwork ends before the start of
the last kept release, so every interview counts at most once and the final
pre-election release is always kept. For a 3-day rolling poll this keeps every third
day, as Erikson and Wlezien did.

Nothing is deleted: thin() returns one row per poll with `kept`, `overlaps_with` and a
`reason`. Where the client is unknown (Wikipedia, outside rolling-marked series),
overlapping polls are kept and flagged `overlap_client_unknown` instead.
"""
from __future__ import annotations

import re

import pandas as pd

from .textparse import strip_accents

POLL_FIELDS = ["election", "source", "poll_id", "institute", "institute_raw", "sponsor", "rolling",
               "table_label", "fieldwork_start", "fieldwork_end", "reported_date"]


def _norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", strip_accents(str(s)).lower())


# The same client under two names. i>Télé was renamed CNews on 27 February 2017.
CLIENT_ALIASES = {"itele": "cnews", "i>tele": "cnews", "i-tele": "cnews"}


def _norm_clients(s) -> str:
    """'Paris Match, Sud Radio, LCI' and 'Paris Match, LCI, Sud Radio' (or 'CNews' and 'Cnews',
    or 'iTELE' and 'CNews') are one client set. Clients are separated by ',' or '&'."""
    if not isinstance(s, str) or not s.strip():
        return "?"
    names = (strip_accents(p).strip().lower() for p in re.split(r"[,&]", s) if p.strip())
    return ", ".join(sorted({CLIENT_ALIASES.get(n, n) for n in names}))


def series_key(polls: pd.DataFrame, clients: dict[str, str] | None = None) -> pd.Series:
    """Pollster + client, as precisely as each source allows. None = no known series.

    - france_politique: the table (one table per institute/client series, e.g. 'CSA/Libération').
    - nsppolls: pollster + commanditaire (client order normalised).
    - wikipedia: no client column, and dates alone cannot tell a rolling series from two
      clients polling the same week (2002: Ifop for the JDD and for L'Express a day apart).
      Only releases the page marks as rolling form a series; other polls stand alone and
      same-pollster overlaps are flagged instead (see thin()).
    - `clients`: poll_id -> client(s) looked up by hand (validation/flagged_clients.csv);
      such a poll joins the series of its pollster and client.
    """
    clients = clients or {}
    keys = []
    for r in polls.itertuples():
        if clients.get(r.poll_id):
            keys.append(f"{_norm_name(r.institute)} | {_norm_clients(clients[r.poll_id])}")
        elif r.source == "france_politique":
            keys.append(f"{r.institute} | {r.table_label}")
        elif r.source == "nsppolls":
            keys.append(f"{r.institute} | {_norm_clients(r.sponsor)}")
        elif r.rolling is True or r.rolling == "True":
            keys.append(f"{_norm_name(r.institute_raw)} [rolling]")
        else:
            keys.append(None)
    return pd.Series(keys, index=polls.index, dtype=object)


def thin(polls: pd.DataFrame, clients: dict[str, str] | None = None) -> pd.DataFrame:
    """polls: one row per poll (POLL_FIELDS). Returns them with series, kept, overlaps_with, reason.
    `clients`: hand-looked-up clients for polls whose source doesn't record one."""
    p = polls.reset_index(drop=True)
    for c in ("fieldwork_start", "fieldwork_end", "reported_date"):
        p[c] = pd.to_datetime(p[c])
    p["series"] = series_key(p, clients)
    p["client_from_validation"] = p["poll_id"].isin([k for k, v in (clients or {}).items() if v])
    p["end"] = p["fieldwork_end"].fillna(p["reported_date"])
    p["kept"], p["overlaps_with"], p["reason"] = True, None, "no overlap"
    p["overlap_client_unknown"] = False

    for _, g in p.dropna(subset=["series"]).groupby(["election", "source", "series"]):
        last_kept = None
        for i in g.sort_values(["end", "fieldwork_start"], ascending=False).index:
            if pd.isna(p.at[i, "fieldwork_start"]):
                p.at[i, "reason"] = "single date: overlap cannot be assessed, kept"
                continue
            if last_kept is not None and p.at[i, "end"] >= p.at[last_kept, "fieldwork_start"]:
                p.at[i, "kept"], p.at[i, "overlaps_with"] = False, p.at[last_kept, "poll_id"]
                p.at[i, "reason"] = "fieldwork overlaps a later kept release of the same series"
            else:
                last_kept = i

    # Polls outside any known series that overlap another poll by the same pollster:
    # kept, but flagged so an analysis can be rerun without them.
    alone = p[p["series"].isna() & p["fieldwork_start"].notna()]
    for _, g in alone.groupby(["election", "source", "institute"]):
        g = g.sort_values("fieldwork_start")
        for a, b in zip(g.index, g.index[1:]):
            if p.at[b, "fieldwork_start"] <= p.at[a, "end"]:
                for i, j in ((a, b), (b, a)):
                    p.at[i, "overlap_client_unknown"] = True
                    p.at[i, "overlaps_with"] = p.at[i, "overlaps_with"] or p.at[j, "poll_id"]
                    p.at[i, "reason"] = "overlaps a poll by the same pollster; client unknown, kept"
    return p.drop(columns="end")


def residual_overlaps(thinned: pd.DataFrame) -> pd.DataFrame:
    """Kept polls by the same pollster (different series) whose fieldwork overlaps.
    Diagnostic only: these are usually independent polls for different clients, but a
    series split by inconsistent client spelling would also show up here."""
    k = thinned[thinned["kept"] & thinned["fieldwork_start"].notna()]
    out = []
    for (e, s, inst), g in k.groupby(["election", "source", "institute"]):
        g = g.sort_values("fieldwork_start")
        rows = list(g.itertuples())
        for a, b in zip(rows, rows[1:]):
            if b.fieldwork_start <= a.fieldwork_end and a.series != b.series:
                out.append(dict(election=e, source=s, institute=inst, poll_a=a.poll_id, series_a=a.series,
                                poll_b=b.poll_id, series_b=b.series))
    return pd.DataFrame(out)
