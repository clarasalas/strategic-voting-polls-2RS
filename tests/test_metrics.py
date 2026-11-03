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


def test_tied_candidates_share_a_role_and_the_cliff_is_zero():
    s = pd.Series({"A": 30.0, "B": 20.0, "C": 20.0, "D": 10.0})
    assert metrics.roles(s).to_dict() == {"A": "leader", "B": "2nd", "C": "2nd", "D": "other"}
    st = metrics.structure(s)
    assert st["cliff"] == 0.0 and st["gap_12"] == 10.0 and st["gap_34"] == 10.0
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
