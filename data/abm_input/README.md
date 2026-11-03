# Poll input for the ABM's empirical mode

Prepared by `notebooks/07_parameters.ipynb` (section 6) with `src/polls/abm_input.py`, in the format the ABM reads
(`data/polls_{year}.csv` in strategic-voting-abm-2RS). **Not used by the ABM yet**: to try one, copy it over the ABM's
file of the same year.

| File | Window | Rolling releases |
|---|---|---|
| `polls_{year}.csv` | the ABM's current window: 1 March – 18 April 2002; 7 March (official list) – 8 April 2022 | thinned: each interview counted once |
| `polls_{year}_all_releases.csv` | same | every release, as voters saw them |
| `polls_{year}_12_weeks.csv` | the last 12 weeks before the first round | thinned |

Built from the validated dataset (`data/final/polls.csv`): each poll's ballot scenario; candidates mapped to the ABM's
parties through their slot (Juppé would count for LR) and the slot's party in the results; extra candidates who will
not be on the ballot dropped (the ABM rescales each poll); below-threshold shares at half their bound, listed in
`below_threshold`; a poll missing a modelled party would be dropped and listed in `polls_dropped.csv` (none is).
`fieldwork` gives the fieldwork dates (ISO), not the published text.

Against the ABM's current files, the weekly signal the ABM computes (ISO-week means, rescaled) differs by 0.01 to
0.07 points on average and at most 0.3 points (`results/tables/abm_input_comparison.csv`).
