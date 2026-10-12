<h1 align="center">validation</h1>

<p align="center">
The checks a program cannot settle: three worklists, written once by notebook 03 and filled in by hand against
the pollster's report or the Commission des sondages notice.
</p>

<p align="center"><sub><a href="../README.md">← Back to the project</a></sub></p>

## What is in here

| File | What it holds | Filled in on 12 October 2026 |
|---|---|---|
| `crosscheck_disagreements.csv` | one row per scenario where two sources disagree | **21 of 79** |
| `flagged_clients.csv` | overlapping polls by one pollster whose client Wikipedia doesn't give | 19 of 19, done |
| `spot_check_sample.csv` | 30 random Wikipedia polls per election | **0 of 150** |

`notebooks/03_cross_check.ipynb` never overwrites an existing worklist. On a rerun it only reports how many rows
have answers and whether its own list of polls has changed. Files saved from a French-locale Excel, with `;` as
the separator, are read correctly.

## What to fill in

### `crosscheck_disagreements.csv`

The sources compared are france-politique and Wikipedia for 2002, NSPPolls and Wikipedia for 2022.

| Column | What to write |
|---|---|
| `correct_source` | `NSPPolls`, `Wikipedia` or `neither` (the values used so far); `france-politique` for 2002 |
| `document_url` | the document actually read, if it is not `document_to_use` |
| `notes` | for `neither`, the values in the document |

Rows are sorted by election, then pollster. Rows 20 to 40 are done: BVA, Cluster17, Elabe and Harris Interactive
in 2022. The 19 rows for 2002 and the 2022 rows from Ifop onwards are not.

**To settle first.** 15 of the 21 answers are `neither`, and none has a note, so the right values are not written
down. See step 1 of [Next steps](../README.md#next-steps).

### `spot_check_sample.csv`

Check each poll against the original document: dates, sample size, and every share.

| Column | What to write |
|---|---|
| `document_url` | the document read |
| `dates_ok`, `sample_size_ok`, `shares_ok` | `yes`, `no` or `n.a.` |
| `notes` | what is wrong, when something is |

The sample is stratified by pollster and drawn with the seed in `config/validation.yaml`, fixed before the draw.
Do not redraw it. If no errors are found in 30 polls, the error rate is below about 10% at 95% confidence (rule of
three).

### `flagged_clients.csv`

Done. `client` is who commissioned the poll and `client_found_in` where that was read. Notebook 02 reads this
file: two overlapping polls with the same pollster and the same client are one series, and are thinned.

<details>
<summary><strong>Reading a row of the disagreements</strong></summary>

<br>

| Column | What it tells you |
|---|---|
| `scenario` | the scenario's position in the poll, e.g. `s2 of 5` |
| `scenario_label` | the source's own label, e.g. NSPPolls' "Hypothèse Pécresse" |
| `scenario_identified_by` | the candidates that set it apart from the poll's other scenarios |
| `disagreements` | `candidate: source a vs Wikipedia`, where source a is france-politique or NSPPolls |
| `shares_source_a`, `shares_wikipedia` | the full list of shares in each source |
| `document_to_use` | the Commission des sondages notice, when NSPPolls gives one; empty for 2002 and for 4 rows of 2022 |

</details>

<details>
<summary><strong>Reading a row of the spot check</strong></summary>

<br>

| Column | What it tells you |
|---|---|
| `upstream_source_url`, `notice_url` | the report or notice linked by Wikipedia; present for every 2017 and 2022 row, for none in 2002, 2007 and 2012 |
| `table_label` | the table of the Wikipedia page the poll is in |
| `shares_as_parsed` | the shares by scenario, `s1: … ; s2: …`, to compare by eye |

</details>
