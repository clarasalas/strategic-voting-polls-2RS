"""Compare the same polls across two sources (2002: france-politique vs Wikipedia;
2022: NSPPolls vs Wikipedia).

1. Polls are matched one-to-one on pollster and fieldwork dates (end dates at most
   `max_days` apart), closest pair first.
2. Within a matched pair, scenarios are paired by the overlap of their tested-candidate
   sets, then by how close their shares are.
3. Shares are compared candidate by candidate.
"""
from __future__ import annotations

import pandas as pd

from .candidates import OTHERS

# 2002: france-politique's CSA and SOFRES/LCI tables test "the Green candidate"
# (Mamère, Voynet or Lipietz); compare it with whichever Green the other source names.
ALIASES = {
    "Verts (Mamère/Voynet/Lipietz)": "Verts",
    "Noël Mamère": "Verts", "Dominique Voynet": "Verts", "Alain Lipietz": "Verts",
}


def _polls(df: pd.DataFrame) -> pd.DataFrame:
    p = df.drop_duplicates("poll_id")[["election", "source", "poll_id", "institute", "sponsor",
                                       "fieldwork_start", "fieldwork_end", "reported_date"]].copy()
    for c in ("fieldwork_start", "fieldwork_end", "reported_date"):
        p[c] = pd.to_datetime(p[c])
    p["end"] = p["fieldwork_end"].fillna(p["reported_date"])
    return p


def _share_gap(a: pd.DataFrame, b: pd.DataFrame) -> dict[tuple, float]:
    """Mean absolute share difference between two polls' first scenarios, per (poll_a, poll_b).
    Used only to break ties between polls by one pollster with identical dates
    (2002: Sofres for LCI and for Le Nouvel Observateur, both 27-28 March)."""
    def first(df):
        f = df[df["scenario_id"] == df["poll_id"] + "_s1"]
        f = f.assign(key=f["candidate"].map(lambda c: ALIASES.get(c, c)))
        return {pid: dict(zip(g["key"], g["share"])) for pid, g in f.dropna(subset=["share"]).groupby("poll_id")}
    return first(a), first(b)


def match_polls(a: pd.DataFrame, b: pd.DataFrame, max_days: int = 1) -> pd.DataFrame:
    """One row per poll of either source: matched pair, or only in one source."""
    pa, pb = _polls(a), _polls(b)
    pairs = pa.merge(pb, on=["election", "institute"], suffixes=("_a", "_b"))
    pairs["d_end"] = (pairs["end_a"] - pairs["end_b"]).dt.days.abs()
    pairs["d_start"] = (pairs["fieldwork_start_a"] - pairs["fieldwork_start_b"]).dt.days.abs().fillna(0)
    pairs = pairs[pairs["d_end"] <= max_days]
    fa, fb = _share_gap(a, b)

    def gap(x, y):
        sa, sb = fa.get(x, {}), fb.get(y, {})
        common = set(sa) & set(sb)
        return sum(abs(sa[k] - sb[k]) for k in common) / len(common) if common else 99.0
    pairs["gap"] = [gap(x, y) for x, y in zip(pairs["poll_id_a"], pairs["poll_id_b"])]
    pairs = pairs.sort_values(["d_end", "d_start", "gap"])

    used_a, used_b, rows = set(), set(), []
    for r in pairs.itertuples():
        if r.poll_id_a in used_a or r.poll_id_b in used_b:
            continue
        used_a.add(r.poll_id_a)
        used_b.add(r.poll_id_b)
        rows.append(dict(election=r.election, institute=r.institute, poll_id_a=r.poll_id_a, poll_id_b=r.poll_id_b,
                         end_a=r.end_a.date(), end_b=r.end_b.date(),
                         start_a=r.fieldwork_start_a, start_b=r.fieldwork_start_b,
                         status="matched" if r.d_end == 0 and r.d_start == 0 else "matched, dates differ"))
    for p, used, side in ((pa, used_a, "a"), (pb, used_b, "b")):
        for r in p[~p["poll_id"].isin(used)].itertuples():
            rows.append({"election": r.election, "institute": r.institute, f"poll_id_{side}": r.poll_id,
                         f"end_{side}": r.end.date() if pd.notna(r.end) else None,
                         f"start_{side}": r.fieldwork_start, "status": f"only in {side}"})
    out = pd.DataFrame(rows)
    for c in ("start_a", "start_b"):
        out[c] = pd.to_datetime(out[c]).dt.date
    return out.sort_values(["election", "institute", "end_a", "end_b"], na_position="last").reset_index(drop=True)


def _scenarios(df: pd.DataFrame) -> dict[str, dict[str, dict]]:
    """scenario_id -> {candidate key: {share, status, bound}}."""
    out: dict[str, dict] = {}
    for r in df.itertuples():
        key = ALIASES.get(r.candidate, r.candidate)
        if key == OTHERS:
            continue
        out.setdefault(r.scenario_id, {})[key] = dict(share=r.share, status=r.share_status,
                                                      bound=r.share_upper_bound, poll_id=r.poll_id)
    return out


def _tested(sc: dict) -> set:
    return {k for k, v in sc.items() if v["status"] != "not_tested"}


def compare_shares(a: pd.DataFrame, b: pd.DataFrame, matches: pd.DataFrame) -> pd.DataFrame:
    """One row per paired scenario x candidate with both sources' values and a verdict."""
    sa, sb = _scenarios(a), _scenarios(b)
    by_poll_a, by_poll_b = {}, {}
    for sid, sc in sa.items():
        by_poll_a.setdefault(next(iter(sc.values()))["poll_id"], []).append(sid)
    for sid, sc in sb.items():
        by_poll_b.setdefault(next(iter(sc.values()))["poll_id"], []).append(sid)

    rows = []
    for m in matches[matches["status"].str.startswith("matched")].itertuples():
        cand_pairs = []
        for x in by_poll_a.get(m.poll_id_a, []):
            for y in by_poll_b.get(m.poll_id_b, []):
                ta, tb = _tested(sa[x]), _tested(sb[y])
                jac = len(ta & tb) / max(1, len(ta | tb))
                common = [k for k in ta & tb if sa[x][k]["share"] == sa[x][k]["share"]
                          and sb[y][k]["share"] == sb[y][k]["share"]]
                gap = sum(abs(sa[x][k]["share"] - sb[y][k]["share"]) for k in common) / max(1, len(common))
                cand_pairs.append((-jac, gap, x, y))
        used_x, used_y = set(), set()
        for _, _, x, y in sorted(cand_pairs):
            if x in used_x or y in used_y:
                continue
            used_x.add(x)
            used_y.add(y)
            for k in sorted(_tested(sa[x]) | _tested(sb[y])):
                va, vb = sa[x].get(k), sb[y].get(k)
                rows.append(dict(election=m.election, institute=m.institute, poll_id_a=m.poll_id_a,
                                 poll_id_b=m.poll_id_b, scenario_a=x, scenario_b=y, candidate=k,
                                 share_a=va["share"] if va else None, status_a=va["status"] if va else "absent",
                                 share_b=vb["share"] if vb else None, status_b=vb["status"] if vb else "absent",
                                 verdict=_verdict(va, vb)))
        for x in set(by_poll_a.get(m.poll_id_a, [])) - used_x:
            rows.append(dict(election=m.election, institute=m.institute, poll_id_a=m.poll_id_a,
                             poll_id_b=m.poll_id_b, scenario_a=x, verdict="scenario only in a"))
        for y in set(by_poll_b.get(m.poll_id_b, [])) - used_y:
            rows.append(dict(election=m.election, institute=m.institute, poll_id_a=m.poll_id_a,
                             poll_id_b=m.poll_id_b, scenario_b=y, verdict="scenario only in b"))
    return pd.DataFrame(rows)


def _verdict(va, vb) -> str:
    for x, y, side in ((va, vb, "b"), (vb, va, "a")):
        if x is None or x["status"] == "not_tested":
            # absent on one side: only worth checking if the other side gives a number
            return f"candidate only in {side}" if y["status"] in ("value", "below_threshold") \
                else f"candidate only in {side}, without a share"
    sa_, sb_ = va["status"], vb["status"]
    if sa_ == sb_ == "value":
        return "equal" if abs(va["share"] - vb["share"]) < 0.01 else "differ"
    if sa_ == sb_:
        return "same status"
    for x, y in ((va, vb), (vb, va)):   # '<0,5 %' on one side, 0 or 0.5 on the other
        if x["status"] == "below_threshold" and y["status"] == "value" and y["share"] <= x["bound"]:
            return "compatible (threshold)"
    return "status differs"


def resolve_flags(thinned: pd.DataFrame, matches: pd.DataFrame, wiki_side: str) -> pd.DataFrame:
    """For Wikipedia polls flagged overlap_client_unknown, use the matched poll in the other
    source (which records the client) to say whether they are separate clients or a
    rolling release that thinning drops in the other source."""
    other = "b" if wiki_side == "a" else "a"
    flagged = thinned[thinned["overlap_client_unknown"] & (thinned["source"] == "wikipedia")]
    t = thinned.set_index("poll_id")
    m = matches.set_index(f"poll_id_{wiki_side}")
    rows = []
    for r in flagged.itertuples():
        if r.poll_id not in m.index or not str(m.at[r.poll_id, "status"]).startswith("matched"):
            if r.election in set(matches["election"]):
                rows.append(dict(election=r.election, poll_id=r.poll_id, institute=r.institute,
                                 resolution="no match in the other source: check by hand"))
            continue
        oid = m.at[r.poll_id, f"poll_id_{other}"]
        o = t.loc[oid]
        resolution = ("rolling release: dropped by thinning in the other source" if not o["kept"]
                      else "independent poll (kept in the other source)")
        rows.append(dict(election=r.election, poll_id=r.poll_id, institute=r.institute,
                         matched_poll=oid, other_series=o["series"], resolution=resolution))
    return pd.DataFrame(rows)


def describe_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """How to recognise each scenario of a poll in the original document.

    For every scenario: its position ('s2 of 3'), the source's own label if any, the
    candidates that set it apart from the poll's other scenarios ('with Pécresse;
    without Bertrand'), and its shares as parsed. A poll with one scenario gets 'only scenario'.
    """
    rows = []
    for pid, g in df.groupby("poll_id"):
        tested = {s: set(x.loc[x["share_status"] != "not_tested", "candidate"]) - {OTHERS}
                  for s, x in g.groupby("scenario_id")}
        common = set.intersection(*tested.values())
        everywhere = set.union(*tested.values())
        order = sorted(tested, key=lambda s: int(s.rsplit("_s", 1)[1]))
        for s in order:
            x = g[g["scenario_id"] == s]
            label = x["scenario_label"].dropna()
            if len(order) == 1:
                distinct = "only scenario"
            else:
                with_ = sorted(tested[s] - common)
                without = sorted(everywhere - tested[s])
                distinct = "; ".join(p for p in (f"with {', '.join(with_)}" if with_ else "",
                                                   f"without {', '.join(without)}" if without else "") if p) \
                    or "same candidates as another scenario"
            shares = " | ".join(
                f"{r.candidate} {r.share:g}" if r.share_status == "value"
                else f"{r.candidate} <{r.share_upper_bound:g}" if r.share_status == "below_threshold"
                else f"{r.candidate} ({r.share_status})"
                for r in x.sort_values("share", ascending=False).itertuples() if r.share_status != "not_tested")
            rows.append(dict(scenario_id=s, scenario=f"s{order.index(s) + 1} of {len(order)}",
                             scenario_label=label.iloc[0] if len(label) else "",
                             scenario_identified_by=distinct, shares=shares))
    return pd.DataFrame(rows).set_index("scenario_id")
