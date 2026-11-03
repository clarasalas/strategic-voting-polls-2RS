<h1 align="center">Study plan</h1>

<p align="center">
What the polls look like, how they compare with the results, and what they say about the model's parameters,
with every decision taken so far. Ticked as the work goes.
</p>

<p align="center"><sub><a href="../README.md">← Back to the project</a></sub></p>

## Purpose

A preliminary study of French presidential first-round polls, 2002–2022, before they are used in the agent-based
model [strategic-voting-abm-2RS](https://github.com/clarasalas/strategic-voting-abm-2RS). The question is practical:
how accurate are polls, how much coordination do they show, and toward whom. It is not a general political-science
study of polling: events, polling modes and the number of hypotheses tested are left out, except where they are
needed to read a result.

Nothing here runs the model. Part 3 only produces bounds and inputs that the model can use later.

## Part 0 · Foundations (done)

| Topic | Decision |
|---|---|
| Base | Wikipedia polls, thinned (notebook 02), with the validation applied (notebook 04): `data/final/polls.csv` |
| Party | the label at the time of the poll: the poll's Wikipedia row, else `config/parties.csv` (with dated periods: Bertrand LR from 15 October 2021, Pécresse from 14 October 2021). Orientation codes (DVG, DVD, EXD) read as SE |
| Slot | the final candidacy a candidate stands in for: same person, or same party at the time, allowing for renamings (UMP → LR, FN → RN…). Never across parties, even when a party later backed the candidate (Buffet, Bayrou, EELV 2017) |
| Scenario | per poll, the *ballot scenario*: every final candidacy with ≥ 2% of the vote has its slot filled; extra candidates not on the ballot allowed and counted (`n_extra`, `extra_share`). Descriptive work may use all scenarios |
| Time axis | days before the first round, from the end of fieldwork (2007, 2012: publication date). Publication comes about 1 day after fieldwork (median, 0–4 days, from the spot check): acknowledged, not modelled |
| Phases | before the official list of candidates; from the list to two weeks before; the last two weeks (`config/elections.yaml`) |
| Shares | every metric computed rescaled to 100 and raw. Below-threshold shares count as half their bound |
| Concentration | HHI = Σ shares², rescaled HHI = 1 / ENP of the ABM. HHI rather than CENP, which depends on the number of candidates |
| Roles | leader, 2nd, 3rd, others, by rank; tied candidates share a role (two 2nds, cliff 0). Pooled analyses take roles from the poll average, not single polls |
| Candidates | all candidates in Parts 1 and 2; the ABM's candidate set only when preparing its inputs |

## Part 1 · The polls themselves (notebook 05)

- [ ] **Coverage**: polls per election, month and pollster; pace near the vote; rolling polls; sample sizes
- [ ] **Trajectories**: poll average per candidate with a band; week-to-week volatility; markers where the set of
      tested candidates changes (entries, withdrawals)
- [ ] **Rank stability**: who is 1st to 4th over time; rank swaps; share of polls whose top two is the real runoff
      pair; date from which the runoff pair stops changing
- [ ] **Pollsters**: house effects (pollster × candidate, against the poll average); herding (agreement beyond sampling
      error, especially near the vote)
- [ ] **Noise**: spread within a week against sampling error: effective sample size

## Part 2 · Polls against results (notebook 06)

- [ ] **Structure metrics** per poll and result: HHI and ENP, top-two share, cliff (2nd − 3rd, in points and relative
      to 2nd), 1st–2nd and 3rd–4th gaps, candidates in contention
- [ ] **Their evolution**, with the change in HHI split two ways: campaign (first poll → last polls) against last mile
      (last polls → result); and change in the candidate set (elite coordination: withdrawals) against shares moving
      within a fixed set (voter coordination)
- [ ] **Poll error by role**, signed: do candidates near the cliff do worse than their polls, their neighbours better?
- [ ] **The cliff**: size in polls against the result; predictability of the runoff pair at each horizon
- [ ] **Who gains in the last weeks**, for 2002 and 2022 with the ABM's candidate positions
- [ ] **Momentum**: does rising predict rising further?
- [ ] **Stylized facts** across the five elections (2007, 2012 and 2017 as out-of-sample cases)

## Part 3 · Parameters (notebook 07)

- [ ] **Poll noise ρ<sub>s</sub>** per election, against the synthetic bounds (10–200). Polling moved from phone to online
      between 2002 and 2022: estimate per election, do not pool blindly
- [ ] **Temperature θ**, two estimates compared: final polls against results (contaminated by late strategic switching:
      a bound), and the slope of shares by rank in polls against results
- [ ] **Prior spread ρ<sub>π</sub>**: how much pollsters disagree at the opening of the campaign
- [ ] **Tolerance τ̂**: paired scenarios of one poll, differing by one candidate, show where that candidate's voters
      go when not offered
- [ ] **Real-world ranges** for the synthetic setup: number of candidates tested (10–16, against 6, 8, 9), HHI, cliff,
      1st–2nd gap, slope of shares by rank
- [ ] **Poll input for the empirical mode**, prepared only: window, aggregation, scenario, thresholds, variants

**Parked**: α, how far voters follow the latest poll (the mechanism will change; survey data on expectations, such as
the CEVIPOF Enquête électorale, would measure it).

## Conventions

- Shared code in `src/polls/` (`timeline.py`, `metrics.py`), tested in `tests/`.
- Tables in `results/tables/`, committed: every number cited comes from one. Figures in `results/figures/`,
  regenerated by the notebooks, not committed.
- One block at a time, reviewed before the next; merged to `main` at the end of each part.

## Limits to report

2007 and 2012 dates are publication dates; small candidates are missing in many 2007 and 2012 polls; sample sizes only
from 2017; no undecided rate (polls exclude those who give no intention, about a quarter of respondents); no runoff
polls.
