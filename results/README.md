<h1 align="center">results</h1>

<p align="center">
Every table and figure of the study. Each number in the main README comes from one of these tables.
</p>

<p align="center"><sub><a href="../README.md">← Back to the project</a></sub></p>

## Start here

`tables/stylized_facts.csv` gathers the main numbers in one table, one column per election, each row naming the
table it comes from: the patterns the model should reproduce, with 2002 and 2022 as the cases it replays and 2007,
2012 and 2017 as out-of-sample cases.

## Tables

All in `tables/`, written by the study notebooks. Shares in points, days counted before the first round.

| Prefix | Notebook | What the tables hold |
|---|---|---|
| `coverage_` | 05 | polls per election, pollster and week; candidates tested; sample sizes |
| `trajectories_` | 05 | the poll average of every candidate, week-to-week volatility, entries and withdrawals |
| `ranks_` | 05 | each candidate's rank per poll; share of polls with the real runoff pair; when the pair locks in |
| `pollsters_` | 05 | house effects (pollster × candidate) and herding by campaign phase |
| `noise_` | 05 | the effective sample size of single polls, against their reported bases |
| `structure_` | 06 | HHI, ENP, top-two share, cliff and gaps per poll, in the poll average, in the last polls and in the results |
| `concentration_decomposition` | 06 | the change in HHI split into voters moving and the offer changing, over the campaign and the last mile |
| `error_` | 06 | result − last two weeks of polls, by candidate and by role; each poll's error on a typical candidate; each company's final poll |
| `cliff_` | 06 | the 2nd–3rd gap at 8, 4 and 1 week, and how predictable the runoff pair was |
| `momentum_` | 06 | does a rise continue: during the campaign, and into the vote |
| `stylized_facts` | 06 | the main numbers of notebooks 05 and 06 together |
| `parameters_` | 07 | ρ<sub>s</sub>, θ, ρ<sub>π</sub>, transfers and tolerance, real-world ranges for the synthetic setup |
| `abm_input_comparison` | 07 | the prepared poll input against the model's current files |

## Figures

All in `figures/`, regenerated with the tables: static versions for reading the notebooks. The interactive page
([`docs/`](../docs/README.md)) draws its own from the same data. Candidates are coloured from left to right in the order of
Wikipedia's poll-table columns.

| Figure | Notebook | What it shows |
|---|---|---|
| `coverage_polls_per_week.png` | 05 | polls per week before the first round |
| `trajectories.png` | 05 | poll average of the six leading candidates over the last 250 days, with the results |
| `ranks.png` | 05 | their ranks, and when the runoff pair stops changing |
| `pollsters_house_effects.png` | 05 | house effects by pollster and candidate |
| `structure_over_campaign.png` | 06 | HHI, top-two share, cliff and gaps over the campaign |
| `concentration_all_vs_core.png` | 06 | HHI over every candidate tested against the core candidates |
| `error_left_right.png` | 06 | result − polls for every candidate, left to right |
| `momentum_into_the_vote.png` | 06 | the last month's trend against the last mile |
| `parameters_theta.png` | 07 | polls against results, log scales: θ |
| `parameters_transfers.png` | 07 | where a candidate's voters go when the candidate is not offered |
| `parameters_real_ranges.png` | 07 | real polls and results against the synthetic setup |

<details>
<summary><strong>Reading the tables</strong><br>Conventions shared by every table</summary>

<br>

* **Polls** are each poll's ballot scenario unless a table says otherwise, with every candidate it tests (what
  voters saw). *Core* means the final candidacies with at least 2% of the vote.
* **Shares** are rescaled to 100; columns marked *raw* use shares as published, which can sum below 100 in 2007 and
  2012.
* **Poll average**: Gaussian kernel, 10-day bandwidth, at least 3 polls nearby. Statistics use it strictly; only the
  figures widen the window where polls are sparse.
* **Last polls**: the last two weeks before the vote. **Roles** (1st, 2nd…) come from the poll average, not single
  polls; tied candidates share a role.
* **HHI** is rescaled (= 1 / ENP, as in the model); the cliff is the model's largest drop between sorted shares.

Definitions in [`docs/study_plan.md`](../docs/study_plan.md) and `src/polls/metrics.py`.

</details>
