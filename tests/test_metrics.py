import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from polls import metrics, timeline  # noqa: E402


def test_hhi_of_equal_shares_is_one_over_n():
    assert metrics.hhi([25, 25, 25, 25]) == pytest.approx(0.25)
    assert metrics.enp([25, 25, 25, 25]) == pytest.approx(4.0)


def test_rescaled_hhi_ignores_the_total_raw_does_not():
    assert metrics.hhi([40, 40]) == pytest.approx(0.5)
    assert metrics.hhi([40, 40], rescale=False) == pytest.approx(0.32)


def test_enp_matches_the_abm_formula():
    s = np.array([31.0, 26.5, 17.0, 12.5, 13.0])
    abm = 1.0 / ((s / s.sum()) ** 2).sum()   # core_model.metrics.enp
    assert metrics.enp(s) == pytest.approx(abm, abs=1e-12)


def test_tied_candidates_share_a_role_and_their_gap_is_zero():
    s = pd.Series({"A": 30.0, "B": 20.0, "C": 20.0, "D": 10.0})
    assert metrics.roles(s).to_dict() == {"A": "leader", "B": "2nd", "C": "2nd", "D": "other"}
    st = metrics.structure(s)
    assert st["gap_23"] == 0.0 and st["gap_12"] == 10.0 and st["gap_34"] == 10.0
    assert st["n_in_contention"] == 2


def test_below_threshold_counts_half_its_bound():
    rows = pd.DataFrame({"candidate": ["A", "B", "C"], "share": [60.0, 40.0, np.nan],
                         "share_status": ["value", "value", "below_threshold"],
                         "share_upper_bound": [np.nan, np.nan, 0.5]})
    assert metrics.shares_of(rows).to_dict() == {"A": 60.0, "B": 40.0, "C": 0.25}


def test_phases_and_weeks():
    cal = pd.DataFrame({"first_round": [pd.Timestamp("2022-04-10")], "official_list": [pd.Timestamp("2022-03-07")]},
                       index=[2022])
    p = pd.DataFrame({"election": [2022] * 4, "date": ["2022-03-01", "2022-03-20", "2022-03-27", "2022-04-08"]})
    t = timeline.add_time(p, cal)
    assert t["days_before"].tolist() == [40, 21, 14, 2]
    assert t["weeks_before"].tolist() == [6, 3, 2, 1]
    assert t["phase"].tolist() == [timeline.PHASES[0], timeline.PHASES[1], timeline.PHASES[2], timeline.PHASES[2]]


def test_poll_average_of_constant_polls_is_that_constant():
    from polls import average
    days = np.arange(0, 60, 2)
    s = average.smooth(days, np.full(len(days), 20.0), np.array([10, 30]))
    assert s["mean"].tolist() == pytest.approx([20.0, 20.0]) and s["sd"].tolist() == pytest.approx([0.0, 0.0])


def test_poll_average_leaves_sparse_days_empty():
    from polls import average
    s = average.smooth(np.array([0.0]), np.array([20.0]), np.array([0, 200]), min_polls=3)
    assert s["mean"].isna().all()


def test_leave_one_out_ignores_the_poll_itself():
    from polls import average
    days = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    values = np.array([10.0, 10.0, 40.0, 10.0, 10.0])
    loo = average.leave_one_out(days, values, h=50, min_polls=1)
    assert loo[2] == pytest.approx(10.0)          # the outlier does not count for itself
    assert loo[0] > 10.0                          # but counts for the others


def test_cliff_matches_the_abm():
    rng = np.random.default_rng(0)
    for _ in range(50):
        s = rng.dirichlet(np.ones(9)) * 100
        # the ABM's _cliff_stats, copied
        srt = np.sort(s)[::-1]; drops = srt[:-1] - srt[1:]; idx = int(np.argmax(drops))
        rest = np.concatenate([drops[:idx], drops[idx + 1:]])
        expected = (idx + 1, drops[idx], drops[idx] / (drops[idx] + rest.mean()))
        assert metrics.cliff(s) == pytest.approx(expected)


def test_largest_cliff_and_gap_23():
    st = metrics.structure(pd.Series({"A": 30.0, "B": 28.0, "C": 12.0, "D": 10.0}))
    assert (st["cliff_location"], st["cliff"], st["gap_23"]) == (2, 16.0, 16.0)
    st = metrics.structure(pd.Series({"A": 40.0, "B": 20.0, "C": 18.0, "D": 16.0}))
    assert (st["cliff_location"], st["cliff"], st["gap_23"]) == (1, 20.0, 2.0)


def test_adaptive_average_fills_sparse_stretches():
    from polls import average
    days = np.array([0, 2, 4, 6, 90.0, 110.0, 130.0, 150.0])
    fixed = average.smooth(days, np.full(8, 10.0), np.array([120]))
    wide = average.smooth(days, np.full(8, 10.0), np.array([120]), adaptive_k=4)
    gone = average.smooth(days, np.full(8, 10.0), np.array([300]), adaptive_k=4)   # beyond max_h: empty
    assert gone["mean"].isna().all()
    assert fixed["mean"].isna().all() and wide["mean"].tolist() == pytest.approx([10.0]) and wide["sparse"].all()
