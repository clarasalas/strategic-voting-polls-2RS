<h1 align="center">validation</h1>

<p align="center">
The checks a program cannot settle: three worklists, written once by notebook 03 and filled in by hand against
the pollster's report or the Commission des sondages notice.
</p>

<p align="center"><sub><a href="../README.md">← Back to the project</a></sub></p>

## What is in here

| File | What it holds | Filled in on 2 November 2026 |
|---|---|---|
| `crosscheck_disagreements.csv` | one row per scenario where two sources disagree | 79 of 79, done |
| `flagged_clients.csv` | overlapping polls by one pollster whose client Wikipedia doesn't give | 19 of 19, done |
| `spot_check_sample.csv` | 30 random Wikipedia polls per election | 150 of 150, done |

`notebooks/03_cross_check.ipynb` never overwrites an existing worklist. On a rerun it only reports how many rows
have answers and whether its own list of polls has changed. Files saved from a French-locale Excel, with `;` as
the separator, are read correctly.

## What to fill in

### `crosscheck_disagreements.csv`

The sources compared are france-politique and Wikipedia for 2002, NSPPolls and Wikipedia for 2022.

| Column | What to write |
|---|---|
| `correct_source` | `NSPPolls`, `Wikipedia`, `Fp` (france-politique, 2002), `neither`, or `NA` when no document was found |
| `document_url` | the document actually read (filled in from the link search; `document_to_use` holds NSPPolls' old, mostly dead links) |
| `notes` | for `neither`, the values in the document; when both sources are wrong but one is named, the other value it gets wrong |

Done: every row is answered. `link_check` and `link_notes` come from the link search (`link_search/`).

### `spot_check_sample.csv`

Check each poll against the original document: dates, sample size, and every share.

| Column | What to write |
|---|---|
| `document_url` | the document read |
| `dates_ok`, `sample_size_ok`, `shares_ok` | `yes`, `no` or `NA` (no document, or nothing to check against) |
| `notes` | what the document says, in the format below |

`notes` is a list of items separated by `; `. Each item starts with a key; a scenario prefix (`s2 share: …`)
limits it to one scenario. Candidates are named by surname, shares are in percent.

| Item | Meaning |
|---|---|
| `fieldwork: 2007-02-19 to 2007-02-20` | fieldwork dates in the document (one date if a single day) |
| `published: 2012-02-19` | publication date, when the document gives no fieldwork |
| `sample size: 1001` | full sample in the document (the data holds the base giving a voting intention) |
| `share: Jospin 23, Le Pen 7` | correct share of a candidate who is in the data; `<0.5` for a share below a threshold |
| `missing: Lepage (1)` | candidate in the document but not in the data, with the share |
| `not in document: Schivardi` | candidate in the data but not in the document |
| `candidate: Mamère → Voynet` | right share, wrong candidate: the data's name, then the document's |
| `document: none found` | no document; also `chart of the leading candidates only`, `commentary without full results`, `method and sample tables only` |
| `other: …` | anything else |

The sample is stratified by pollster and drawn with the seed in `config/validation.yaml`, fixed before the draw.
Do not redraw it. If no errors are found in 30 polls, the error rate is below about 10% at 95% confidence (rule of
three).

### `opinionway_2022_overlaps.csv`

The 34 OpinionWay polls of 2022 (NSPPolls) whose fieldwork overlaps between its CNews series (2 days) and its
*Les Echos* / Radio Classique rolling series (4 days), with each poll's Commission des sondages notice: the number,
the current address where the link search found it, the old (dead) address and its Wayback form. To settle whether
CNews got part of the same rolling sample:

| Column | What to write |
|---|---|
| `same_sample` | `yes`, `no`, `assumed` or `NA` |
| `notes` | what the notices say (fieldwork, sample, method) |

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
