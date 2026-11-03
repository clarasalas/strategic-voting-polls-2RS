"""Which scenario of each poll corresponds to the final ballot, and whose slot each candidate fills.

A final-ballot candidacy is a candidate on the official first-round list. A tested candidate fills
its slot if it is the same person (Zemmour, SE in 2021, fills Zemmour's), or has the same party at
the time of the poll, allowing for renamings (Juppé, UMP in 2014, fills Fillon's LR slot). SE never
matches by party: unaffiliated candidates are not one party. Candidates from another party never
fill a slot, even if their party later backed that candidate (Bayrou for Macron in 2017).

A scenario is a ballot scenario when every final candidacy at or above REQUIRED_SHARE in the result
has its slot filled. It may also test candidates who will not be on the ballot ("extra", counted
with their total share): that is the poll voters saw. Among a poll's ballot scenarios, the one
chosen has the most slots filled by the same person, then the fewest extra candidates, then the
most final candidacies tested, then the lowest number.
"""
from __future__ import annotations

import pandas as pd

from .candidates import OTHERS

REQUIRED_SHARE = 2.0   # percent of the vote in the result

# A party's later names: the slot is the same organisation under a new name.
RENAMES = {
    "RPR": "UMP",     # 2002: the RPR merged into the UMP
    "UMP": "LR",      # May 2015
    "FN": "RN",       # June 2018
    "DLR": "DLF",     # October 2014
    "EM": "LREM",     # May 2017
    "LV": "EELV",     # November 2010: Les Verts became Europe Écologie Les Verts
    "LCR": "NPA",     # February 2009
}


def canon(party: str) -> str:
    """The latest name of a party: 'UMP' -> 'LR'."""
    seen = set()
    while party in RENAMES and party not in seen:
        seen.add(party)
        party = RENAMES[party]
    return party


def final_slots(polls: pd.DataFrame, results: pd.DataFrame) -> pd.DataFrame:
    """One row per final-ballot candidate: their party at the time of the election (their label in
    their last poll), its latest name, their result, and whether their slot is required."""
    tested = polls[polls["share_status"] != "not_tested"]
    last = (tested.sort_values("date").groupby(["election", "candidate"])["party"].last())
    out = results[["election", "candidate", "share"]].rename(columns={"share": "result"}).copy()
    out["party"] = [last.get((e, c), "") for e, c in zip(out["election"], out["candidate"])]
    out["party_canon"] = out["party"].map(canon)
    out["required"] = out["result"] >= REQUIRED_SHARE
    return out


def match(polls: pd.DataFrame, results: pd.DataFrame) -> tuple[pd.Series, pd.DataFrame]:
    """Returns (slot per row of `polls`, one row per scenario with the match details)."""
    slots = final_slots(polls, results)
    by_election = {e: g for e, g in slots.groupby("election")}
    slot_col = pd.Series("", index=polls.index)
    rows = []
    tested = polls[(polls["share_status"] != "not_tested") & (polls["candidate"] != OTHERS)]
    for sid, g in tested.groupby("scenario_id"):
        e = int(g["election"].iloc[0])
        final = by_election[e]
        person = set(final["candidate"])
        party_slot = {p: c for p, c in zip(final["party_canon"], final["candidate"]) if p and p != "SE"}
        filled, same_person, extra, extra_share = {}, 0, [], 0.0
        for i, r in g.iterrows():
            if r["candidate"] in person:
                slot = r["candidate"]
            else:
                slot = party_slot.get(canon(r["party"])) if r["party"] != "SE" else None
            if slot:
                slot_col.at[i] = slot
                filled.setdefault(slot, []).append(r["candidate"])
                same_person += r["candidate"] == slot
            else:
                extra.append(r["candidate"])
                extra_share += r["share"] if r["share_status"] == "value" else 0.0
        required = final.loc[final["required"], "candidate"]
        missing = [c for c in required if c not in filled]
        rows.append(dict(
            election=e, poll_id=g["poll_id"].iloc[0], scenario_id=sid, date=g["date"].iloc[0],
            ballot_scenario=not missing, missing_required="; ".join(missing),
            n_slots_filled=len(filled), n_same_person=same_person, n_final=len(final),
            n_extra=len(extra), extra_share=round(extra_share, 2), extra_candidates="; ".join(sorted(extra)),
            stand_ins="; ".join(f"{c} for {s}" for s, cs in sorted(filled.items()) for c in cs if c != s)))
    sc = pd.DataFrame(rows)
    sc["number"] = sc["scenario_id"].str.rsplit("_s", n=1).str[1].astype(int)
    ok = sc[sc["ballot_scenario"]].sort_values(
        ["poll_id", "n_same_person", "n_extra", "n_slots_filled", "number"],
        ascending=[True, False, True, False, True])
    chosen = set(ok.drop_duplicates("poll_id")["scenario_id"])
    sc["chosen"] = sc["scenario_id"].isin(chosen)
    return slot_col, sc.drop(columns="number").sort_values(["election", "date", "poll_id", "scenario_id"])
