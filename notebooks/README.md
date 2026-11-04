<h1 align="center">notebooks</h1>

<p align="center">
The whole project, in order: four notebooks build the dataset, three study it.
</p>

<p align="center"><sub><a href="../README.md">← Back to the project</a></sub></p>

## Start here

| Notebook | What it does | Writes |
|---|---|---|
| `01_collect_and_parse` | downloads the pinned sources (only what is missing) and parses them into one table per source; maps names to candidates and pollsters; checks consistency | `data/raw/`, `data/interim/polls_*.csv`, `results.csv`, `parse_errors.csv` |
| `02_thin_rolling` | removes sample overlap within one pollster's series for one client, so that each interview counts once | `data/interim/thinning.csv` |
| `03_cross_check` | compares the polls of two sources (2002, 2022) share by share; draws the spot-check sample; writes the worklists | `data/interim/crosscheck_*.csv`, `validation/` (once) |
| `04_final_dataset` | applies the hand-filled worklists, assigns parties and slots, chooses each poll's ballot scenario | `data/final/` |
| `05_polls_descriptive` | the polls themselves: coverage, trajectories, rank stability, pollsters, noise | `results/tables/`, `results/figures/` |
| `06_polls_vs_results` | polls against results: structure metrics, where concentration changes, error by role, the cliff, momentum, stylized facts | `results/tables/`, `results/figures/` |
| `07_parameters` | the model's parameters: ρ<sub>s</sub>, θ, ρ<sub>π</sub>, tolerance, real-world ranges, the empirical poll input | `results/tables/`, `results/figures/`, `data/abm_input/` |

Run them in order, from the repository root:

```bash
for nb in notebooks/0*.ipynb; do jupyter nbconvert --to notebook --execute --inplace "$nb"; done
```

They are committed with their outputs, so they can be read without running them. Each one starts with what it reads
and writes, and the study notebooks follow the blocks of [`docs/study_plan.md`](../docs/study_plan.md).

<details>
<summary><strong>Running parts of the pipeline</strong><br>The network, the worklists, and when to rerun what</summary>

<br>

* **Network.** Part 1 of notebook 01 downloads only what is not already in `data/raw/`, which is committed, so a rerun
  makes no request unless a pin in `config/sources.yaml` is blank. Part 2 reads only `data/raw/`. Every other notebook
  is offline.
* **Worklists.** Notebook 03 writes the worklists in `validation/` once and never overwrites them. On a rerun it only
  reports how many rows are answered and whether its own list of polls has changed.
* **What to rerun.** A change to `config/` needs 01 onwards (`parties.csv`: 04 onwards); a change to a worklist, 04
  onwards; a change to the study, the notebook concerned (05 to 07 read only `data/final/` and the results).

</details>
