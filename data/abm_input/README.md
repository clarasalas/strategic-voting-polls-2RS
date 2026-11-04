<h1 align="center">data/abm_input</h1>

<p align="center">
The poll input for the model's empirical mode, built from the validated dataset in the format
strategic-voting-abm-2RS reads. Prepared only: the model does not use it yet.
</p>

<p align="center"><sub><a href="../README.md">← Back to data</a></sub></p>

## What is in here

Written by `notebooks/07_parameters.ipynb` (section 6) with `src/polls/abm_input.py`.

| File | Window | Rolling releases |
|---|---|---|
| `polls_{year}.csv` | the model's current window: 1 March – 18 April 2002; 7 March (official list) – 8 April 2022 | thinned: each interview counted once |
| `polls_{year}_all_releases.csv` | same | every release, as voters saw them |
| `polls_{year}_12_weeks.csv` | the last 12 weeks before the first round | thinned |

To try one, copy it over the model's `data/polls_{year}.csv`. Against the model's current files, the weekly signal it
computes (ISO-week means, rescaled) differs by 0.01 to 0.07 points on average and at most 0.3 points
(`results/tables/abm_input_comparison.csv`).

<details>
<summary><strong>How the files are built</strong><br>From the final dataset to the model's parties</summary>

<br>

* Each poll's ballot scenario, from `data/final/polls.csv`.
* Candidates mapped to the model's parties through their slot (Juppé would count for LR) and the slot's party in
  the results.
* Extra candidates who will not be on the ballot dropped: the model rescales each poll.
* Below-threshold shares at half their bound, listed in `below_threshold`.
* A poll missing a modelled party would be dropped and listed in `polls_dropped.csv`; none is.
* `fieldwork` gives the fieldwork dates (ISO), not the published text.

</details>
