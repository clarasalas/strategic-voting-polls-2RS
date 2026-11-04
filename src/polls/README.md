<h1 align="center">src/polls</h1>

<p align="center">
The code the notebooks call. Each module does one step; the notebooks put them in order.
</p>

<p align="center"><sub><a href="../../README.md">← Back to the project</a></sub></p>

## What is in here

The notebooks add `src/` to the path and import `polls`; nothing needs installing.

| Step | Modules |
|---|---|
| **Collect** | `fetch` (downloads to `data/raw/` as received, pins, manifest) |
| **Parse** | `wikipedia`, `france_politique`, `nsppolls` (one parser per source), `html_tables` (rowspan and colspan), `textparse` (French numbers, shares and dates), `results` (official results) |
| **Map and assemble** | `candidates`, `institutes`, `parties` (through the hand-editable files in `config/`), `assemble` (column order, types, stable ids) |
| **Check and thin** | `checks` (consistency reports; never drop rows), `thinning` (rolling overlap) |
| **Validate** | `crosscheck` (two sources, share by share), `sampling` (the spot-check draw), `worklists` (written to `validation/`), `links` (links from the link search into the worklists) |
| **Final dataset** | `final` (applies the worklists), `matching` (slots and ballot scenarios) |
| **Study** | `timeline` (days before the vote, phases), `metrics` (HHI, ENP, cliff, gaps, roles), `average` (poll average), `ideology` (left-right order), `figures` (plotting helpers), `abm_input` (the model's poll input) |

<details>
<summary><strong>Where the main rules live</strong><br>Which module to read for each decision</summary>

<br>

| Rule | Module |
|---|---|
| Each interview counted once; OpinionWay's 2022 series sharing daily samples (`SHARED_SAMPLES`) | `thinning.py` |
| A Wikipedia poll's client taken from the matched france-politique or NSPPolls poll | `thinning.py` (`series_key`), from notebook 02 |
| Party at the time; orientation codes read as SE | `parties.py` |
| Slots, renamings (`RENAMES`), the 2% threshold, choosing the ballot scenario | `matching.py` |
| How each worklist answer becomes a correction, or why not | `final.py` |
| HHI, ENP, the cliff as in the model, roles with ties, below-threshold shares | `metrics.py` |
| Kernel, bandwidth, minimum polls, leave-one-out, the widened window of the figures | `average.py` |

</details>
