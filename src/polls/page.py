"""Build the interactive page, docs/index.html, from the final dataset and the study's tables.

    PYTHONPATH=src python -m polls.page

The page tells the story of the results (notebooks 05 and 06); the parameters (notebook 07) and
the data work are left to the READMEs. Every number on it comes from data/final/ or results/tables/,
recomputed here only where a table keeps a coarser version: the poll averages are drawn as in the
figures (the window widens where polls are sparse, drawn pale), every 2 days over the last 250.
The template, page_template.html, holds the text, the style and the charts; this module only
fills in the data, so the page is one standalone file.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import average, ideology, timeline

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "results" / "tables"
TEMPLATE = Path(__file__).with_name("page_template.html")
OUT = ROOT / "docs" / "index.html"
WINDOW = 250                      # days before the vote shown
GRID = np.arange(0, WINDOW + 1, 2)
ELECTION_COLOURS = ["#9e0142", "#f46d43", "#e09000", "#2a9d8f", "#5e4fa2"]   # as in notebook 06


def _hex(rgb) -> str:
    return "#" + "".join(f"{round(c * 255):02x}" for c in rgb)


def _r(x, n=2):
    """Rounded float, or None for NaN (JSON null)."""
    return None if x is None or pd.isna(x) else round(float(x), n)


def surname(name: str) -> str:
    return name.split(" ", 1)[1] if " " in name else name


def load():
    calendar = timeline.load(ROOT / "config" / "elections.yaml")
    rows = timeline.add_time(pd.read_csv(ROOT / "data" / "final" / "polls.csv", low_memory=False), calendar)
    results = pd.read_csv(ROOT / "data" / "interim" / "results.csv")
    ballot = rows[rows["ballot_scenario"] & (rows["share_status"] != "not_tested")].copy()
    ballot["value"] = np.where(ballot["share_status"] == "value", ballot["share"], ballot["share_upper_bound"] * 0.5)
    slot_polls = ballot.dropna(subset=["slot"]).groupby(["election", "poll_id", "slot"], as_index=False).agg(
        value=("value", "sum"), days_before=("days_before", "first"), date=("date", "first"),
        pollster=("institute_family", "first"))
    lr = ideology.order(ROOT, {int(p.name[:4]): p for p in (ROOT / "data" / "raw" / "wikipedia").glob("*.json")},
                        pd.read_csv(ROOT / "data" / "interim" / "polls_wikipedia.csv", low_memory=False))
    lr_pos = lr.set_index(["election", "candidate"])["position"]
    # candidates tested with the full ballot who will not be on it (they withdrew, or never stood)
    extra_polls = ballot[ballot["slot"].isna()].groupby(["election", "poll_id", "candidate"], as_index=False).agg(
        value=("value", "sum"), days_before=("days_before", "first"), party=("party", "first"))
    polls = rows.drop_duplicates("poll_id")[["election", "poll_id", "weeks_before"]].copy()
    polls["full_ballot"] = polls["poll_id"].isin(ballot["poll_id"])
    return calendar, rows, results, slot_polls, extra_polls, polls, lr_pos


def _colour_at(frac: float) -> str:
    """The left-right palette at a fraction of the way from left to right, darkened as in ideology.colours."""
    from matplotlib.colors import LinearSegmentedColormap
    rgb = list(LinearSegmentedColormap.from_list("left_right", ideology.LEFT_RIGHT)(frac)[:3])
    while ideology._luminance(rgb) > 0.35:
        rgb = [x * 0.95 for x in rgb]
    return _hex(rgb)


def withdrawn(e, extra_polls, lr_pos, final_order) -> list[dict]:
    """Candidates tested with the full ballot who were not on it, with at least 5 polls in the window and a poll
    average reaching 2%: their line, drawn only between their first and last poll. Coloured by their place
    among the final candidates on the left-right axis."""
    ep = extra_polls[(extra_polls["election"] == e) & (extra_polls["days_before"] <= WINDOW)]
    final_pos = sorted(lr_pos.get((e, c), 0.5) for c in final_order)
    out = []
    for c, g in ep.groupby("candidate"):
        if g["poll_id"].nunique() < 5:
            continue
        sm = average.smooth(g["days_before"].to_numpy(), g["value"].to_numpy(), GRID, adaptive_k=4).dropna()
        sm = sm[(sm.index >= g["days_before"].min()) & (sm.index <= g["days_before"].max())]
        if sm.empty or sm["mean"].max() < 2.0:
            continue
        frac = float(np.interp(lr_pos.get((e, c), 0.5), final_pos, np.linspace(0, 1, len(final_pos))))
        out.append(dict(name=c, short=surname(c), party=g["party"].iloc[0], result=None, colour=_colour_at(frac),
                        top6=False, withdrawn=True, last_poll=int(g["days_before"].min()),
                        traj=[[int(d), _r(m, 2), _r(sd, 2), int(sp_)] for d, m, sd, sp_ in
                              zip(sm.index, sm["mean"], sm["sd"], sm["sparse"])], rank=[]))
    return out


def table(name: str) -> pd.DataFrame:
    return pd.read_csv(TABLES / f"{name}.csv")


def election_block(e, calendar, rows, results, slot_polls, extra_polls, all_polls, lr_pos) -> dict:
    res = results[results["election"] == e].sort_values("share", ascending=False)
    cands = sorted(res["candidate"], key=lambda c: lr_pos.get((e, c), 0.5))
    colour = {c: _hex(rgb) for c, rgb in ideology.colours(cands).items()}
    top6 = set(res["candidate"].head(6))
    sp = slot_polls[slot_polls["election"] == e]
    traj = average.by_candidate(sp, "value", GRID, adaptive_k=4)
    ok = traj.dropna(subset=["mean"]).copy()
    ok["rank"] = ok.groupby("days_before")["mean"].rank(ascending=False, method="first")

    # party label at the time: the candidate's label in their last poll (the results file uses current names)
    tested = rows[(rows["election"] == e) & (rows["share_status"] != "not_tested")]
    party_then = tested.sort_values("date").groupby("candidate")["party"].last()
    candidates = []
    for c in cands:
        t = ok[ok["slot"] == c].sort_values("days_before")
        r = res.set_index("candidate").loc[c]
        candidates.append(dict(
            name=c, short=surname(c), party=party_then.get(c, r["party"]), result=_r(r["share"]), colour=colour[c], top6=c in top6,
            traj=[[int(d), _r(m, 2), _r(s, 2), int(sp_)] for d, m, s, sp_ in
                  zip(t["days_before"], t["mean"], t["sd"], t["sparse"])],
            rank=[[int(d), int(k)] for d, k in zip(t["days_before"], t["rank"])]))
    candidates += withdrawn(e, extra_polls, lr_pos, cands)

    shown = sp[sp["days_before"] <= WINDOW]
    index = {c["name"]: i for i, c in enumerate(candidates)}
    extra = extra_polls[(extra_polls["election"] == e) & extra_polls["candidate"].isin(index)].set_index("poll_id")
    polls = []
    for pid, g in shown.groupby("poll_id"):
        values = {index[s]: _r(v, 1) for s, v in zip(g["slot"], g["value"]) if s in index}
        if pid in extra.index:
            x = extra.loc[[pid]]
            values.update({index[c]: _r(v, 1) for c, v in zip(x["candidate"], x["value"])})
        polls.append([int(g["days_before"].iloc[0]), g["pollster"].iloc[0], str(g["date"].iloc[0])[:10], values])

    events = table("trajectories_entries_withdrawals").query("election == @e and days_before <= @WINDOW")
    cov = table("coverage_by_election").set_index("election").loc[e]
    ap = all_polls[all_polls["election"] == e]
    weekly = ap.groupby(["weeks_before", "full_ballot"]).size().unstack(fill_value=0)
    right = table("ranks_right_pair_by_phase").set_index("election").loc[e]
    lock = table("ranks_lockin").set_index("election").loc[e]
    pred = table("cliff_predictability").query("election == @e").set_index("horizon")
    vol = table("trajectories_volatility").set_index("election").loc[e]
    sr = table("structure_results").set_index("election").loc[e]
    last = _last_polls(e)

    err = table("error_by_candidate").query("election == @e").sort_values("position")
    house = table("pollsters_house_effects").query("election == @e")
    return dict(
        election=int(e), first_round=str(calendar.loc[e, "first_round"].date()),
        official_list=int((calendar.loc[e, "first_round"] - calendar.loc[e, "official_list"]).days),
        candidates=candidates, polls=sorted(polls, key=lambda p: -p[0]),
        events=[dict(kind=r.kind, name=surname(r.candidate), day=int(r.days_before)) for r in events.itertuples()],
        accuracy=dict(polls=[[r.institute, str(r.date)[:10], int(r.days_before), _r(r.rmse), surname(r.largest_miss),
                              _r(r.largest_miss_error)] for r in table("error_by_poll").query("election == @e").itertuples()],
                      average=_r(np.sqrt((err["error"].dropna() ** 2).mean()))),
        weekly=[[int(weekly.loc[w].get(True, 0)), int(weekly.loc[w].get(False, 0))] if w in weekly.index else [0, 0]
                for w in range(1, WINDOW // 7 + 1)],
        stats=dict(polls=int(cov["polls"]), pollsters=int(cov["pollsters"]), last_two_weeks=int(cov["last two weeks"]),
                   volatility_last=_r(vol["last two weeks"]),
                   right_pair_last=_r(right["last two weeks"]), right_leader_last=_r(right["1st place right, last two weeks"]),
                   locked_from=_r(lock["locked_from_days_before"], 0),
                   p_pair_1w=_r(pred.loc["1 week", "p_real_pair"], 3), p_pair_4w=_r(pred.loc["4 weeks", "p_real_pair"], 3),
                   gap_result=_r(sr["gap_23"]), gap_polls=_r(last.get("gap_23")),
                   second=surname(sr["second"]), third=surname(sr["third"])),
        errors=[dict(name=surname(r.slot), colour=colour.get(r.slot, "#888"), result=_r(r.result), polled=_r(r.polled),
                     error=_r(r.error), role=r.role) for r in err.itertuples() if pd.notna(r.error)],
        house=dict(pollsters=sorted(house["institute_family"].unique()),
                   candidates=[c["short"] for c in candidates if c["name"] in set(house["slot"])],
                   cells=[[r.institute_family, surname(r.slot), _r(r.house_effect), _r(r.se), int(r.polls), bool(r.significant)]
                          for r in house.itertuples()]))


def _last_polls(e) -> dict:
    """Mean structure of the last two weeks of polls (structure_last_polls_vs_result)."""
    t = pd.read_csv(TABLES / "structure_last_polls_vs_result.csv", header=[0, 1], index_col=0)
    return t.xs("last polls", axis=1, level=1).loc[e].to_dict()


def structure_block() -> dict:
    """Per-poll structure metrics, averaged over the campaign (widened window), and the results."""
    per_poll = table("structure_by_poll")
    sr = table("structure_results").set_index("election")
    out = {}
    for m in ["hhi", "top2_share", "cliff", "gap_23"]:
        series = {}
        for e, d in per_poll.groupby("election"):
            s = average.smooth(d["days_before"].to_numpy(), d[m].to_numpy(dtype=float), GRID, adaptive_k=4).dropna()
            series[int(e)] = dict(line=[[int(day), _r(v, 4), int(sp)] for day, v, sp in zip(s.index, s["mean"], s["sparse"])],
                                  result=_r(sr.loc[e, m], 4))
        out[m] = series
    return out


def build() -> Path:
    calendar, rows, results, slot_polls, extra_polls, all_polls, lr_pos = load()
    elections = sorted(int(e) for e in rows["election"].unique())
    dec = table("concentration_decomposition")
    momentum = table("momentum_into_the_vote")
    mom_c = table("momentum_campaign").set_index("sample").T
    roles = table("error_by_role")
    herd = table("pollsters_herding").query("phase == 'last two weeks'").set_index("election")
    noise = table("noise_effective_sample_size").query("period == 'last two weeks'").set_index("election")
    blocks = {e: election_block(e, calendar, rows, results, slot_polls, extra_polls, all_polls, lr_pos) for e in elections}
    data = dict(
        window=WINDOW, elections=elections, colours=dict(zip(map(str, elections), ELECTION_COLOURS)),
        blocks=blocks, structure=structure_block(),
        decomposition=[dict(election=int(r["election"]), campaign_voters=_r(r["campaign: voters (core)"], 3),
                            campaign_offer=_r(r["campaign: offer (composition)"], 3),
                            last_mile_voters=_r(r["last mile: voters (core)"], 3),
                            last_mile_total=_r(r["last mile: total"], 3)) for _, r in dec.iterrows()],
        roles=[dict(role=r.role, mean=_r(r.mean_error), better=int(r.did_better), worse=int(r.did_worse))
               for r in roles.itertuples()],
        momentum=dict(points=[dict(election=int(r.election), name=surname(r.slot), before=_r(r.before), after=_r(r.after),
                                   level=_r(r.level, 1)) for r in momentum.itertuples()],
                      slope=_r(np.polyfit(momentum["before"], momentum["after"], 1)[0]),
                      campaign=dict(slope=_r(mom_c.loc["slope", "all"]), low=_r(mom_c.loc["low", "all"]),
                                    high=_r(mom_c.loc["high", "all"]))),
        noise={int(e): dict(n_eff=_r(noise.loc[e, "n_eff"], 0), herding=_r(herd.loc[e, "ratio"])) for e in elections},
        final_polls=[dict(election=int(r.election), institute=r.institute, date=str(r.date)[:10], days=int(r.days_before),
                          rmse=_r(r.rmse), relative=_r(r.relative))
                     for r in table("error_final_poll_by_pollster").itertuples()],
    )
    html = TEMPLATE.read_text().replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    OUT.write_text(html)
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size / 1e3:.0f} kB)")
