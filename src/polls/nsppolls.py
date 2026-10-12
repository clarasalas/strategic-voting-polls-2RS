"""Parse NSPPolls presidentielle.json (2022): poll -> tour -> hypothese -> candidat.

Only 'Premier tour' is kept. Each hypothesis is a scenario; its label is kept in
scenario_label. Entries with no candidate name but a party (e.g. « ext. gauche ») get
candidate_raw '[<party>]'.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from .textparse import ParseError

COMMISSION_DOMAIN = "commission-des-sondages.fr"


def _date(s):
    return date.fromisoformat(s) if s else None


def parse_file(path: Path) -> tuple[list[dict], list[dict]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rows, errors = [], []
    for p in data:
        first = [t for t in p["tours"] if t["tour"] == "Premier tour"]
        if not first:
            continue
        link = p.get("lien") or None
        try:
            start, end = _date(p["debut_enquete"]), _date(p["fin_enquete"])
        except ValueError as e:
            errors.append(dict(source="nsppolls", election=2022, location=p["id"],
                               raw=f"{p['debut_enquete']} / {p['fin_enquete']}", reason=str(e)))
            start = end = None
        base = dict(
            election=2022, source="nsppolls", institute=p["nom_institut"], sponsor=p.get("commanditaire") or None,
            fieldwork_start=start, fieldwork_end=end, publication_date=None, reported_date=None,
            date_raw=f"{p['debut_enquete']} / {p['fin_enquete']}",
            sample_size=p.get("echantillon"), population_base=p.get("population") or None,
            mode=None, panel=None, rolling=p.get("rolling"),
            upstream_source_url=link if link and COMMISSION_DOMAIN not in link else None,
            notice_url=link if link and COMMISSION_DOMAIN in link else None,
            wiki_revision_id=None, table_label=None, source_poll_ref=p["id"], page_poll_no=p["id"],
        )
        k = 0
        for tour in first:
            for h in tour["hypotheses"]:
                k += 1
                for c in h["candidats"]:
                    name = c.get("candidat")
                    if not name:
                        parties = ", ".join(c.get("parti") or [])
                        if not parties:
                            errors.append(dict(source="nsppolls", election=2022, location=f"{p['id']} {h['hypothese']}",
                                               raw=json.dumps(c, ensure_ascii=False), reason="no candidate and no party"))
                            continue
                        name = f"[{parties}]"
                    v = c.get("intentions")
                    rows.append({
                        **base, "effective_base": h.get("sous_echantillon"),
                        "scenario_no": k, "scenario_label": h.get("hypothese"),
                        "candidate_raw": name, "candidate_column": None, "name_hint": None,
                        "share": float(v) if v is not None else None,
                        "share_status": "value" if v is not None else "missing", "share_upper_bound": None,
                    })
    return rows, errors
