<h1 align="center">French presidential polls, 2002–2022</h1>

<p align="center">
Every first-round poll of the five French presidential elections from 2002 to 2022, checked against the original
documents, and what they say about how voters coordinate before the vote.
</p>

<p align="center">
  <a href="https://clarasalas.github.io/strategic-voting-polls-2RS/">
    <img src="https://img.shields.io/badge/Open%20the%20interactive%20page-1a1a1a?style=for-the-badge" alt="Open the interactive page">
  </a>
</p>

<p align="center">
The interactive page tells the story of the five campaigns: every candidate's poll average and polls, who seemed
headed for the runoff, who gained in the last weeks, how concentrated the vote was, and how pollsters differed.
</p>

## About

In a two-round election, voters who expect their preferred candidate to be eliminated can move to a candidate with a
real chance of reaching the runoff. What they expect comes largely from the polls. This project builds a validated
dataset of the first-round polls of 2002, 2007, 2012, 2017 and 2022, and studies it: how accurate the polls are, how
much coordination they show, and toward whom.

It is the poll side of [strategic-voting-abm-2RS](https://github.com/clarasalas/strategic-voting-abm-2RS), an
agent-based model of voters who switch to a compromise candidate when nobody they can tolerate looks likely to reach
the runoff. The model reads polls as its voters' information; this project describes what real polls looked like, and
gives realistic ranges for the model's poll parameters. Nothing here runs the model. A companion project,
[strategic-voting-geo-2RS](https://github.com/clarasalas/strategic-voting-geo-2RS), maps where the vote concentrated.

**The data.** The polls come from the French Wikipedia lists of polls, at fixed revisions, with france-politique.fr
for 2002 and NSPPolls for 2022 as second sources. Rolling polls are thinned so that each interview counts once. Where
two sources cover the same poll they are compared share by share, and every disagreement was settled by hand against
the pollster's report or the Commission des sondages notice; a random sample of 30 polls per election was checked
the same way. The result, `data/final/polls.csv`, holds 693 polls and 1,149 scenarios, with 136 corrections applied.

**What is measured.** Each poll is read through its *ballot scenario*: the hypothesis that tests every candidate who
will win at least 2% of the vote, as voters saw it. Concentration is the Herfindahl–Hirschman index (HHI, the sum of
squared shares; 1/HHI is the effective number of candidates, ENP, as in the model). The *cliff* is the model's: the
largest drop between consecutive sorted shares. The runoff is decided by the gap between the 2nd and the 3rd.

Polls are not voters' expectations, and the result is not the polls' target: it also contains the late switching
the model is meant to produce. A gap between the last polls and the result therefore mixes poll error and real late
movement, which these data cannot separate. All results are descriptive, over five elections.

## Main findings

**When the 2nd and the 3rd are far apart, the polls name the runoff pair months ahead; when they are close, the polls
cannot.** In the last two weeks, every poll had the real runoff pair as its top two in 2007, 2012 and 2022, 95% in
2017, none in 2002. In the poll average, the pair stopped changing about 200 days before the vote in 2007 and 2012,
and about 90 days before in 2017 and 2022. It never settled in 2002, when Le Pen finished 0.7 points ahead of Jospin.

<details>
<summary>Supporting evidence: the gap for qualification and how predictable the pair was</summary>

<br>

* **Close results, wider polls.** The gap between the 2nd and the 3rd was 0.7 points in the 2002 result, 1.3 in 2017
  and 1.2 in 2022. The last two weeks of polls had put it at 5.3, 3.0 and 6.0 points.
* **How likely the polls made the real pair, one week before**, allowing for the typical poll error of the other four
  elections: 4% in 2002, 72% in 2017, 94% in 2007, 98% in 2022, almost 100% in 2012. A rough gauge, not a forecast
  model (candidates' errors drawn independently).
* **The leader** was right in every poll of the last two weeks in 2002, 2007 and 2022, in 91% in 2017 and 67% in
  2012 (Hollande and Sarkozy about a point apart).

Tables: `ranks_right_pair_by_phase.csv`, `ranks_lockin.csv`, `cliff_predictability.csv`,
`structure_last_polls_vs_result.csv`.

</details>

**Near the threshold, the result tilts toward the candidate polled 3rd and away from the 4th.** The candidate 3rd in
the last two weeks of polls did at least as well as polled in all five elections, by 2.6 points on average (Le Pen
+4.2 in 2002, Mélenchon +5.8 in 2022); the 4th did worse in four of five, by 2.1 points on average. This is the
direction the model's mechanism predicts, voters leaving a candidate out of reach for one within reach of the runoff,
but it is also what a poll bias would produce: the two cannot be told apart here.

<details>
<summary>Supporting evidence: error by role and overall accuracy</summary>

<br>

| Role in the last polls | Mean error (points) | Did better | Did worse |
|---|---|---|---|
| 1st | +0.9 | 4 | 1 |
| 2nd | 0.0 | 3 | 2 |
| 3rd | +2.6 | 5 | 0 |
| 4th | −2.1 | 1 | 4 |
| 5th and below | −0.2 | 19 | 22 |

Error = result − mean of the last two weeks of polls; roles come from that mean. The mean absolute error for the
candidates polled at 5% or more is 1.0 to 2.5 points per election. Tables: `error_by_role.csv`,
`error_by_candidate.csv`.

</details>

**The vote concentrates at the end, not over the campaign.** Within a fixed set of candidates, the polls spread out
over the campaign in 2002, 2007, 2012 and 2017 (HHI down by 0.01 to 0.04 from the opening polls to the last ones);
the rises in 2012 and 2022 come mostly from the offer narrowing, as candidates withdrew. Between the last polls and the result, the vote
concentrates in all five elections, by voters moving, most in 2007 and 2022 (HHI +0.016 and +0.020). 2002 is the
most fragmented result by far: 8.7 effective candidates, against 4.7 to 5.3 in the other four.

<details>
<summary>Supporting evidence: splitting the change in concentration</summary>

<br>

HHI is computed twice for every ballot poll and for the result: over every candidate tested, and over the *core*,
the candidates who will win at least 2%, rescaled among themselves. The core is the same set throughout, so its
changes are voters moving; the difference between the two is the offer (candidates tested, then withdrawing).

| | 2002 | 2007 | 2012 | 2017 | 2022 |
|---|---|---|---|---|---|
| Campaign: voters (core) | −0.032 | −0.041 | −0.020 | −0.009 | +0.006 |
| Campaign: offer | +0.004 | −0.002 | +0.042 | +0.006 | +0.020 |
| Last mile: voters (core) | +0.002 | +0.011 | +0.007 | +0.001 | +0.020 |

Table: `concentration_decomposition.csv`. Figure: `results/figures/structure_over_campaign.png`.

</details>

**Single polls are about as precise as random samples of one to two thousand people, house effects are small, and
movement partly carries on.** In the last two weeks, the scatter of single polls around the poll average is what
simple random samples of 860 to 1,800 people would give. Pollsters' house effects are typically 0.3 to 0.5 points, at most
about 2. A rise in the poll average over three weeks is followed by a further rise of about 0.4 times as much over the
next three.

<details>
<summary>Supporting evidence: noise, herding, house effects and momentum</summary>

<br>

* **Herding.** Polls agreed more than sampling allows in the last two weeks of 2017 (scatter 0.73 of sampling noise),
  and much less in 2022 (2.1). Against the bases they report (given only from 2017), polls were slightly more precise
  than their samples in 2017 and about half as precise in 2022.
* **House effects** (pollster × candidate, against the leave-one-out poll average): largest for Cluster17 on
  Mélenchon in 2022 (+2.2) and CSA on Le Pen and Sarkozy in 2007 (+2.2, −2.1).
* **Momentum.** Pooled slope 0.40 (95% interval 0.29–0.53), from 0.27 to 0.55 per election, with 2002 alone near 1
  and very uncertain. The trend of the last month also carries on into the result (slope 0.62 over 33 candidates).

Tables: `noise_effective_sample_size.csv`, `pollsters_herding.csv`, `pollsters_house_effects.csv`,
`momentum_campaign.csv`, `momentum_into_the_vote.csv`.

</details>

**Real polls are much less noisy than the model's synthetic polls, and about as steep as the results.** The model
draws synthetic polls with a noise ρ<sub>s</sub> between 10 and 200 and a temperature θ between 0.3 and 3. Single
real polls correspond to ρ<sub>s</sub> of about 500 to 1,800, and θ comes out at 0.94 to 1.12. Real polls test 9 to
16 candidates (median 12), against 6, 8 and 9 in the synthetic runs.

<details>
<summary>Supporting evidence: the model's parameters</summary>

<br>

* **Poll noise ρ<sub>s</sub>.** 490 to 880 for single polls over the campaign, 860 to 1,810 in the last two weeks. A
  lower bound, the poll average a week out against the result (noise, common bias and late movement together), gives
  105 to 730: only the top of the current range reaches it.
* **Temperature θ**, two ways: candidate by candidate (0.94 to 1.12) and from the slope of shares by rank (0.95 to
  1.08). Polls neither sharpen nor flatten the result much, though the result itself contains late switching.
* **Prior spread ρ<sub>π</sub>**, how much the opening polls disagree: 290 to 1,410. An upper bound: voters' beliefs
  are surely more spread out than the polls they could read.
* **Tolerance τ̂.** Two hypotheses of the same poll that differ by one candidate show where that candidate's voters go
  when not offered. For candidates polling 3% or more, about half go to a neighbour on the left-right axis, and on
  average 1.8 to 2.6 places away, inside the model's range τ̂ ∈ [0.5, 3]. Few pairs outside Bayrou and Macron in
  2017 and Zemmour and Taubira in 2022.
* **α**, how far voters follow the latest poll, is left out: the mechanism will change, and survey data on
  expectations would measure it better than polls.

Tables: `parameters_*.csv`. A poll input for the model's empirical mode is prepared in
[`data/abm_input/`](data/abm_input/README.md), not used.

</details>

The study is in `notebooks/05_polls_descriptive.ipynb`, `06_polls_vs_results.ipynb` and `07_parameters.ipynb`; every
decision behind it is in [`docs/study_plan.md`](docs/study_plan.md), and every number above comes from a table in
[`results/tables/`](results/README.md).

## Reproduce

```bash
pip install -r requirements.txt
for nb in notebooks/0*.ipynb; do jupyter nbconvert --to notebook --execute --inplace "$nb"; done
PYTHONPATH=src python -m polls.page          # rebuilds the interactive page, docs/index.html
python -m pytest tests
```

The notebooks run in order, 01 to 07, each reading what the previous ones wrote (see
[`notebooks/`](notebooks/README.md)). Every source is pinned and the downloads are committed in `data/raw/`, so the
whole pipeline runs offline and gives the same tables; notebook 01 goes online only for a pin left blank in
`config/sources.yaml`. The hand-filled files, `config/*.csv` and the worklists in `validation/`, are never
overwritten by a rerun. The results were produced with Python 3.13. The interactive page is a single standalone
file, published with GitHub Pages from the `docs/` folder (see [`docs/README.md`](docs/README.md)).

<details>
<summary><strong>Repository layout</strong></summary>

<br>

```
config/          pinned sources, election dates, and the hand-editable name and party mappings
data/
  raw/           downloads exactly as received, never edited
  interim/       parsed tables, one per source, thinning and cross-check
  final/         the final dataset: polls, scenarios, corrections
  abm_input/     poll input for the model's empirical mode (prepared, not used)
validation/      worklists filled in by hand against the original documents
notebooks/       the pipeline (01–04) and the study (05–07)
src/polls/       the code the notebooks call: parsers, mappings, thinning, metrics, poll average
results/
  tables/        every table the study produces
  figures/       static versions of its figures
tests/           tests of the metrics and the time axis
docs/            the interactive page (generated), the study plan and its decisions
```

Each folder has its own README.

</details>

<details>
<summary><strong>Pipeline</strong></summary>

<br>

| Notebook | Reads | Writes |
|---|---|---|
| `01_collect_and_parse` | the sources (`config/sources.yaml`) | `data/raw/`, `data/interim/polls_*.csv`, `results.csv`, `parse_errors.csv` |
| `02_thin_rolling` | interim polls, `validation/flagged_clients.csv` | `data/interim/thinning.csv` |
| `03_cross_check` | interim polls, thinning | `data/interim/crosscheck_*.csv`, the worklists in `validation/` (once) |
| `04_final_dataset` | interim tables, filled worklists | `data/final/` |
| `05_polls_descriptive` | `data/final/polls.csv` | `results/tables/coverage_*`, `trajectories_*`, `ranks_*`, `pollsters_*`, `noise_*`, figures |
| `06_polls_vs_results` | final polls, results | `results/tables/structure_*`, `error_*`, `cliff_*`, `momentum_*`, `stylized_facts.csv`, figures |
| `07_parameters` | final polls, results | `results/tables/parameters_*`, `data/abm_input/`, figures |
| `python -m polls.page` | final polls, results, the tables of 05 and 06 | `docs/index.html` |

</details>

<details>
<summary><strong>Data sources</strong></summary>

<br>

* **Polls, 2002–2022**: the French Wikipedia lists of polls, at fixed revisions for
  [2002](https://fr.wikipedia.org/w/index.php?oldid=236399441),
  [2007](https://fr.wikipedia.org/w/index.php?oldid=233109259),
  [2012](https://fr.wikipedia.org/w/index.php?oldid=238741176),
  [2017](https://fr.wikipedia.org/w/index.php?oldid=239719711) and
  [2022](https://fr.wikipedia.org/w/index.php?oldid=239942428).
* **Polls, 2002**: [france-politique.fr](https://www.france-politique.fr/sondages-electoraux-presidentielle-2002.htm),
  live copy and Wayback capture of 1 October 2026. It gives the client of each poll.
* **Polls, 2022**: [NSPPolls](https://github.com/nsppolls/nsppolls), `presidentielle.json` at commit `ddcd5ce`. It
  gives the client, the rolling flag and the Commission des sondages notice.
* **Official first-round results**: `data/FR-electoral_data.csv` in
  [strategic-voting-abm-2RS](https://github.com/clarasalas/strategic-voting-abm-2RS), at commit `8e99f86`.
* **Original documents** for the validation: pollsters' reports and Commission des sondages notices, linked row by
  row in the worklists.

Pins are in `config/sources.yaml`; every download is logged with its SHA-256 in `data/raw/manifest.csv`.

</details>

<details>
<summary><strong>Methodological choices</strong></summary>

<br>

* **Wikipedia is the base for every election**, so one source covers all five. For 2002 and 2022 the cross-check
  corrections are applied to it; polls only the second source has are not added.
* **Thinning.** Releases of a rolling poll share interviews. Within one pollster's series for one client, a release
  is dropped when its fieldwork overlaps a kept one, so each interview counts once (Erikson and Wlezien). OpinionWay's
  CNews and *Les Echos* series of 2022 are treated as one series sharing daily online samples, an assumption the
  notices support without stating it.
* **Party** is the label at the time of the poll (Juppé is UMP in 2014, LR from 2015). Orientation codes (DVG, DVD,
  EXD) are not parties and read as unaffiliated (SE).
* **Slot.** A tested candidate fills the place of a final candidacy when it is the same person, or the same party at
  the time, allowing for renamings (UMP → LR, FN → RN…); never across parties, even when a party later backed the
  candidate.
* **Ballot scenario.** Per poll, the hypothesis that fills the slot of every candidacy with at least 2% of the vote.
  It may also test candidates who will not run (Taubira in 2022): that is the poll voters saw.
* **Time** is counted in days before the first round, from the end of fieldwork (2007 and 2012: publication date).
* **Poll average**: a Gaussian kernel with a 10-day bandwidth, at least 3 polls nearby. Figures widen the window where
  polls are sparse and draw those stretches pale.
* **Shares** are rescaled to 100; every metric is also kept on raw shares. A share given as below a threshold counts
  as half its bound.
* **HHI rather than CENP** to compare elections, since CENP depends on the number of candidates.

Every decision, with its reason, is in [`docs/study_plan.md`](docs/study_plan.md).

</details>

<details>
<summary><strong>Limits</strong></summary>

<br>

* 2007 and 2012 dates are publication dates, usually 1 to 5 days after fieldwork.
* Small candidates, mostly at 2% or less, are missing in many 2007 and 2012 polls, so their shares can sum below 100.
* Before a party chose its candidate, Wikipedia can file the share under the eventual candidate (Mamère for Voynet
  or Lipietz in 2002).
* Sample sizes are given only from 2017, and are the base of respondents giving a voting intention.
* No undecided rate: polls leave out those who give no intention, about a quarter of respondents. No runoff polls.
* Five elections: every pattern above rests on five cases.

</details>

---

Clara Salas (ENS-PSL). Complementary analysis to the agent-based model
[strategic-voting-abm-2RS](https://github.com/clarasalas/strategic-voting-abm-2RS).
