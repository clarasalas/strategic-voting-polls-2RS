"""Copy the links found with the link-search prompts into the two worklists.

Reads validation/link_search/found_<year>.csv (poll_id,url,source_type,matches,archive_url,notes),
keyed on the Wikipedia poll id, and fills in:
  crosscheck_disagreements.csv  matched on poll_id_wikipedia
  spot_check_sample.csv         matched on poll_id
Only empty document_url cells are filled, so links typed by hand are kept. Two extra columns,
link_check and link_notes, hold the link search's own verdict and notes.

Run from the repository root:  python -m polls.links   (with src/ on PYTHONPATH)
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from polls import worklists

ROOT = Path(__file__).resolve().parents[2]
VALIDATION = ROOT / "validation"
FOUND = VALIDATION / "link_search"
TARGETS = {"crosscheck_disagreements.csv": "poll_id_wikipedia", "spot_check_sample.csv": "poll_id"}


def read_found() -> pd.DataFrame:
    files = sorted(FOUND.glob("found_*.csv"))
    found = pd.concat([worklists.read(f) for f in files], ignore_index=True) if files else pd.DataFrame()
    if found.empty:
        return found
    found = found.apply(lambda c: c.str.strip())
    found = found.drop_duplicates("poll_id", keep="last").set_index("poll_id")
    ok = ~found["url"].str.lower().isin(["", "not_found"])
    found["link"] = found["url"].where(ok, "")
    found["check"] = (found["source_type"] + " / " + found["matches"]).str.strip(" /").where(ok, "not_found")
    archive = found.get("archive_url", pd.Series("", index=found.index))
    found["note"] = found["notes"] + ("" if archive is None else archive.map(lambda a: f" [archive: {a}]" if a else ""))
    return found


def apply(found: pd.DataFrame) -> None:
    for name, key in TARGETS.items():
        path = VALIDATION / name
        wl = worklists.read(path)
        for c in ("link_check", "link_notes"):
            if c not in wl:
                wl[c] = ""
        hit = wl[key].isin(found.index)
        ids = wl.loc[hit, key]
        empty = hit & (wl["document_url"] == "")
        wl.loc[empty, "document_url"] = wl.loc[empty, key].map(found["link"])
        wl.loc[hit, "link_check"] = ids.map(found["check"]).values
        wl.loc[hit, "link_notes"] = ids.map(found["note"]).values
        wl.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"{name}: {hit.sum()} rows matched, {(wl.loc[hit, 'document_url'] != '').sum()} with a link")
    unknown = set(found.index) - set().union(*(set(worklists.read(VALIDATION / n)[k]) for n, k in TARGETS.items()))
    if unknown:
        print(f"WARNING: {len(unknown)} poll_ids in found_*.csv match no worklist row: {sorted(unknown)}")


if __name__ == "__main__":
    apply(read_found())
