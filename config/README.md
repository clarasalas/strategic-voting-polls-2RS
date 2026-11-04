<h1 align="center">config</h1>

<p align="center">
What the pipeline reads before any poll: the pinned sources, the election calendar, and the hand-editable mappings
from names in the sources to candidates, pollsters and parties.
</p>

<p align="center"><sub><a href="../README.md">← Back to the project</a></sub></p>

## What is in here

| File | What it holds | Used by |
|---|---|---|
| `sources.yaml` | the pins: a Wikipedia revision per election, the NSPPolls and results commits, the france-politique Wayback capture | notebook 01 |
| `elections.yaml` | first-round dates and the publication of the official list of candidates | the time axis and campaign phases (`src/polls/timeline.py`) |
| `candidates.csv` | (election, name as written in the source) → candidate, 263 rows | notebook 01 |
| `institutes.csv` | name as written → pollster at the time and company (`institute_family`), 38 rows | notebook 01 |
| `parties.csv` | party for poll rows Wikipedia leaves without a label, with dated periods, 48 rows | notebook 04 (`src/polls/parties.py`) |
| `validation.yaml` | seed and size of the spot-check sample, fixed before the draw | notebook 03 |

## Hand-editable mappings

The three `.csv` files are written by the pipeline and then edited by hand. A rerun adds rows for new names but
**never changes a row already in the file**, so hand edits persist. `match` says where each row came from:

| File | `match` values |
|---|---|
| `candidates.csv` | `results` (name on the official list), `exact`, `surname`, `initial+surname`, `hint`, `rule`, `manual` |
| `institutes.csv` | `spelling` (a spelling variant), `manual` |
| `parties.csv` | `label` (the candidate's only label elsewhere on Wikipedia), `suggested` (a proposal), `manual` (checked by hand) |

If notebook 01 stops with "unmapped candidate names" or "unmapped pollster names", fill in the empty columns of the
listed rows, set `match` to `manual`, and rerun.

<details>
<summary><strong>parties.csv</strong><br>Labels at the time, dated periods and overrides</summary>

<br>

The party of a poll row is first the label in the row itself on Wikipedia ("Alain Juppé (UMP)" in 2014, "(LR)" from
2015), so it follows renamings and changes of party. This file covers the rest:

* `party` fills the rows without a label, and must be the label at the time of those rows (Duflot in 2010: Les Verts,
  before EELV existed);
* `from_date` starts a period: a candidate can have several rows, each applying from its date until the next one
  (Bertrand in 2022: unaffiliated, then LR from 15 October 2021; Pécresse: Libres!, then LR from 14 October 2021);
* `override` = `yes` applies `party` to every row of that candidate, replacing Wikipedia's label (none at present).

Orientation codes (DVG, DVD, EXD) are not parties and read as unaffiliated (SE): Zemmour is SE until Reconquête was
founded on 5 December 2021.

</details>

<details>
<summary><strong>Updating a pinned source</strong><br>Pins are only set when blank, never changed automatically</summary>

<br>

* **Wikipedia page**: set that year's `revision_id` (and `revision_timestamp`) to `null` to pin the current revision
  on the next run, or write a specific revision id.
* **NSPPolls, results file**: set `commit` to `null` (pins the latest commit: on `master` for NSPPolls, the latest
  commit that modified the file for the results), or write a specific hash.
* **france-politique**: set `wayback_timestamp` to `null` and delete the local copy in `data/raw/france_politique/`
  to download the page again and request a new Wayback capture.

Old raw files stay in `data/raw/` and in the manifest; parsing uses only the files the current pins point to. A new
pin changes the polls, so the validation worklists may no longer match: notebook 03 reports it.

</details>
