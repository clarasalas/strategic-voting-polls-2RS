"""Party of each candidate, through the hand-editable config/parties.csv.

One row per (election, candidate). Parties are named as in the official results (today's names:
RN, RE, LFI...), so a candidate tested before nomination counts for the party whose slot they
would fill on the ballot (Juppé and Sarkozy for LR in 2017).

`match` says how a row was filled: "results" (on the ballot: the official label), "label" (the
Wikipedia label, renamed to the ballot's name where needed), "suggested" (a proposal to check),
"manual" (checked or written by hand). Rows already in the file are never changed, so hand edits
persist; new candidates are added, filled where possible.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

COLUMNS = ["election", "candidate", "labels", "party", "on_ballot", "match", "note"]

# Initial fill for candidates not on the final ballot: (election, candidate) -> (party, match, note).
INITIAL = {
    # 2002
    (2002, "Antoine Waechter"): ("MEI", "suggested", "Mouvement écologiste indépendant; not on the ballot"),
    (2002, "Charles Pasqua"): ("RPF", "label", "withdrew before the official list"),
    (2002, "Dieudonné M'Bala M'Bala"): ("SE", "suggested", "no label; independent, not on the ballot"),
    (2002, "Dominique Voynet"): ("LV", "label", "Green candidate before Mamère"),
    (2002, "Philippe de Villiers"): ("MPF", "label", "did not run"),
    (2002, "Pierre Larrouturou"): ("SE", "suggested", "no label; affiliation in 2002 to check"),
    # 2007
    (2007, "François Hollande"): ("PS", "label", "before the PS nomination"),
    (2007, "Jack Lang"): ("PS", "label", "before the PS nomination"),
    (2007, "Laurent Fabius"): ("PS", "label", "before the PS nomination"),
    (2007, "Nicolas Hulot"): ("SE", "label", "did not run"),
    (2007, "Noël Mamère"): ("VERTS", "label", "Green candidate before Voynet (label LV)"),
    # 2012
    (2012, "Arlette Laguiller"): ("LO", "label", "before Arthaud"),
    (2012, "Bernard Tapie"): ("PRG", "label", "did not run"),
    (2012, "Christine Boutin"): ("PCD", "label", "withdrew"),
    (2012, "Corinne Lepage"): ("CAP21", "label", "not on the ballot"),
    (2012, "Cécile Duflot"): ("EELV", "label", "before the EELV primary"),
    (2012, "Dominique Strauss-Kahn"): ("PS", "label", "before the PS primary"),
    (2012, "Dominique Voynet"): ("EELV", "label", "before the EELV primary"),
    (2012, "Dominique de Villepin"): ("RS", "label", "not on the ballot"),
    (2012, "Frédéric Nihous"): ("CPNT", "label", "did not run"),
    (2012, "Gérard Schivardi"): ("PT", "label", "did not run"),
    (2012, "Hervé Morin"): ("NC", "label", "withdrew"),
    (2012, "Jean-Louis Borloo"): ("PR", "label", "did not run"),
    (2012, "Jean-Marie Le Pen"): ("FN", "suggested", "no label; FN before Marine Le Pen took over (January 2011)"),
    (2012, "Jean-Pierre Chevènement"): ("MRC", "label", "withdrew"),
    (2012, "José Bové"): ("EELV", "suggested", "label SÉ; tested as a possible EELV candidate"),
    (2012, "Marie-George Buffet"): ("FI", "suggested", "PCF, part of the Front de gauche behind Mélenchon (FI in the results)"),
    (2012, "Martine Aubry"): ("PS", "label", "before the PS primary"),
    (2012, "Nicolas Hulot"): ("EELV", "label", "before the EELV primary"),
    (2012, "Olivier Besancenot"): ("NPA", "label", "before Poutou"),
    (2012, "Philippe de Villiers"): ("MPF", "label", "did not run"),
    (2012, "Ségolène Royal"): ("PS", "label", "before the PS primary"),
    (2012, "[EELV, candidat non désigné]"): ("EELV", "label", "placeholder before the EELV primary"),
    # 2017
    (2017, "Alain Juppé"): ("LR", "label", "LR primary (label LR or UMP)"),
    (2017, "Arnaud Montebourg"): ("PS", "label", "PS primary"),
    (2017, "Bruno Le Maire"): ("LR", "label", "LR primary"),
    (2017, "Charlotte Marchandise"): ("SE", "suggested", "no label; LaPrimaire.org, not on the ballot"),
    (2017, "Cécile Duflot"): ("EELV", "label", "EELV primary; EELV later backed Hamon"),
    (2017, "Eva Joly"): ("EELV", "label", "EELV later backed Hamon"),
    (2017, "François Bayrou"): ("MODEM", "label", "withdrew, backed Macron"),
    (2017, "François Hollande"): ("PS", "label", "did not run"),
    (2017, "Henri Guaino"): ("SE", "suggested", "no label; LR member running as an independent, not on the ballot"),
    (2017, "Jean-François Copé"): ("LR", "label", "LR primary (label UMP)"),
    (2017, "Manuel Valls"): ("PS", "label", "PS primary"),
    (2017, "Martine Aubry"): ("PS", "label", "did not run"),
    (2017, "Michèle Alliot-Marie"): ("SE", "suggested", "no label; independent bid, not on the ballot"),
    (2017, "Nicolas Hulot"): ("SE", "suggested", "no label; did not run"),
    (2017, "Nicolas Sarkozy"): ("LR", "label", "LR primary (label LR or UMP)"),
    (2017, "Olivier Besancenot"): ("NPA", "label", "before Poutou"),
    (2017, "Philippe de Villiers"): ("MPF", "label", "did not run"),
    (2017, "Pierre Larrouturou"): ("ND", "suggested", "no label; Nouvelle Donne"),
    (2017, "Rama Yade"): ("SE", "suggested", "no label; La France qui ose, not on the ballot"),
    (2017, "Sylvia Pinel"): ("PRG", "label", "PS primary; PRG later backed Hamon"),
    (2017, "Vincent Peillon"): ("PS", "label", "PS primary"),
    (2017, "Yannick Jadot"): ("EELV", "label", "withdrew, backed Hamon"),
    # 2022
    (2022, "Arnaud Montebourg"): ("DVG", "suggested", "label DVG or PS; ran outside the PS, withdrew"),
    (2022, "Benoît Hamon"): ("G.s", "label", "did not run"),
    (2022, "Bernard Cazeneuve"): ("PS", "suggested", "no label; tested as an alternative PS-side candidate"),
    (2022, "Bruno Retailleau"): ("LR", "suggested", "no label; LR nomination contender"),
    (2022, "Christiane Taubira"): ("DVG", "label", "withdrew; not the PS candidate"),
    (2022, "Denis Payre"): ("LR", "suggested", "no label; LR congress candidate"),
    (2022, "Florian Philippot"): ("LP", "label", "not on the ballot"),
    (2022, "François Asselineau"): ("UPR", "label", "not on the ballot"),
    (2022, "François Baroin"): ("LR", "suggested", "no label; possible LR candidate"),
    (2022, "François Fillon"): ("LR", "suggested", "no label"),
    (2022, "François Hollande"): ("PS", "suggested", "no label"),
    (2022, "Hélène Thouy"): ("PA", "label", "not on the ballot"),
    (2022, "Jacques Cheminade"): ("SP", "label", "not on the ballot"),
    (2022, "Jean-Christophe Lagarde"): ("UDI", "label", "withdrew, backed Pécresse"),
    (2022, "Jean-Frédéric Poisson"): ("VIA", "label", "withdrew, backed Zemmour"),
    (2022, "Laurent Wauquiez"): ("LR", "suggested", "no label; possible LR candidate"),
    (2022, "Michel Barnier"): ("LR", "suggested", "no label; LR congress candidate"),
    (2022, "Olivier Faure"): ("PS", "suggested", "no label; PS first secretary"),
    (2022, "Philippe Juvin"): ("LR", "suggested", "no label; LR congress candidate"),
    (2022, "Rachida Dati"): ("LR", "suggested", "no label"),
    (2022, "Sandrine Rousseau"): ("EELV", "label", "EELV primary"),
    (2022, "Ségolène Royal"): ("PS", "suggested", "no label; former PS candidate, considered an independent bid"),
    (2022, "Xavier Bertrand"): ("LR", "suggested", "no label; left LR in 2017, ran in the LR congress in 2021"),
    (2022, "[EELV, candidat non désigné]"): ("EELV", "label", "placeholder before the EELV primary"),
    (2022, "[LR, candidat non désigné]"): ("LR", "suggested", "placeholder before the LR congress"),
    (2022, "[PS, candidat non désigné]"): ("PS", "suggested", "placeholder"),
    (2022, "[PS/DVG, candidat non désigné]"): ("PS", "suggested", "placeholder for the PS or an ally"),
    (2022, "[extrême gauche, candidat non désigné]"): ("NPA", "suggested", "placeholder; label NPA"),
    (2022, "Éric Ciotti"): ("LR", "suggested", "no label; LR congress candidate"),
    (2022, "Éric Piolle"): ("EELV", "label", "EELV primary"),
}


def _label(text) -> str | None:
    m = re.search(r"\(([^()]+)\)\s*$", text) if isinstance(text, str) else None
    return m.group(1) if m else None


def labels_seen(polls: pd.DataFrame) -> pd.Series:
    """(election, candidate) -> 'LR|UMP': the party labels Wikipedia gives the candidate."""
    lab = polls[["election", "candidate", "candidate_raw", "candidate_column"]].drop_duplicates()
    lab = lab.assign(label=[_label(a) or _label(b) for a, b in zip(lab["candidate_raw"], lab["candidate_column"])])
    return lab.groupby(["election", "candidate"])["label"].agg(lambda x: "|".join(sorted(set(x.dropna()))))


def update(path: Path, polls: pd.DataFrame, results: pd.DataFrame, extra=()) -> pd.DataFrame:
    """Add missing (election, candidate) rows to the file and return it. Existing rows are kept.
    `extra`: more (election, candidate) pairs, e.g. candidates added from another source."""
    existing = pd.read_csv(path, dtype=str, keep_default_na=False) if path.exists() else pd.DataFrame(columns=COLUMNS)
    have = set(zip(existing["election"].astype(int), existing["candidate"]))
    ballot = {(int(e), c): p for e, c, p in zip(results["election"], results["candidate"], results["party"])}
    labels = labels_seen(polls).to_dict()
    for e, c in extra:
        labels.setdefault((int(e), c), "")
    new = []
    for (e, c), lab in sorted(labels.items()):
        if (int(e), c) in have:
            continue
        if (int(e), c) in ballot:
            party, match, note = ballot[(int(e), c)], "results", ""
        else:
            party, match, note = INITIAL.get((int(e), c), ("", "", ""))
        new.append(dict(election=int(e), candidate=c, labels=lab, party=party,
                        on_ballot=(int(e), c) in ballot, match=match, note=note))
    out = pd.concat([existing, pd.DataFrame(new, columns=COLUMNS)], ignore_index=True)
    out["election"] = out["election"].astype(int)
    out = out.sort_values(["election", "on_ballot", "candidate"], ascending=[True, False, True])
    out.to_csv(path, index=False, encoding="utf-8-sig")
    return out


def load(path: Path) -> dict[tuple[int, str], str]:
    """(election, candidate) -> party, for the filled rows."""
    p = pd.read_csv(path, dtype=str, keep_default_na=False)
    return {(int(e), c): party for e, c, party in zip(p["election"], p["candidate"], p["party"]) if party}
