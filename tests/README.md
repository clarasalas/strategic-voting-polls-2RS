<h1 align="center">tests</h1>

<p align="center">
Checks of the formulas the study rests on: concentration, the cliff, roles, the time axis and the poll average.
</p>

<p align="center"><sub><a href="../README.md">← Back to the project</a></sub></p>

## Run them

```bash
python -m pytest tests
```

12 tests, in under a second. They need only the packages in `requirements.txt`, not the data.

## What they check

| Question | Tests |
|---|---|
| **Do the metrics match their definitions?** HHI of equal shares, rescaled against raw HHI, below-threshold shares at half their bound | `test_hhi_of_equal_shares_is_one_over_n`, `test_rescaled_hhi_ignores_the_total_raw_does_not`, `test_below_threshold_counts_half_its_bound` |
| **Do they match the model?** ENP and the cliff computed as in strategic-voting-abm-2RS | `test_enp_matches_the_abm_formula`, `test_cliff_matches_the_abm`, `test_largest_cliff_and_gap_23` |
| **Are ties handled?** Tied candidates share a role, with a gap of 0 | `test_tied_candidates_share_a_role_and_their_gap_is_zero` |
| **Is the time axis right?** Days before the vote, weeks and campaign phases | `test_phases_and_weeks` |
| **Does the poll average behave?** Constant polls, sparse days left empty, leave-one-out, the widened window of the figures | `test_poll_average_of_constant_polls_is_that_constant`, `test_poll_average_leaves_sparse_days_empty`, `test_leave_one_out_ignores_the_poll_itself`, `test_adaptive_average_fills_sparse_stretches` |

The parsing and the validation are checked differently: by the consistency reports of notebook 01
(`src/polls/checks.py`), by comparing two sources in notebook 03, and by hand against the original documents
([`validation/`](../validation/README.md)).
