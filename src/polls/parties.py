"""Party of each candidate in each poll: the label at the time of the poll.

The label comes first from the poll's own Wikipedia row ("Alain Juppé (UMP)" in 2014, "(LR)" from
2015), so it follows renamings and changes of party over the campaign. config/parties.csv is
hand-editable and covers the rest:

- `party` fills the rows where Wikipedia gives no label, and must be the label at the time of
  those rows (Duflot in 2010: Les Verts, before EELV existed);
- `override` = yes applies `party` to every row of that candidate, replacing Wikipedia's label
  (none at present).

`match`: "label" (taken from the candidate's other Wikipedia labels), "suggested" (a proposal to
check), "manual" (checked or written by hand). Rows already in the file are never changed; new
candidates that need a fallback are added.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

COLUMNS = ["election", "candidate", "labels", "party", "override", "unlabelled_polls", "match", "note"]

# Spelling variants of one label.
SPELLING = {"SP": "S&P", "SÉ": "SE"}

# Initial fill for the rows Wikipedia leaves without a label: (election, candidate) -> (party, override, match, note).
INITIAL = {
    (2002, "Antoine Waechter"): ("MEI", "", "suggested", "Mouvement écologiste indépendant"),
    (2002, "Dieudonné M'Bala M'Bala"): ("SE", "", "suggested", "independent"),
    (2002, "Pierre Larrouturou"): ("SE", "", "manual", "independent: had left the PS (checked by hand)"),
    (2012, "Cécile Duflot"): ("LV", "", "suggested", "polls of 2010, before Les Verts became EELV (November 2010)"),
    (2012, "Jean-Marie Le Pen"): ("FN", "", "suggested", "polls of 2007-2009"),
    (2012, "José Bové"): ("SE", "", "manual", "SE as Wikipedia: unaffiliated, then Europe Écologie (a coalition) from 2008 (checked by hand)"),
    (2017, "Henri Guaino"): ("LR", "", "suggested", "poll of June 2016, still an LR deputy"),
    (2017, "Jean Lassalle"): ("RES", "", "suggested", "poll of June 2016: check that Résistons! existed then"),
    (2017, "Nicolas Hulot"): ("SE", "", "suggested", "polls of 2016"),
    (2017, "Rama Yade"): ("SE", "", "suggested", "poll of June 2016"),
    (2022, "Arnaud Montebourg"): ("DVG", "", "suggested", "polls of January 2021, as his later label"),
    (2022, "Bernard Cazeneuve"): ("PS", "", "suggested", "poll of 2019"),
    (2022, "Bruno Retailleau"): ("LR", "", "suggested", ""),
    (2022, "Denis Payre"): ("LR", "", "suggested", "LR congress candidate, September 2021: check membership"),
    (2022, "François Baroin"): ("LR", "", "suggested", ""),
    (2022, "François Fillon"): ("LR", "", "suggested", "polls of 2017-2018"),
    (2022, "François Hollande"): ("PS", "", "suggested", ""),
    (2022, "Laurent Wauquiez"): ("LR", "", "suggested", ""),
    (2022, "Michel Barnier"): ("LR", "", "suggested", ""),
    (2022, "Olivier Faure"): ("PS", "", "suggested", "PS first secretary"),
    (2022, "Philippe Juvin"): ("LR", "", "suggested", ""),
    (2022, "Rachida Dati"): ("LR", "", "suggested", ""),
    (2022, "Ségolène Royal"): ("PS", "", "suggested", "poll of October 2020: check membership"),
    (2022, "Valérie Pécresse"): ("Libres!", "", "suggested",
                                 "polls of October 2019 to November 2021: left LR in June 2019; check when she rejoined for the congress"),
    (2022, "Xavier Bertrand"): ("DVD", "", "suggested", "polls of 2019-2021: left LR in 2017, ran in the 2021 LR congress"),
    (2022, "Éric Ciotti"): ("LR", "", "suggested", ""),
    (2022, "Éric Zemmour"): ("EXD", "", "suggested", "polls of February-June 2021: as Wikipedia labels him until November 2021"),
    (2022, "[LR, candidat non désigné]"): ("LR", "", "label", "placeholder"),
    (2022, "[EELV, candidat non désigné]"): ("EELV", "", "label", "placeholder before the EELV primary"),
}


def row_label(raw, column) -> str | None:
    """The label in a Wikipedia row: 'Alain Juppé (UMP)' -> 'UMP'."""
    for text in (raw, column):
        m = re.search(r"\(([^()]+)\)\s*$", text) if isinstance(text, str) else None
        if m:
            return SPELLING.get(m.group(1), m.group(1))
    return None


def update(path: Path, polls: pd.DataFrame) -> pd.DataFrame:
    """Add a row for every candidate that needs one (some rows without a label) and return the file.
    `polls`: rows with election, candidate, candidate_raw, candidate_column, date."""
    existing = pd.read_csv(path, dtype=str, keep_default_na=False) if path.exists() else pd.DataFrame(columns=COLUMNS)
    have = set(zip(existing["election"].astype(int), existing["candidate"]))
    p = polls.assign(label=[row_label(a, b) for a, b in zip(polls["candidate_raw"], polls["candidate_column"])])
    new = []
    for (e, c), g in p.groupby(["election", "candidate"]):
        key = (int(e), c)
        n_unlabelled = g.loc[g["label"].isna(), "poll_id"].nunique()
        if key in have or not (n_unlabelled or key in INITIAL):
            continue
        labels = sorted(set(g["label"].dropna()))
        if key in INITIAL:
            party, override, match, note = INITIAL[key]
        elif len(labels) == 1:   # the candidate's only label elsewhere
            party, override, match, note = labels[0], "", "label", ""
        else:
            party, override, match, note = "", "", "", ""
        new.append(dict(election=int(e), candidate=c, labels="|".join(labels), party=party, override=override,
                        unlabelled_polls=n_unlabelled, match=match, note=note))
    out = pd.concat([existing, pd.DataFrame(new, columns=COLUMNS)], ignore_index=True)
    out["election"] = out["election"].astype(int)
    out = out.sort_values(["election", "candidate"])
    out.to_csv(path, index=False, encoding="utf-8-sig")
    return out


def assign(polls: pd.DataFrame, path: Path) -> pd.Series:
    """Party of every row: override, else the row's Wikipedia label, else the file's fallback."""
    f = pd.read_csv(path, dtype=str, keep_default_na=False)
    fallback = {(int(e), c): p for e, c, p in zip(f["election"], f["candidate"], f["party"]) if p}
    forced = {(int(e), c): p for e, c, p, o in zip(f["election"], f["candidate"], f["party"], f["override"])
              if p and o.strip().lower() == "yes"}
    out = []
    for e, c, raw, col in zip(polls["election"], polls["candidate"], polls["candidate_raw"], polls["candidate_column"]):
        key = (int(e), c)
        out.append(forced.get(key) or row_label(raw, col) or fallback.get(key, ""))
    return pd.Series(out, index=polls.index)
