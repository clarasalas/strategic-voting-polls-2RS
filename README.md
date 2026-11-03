<h1 align="center">French presidential polls, 2002–2022</h1>

<p align="center">
Every first-round poll of the five French presidential elections from 2002 to 2022, collected from pinned
sources, parsed into one table per source, and checked against the original documents.
</p>

<p align="center"><sub>
Paused on 5 October 2026, with the manual validation half done. <a href="#where-things-stand">Where things stand</a>
and <a href="#next-steps">Next steps</a> say where to pick up.
</sub></p>

## About

This is the poll data behind [strategic-voting-abm-2RS](https://github.com/clarasalas/strategic-voting-abm-2RS),
an agent-based model of strategic voting in two-round elections: an empirical study of French presidential
first-round polls, used to calibrate the model.

The polls come from the French Wikipedia lists of polls for the five elections, from france-politique.fr for 2002
and from NSPPolls for 2022. Every source is pinned (a Wikipedia revision, a git commit, a Wayback capture) and
stored exactly as downloaded, so the parsing can be rerun offline and gives the same tables. The output is one row
per poll × scenario × candidate.

Three steps follow the parsing. Rolling polls are thinned, so that each interview counts at most once within a
pollster's series for one client (Erikson and Wlezien). Where two sources cover the same election (2002 and 2022),
they are compared share by share. And the points a program cannot settle go to worklists filled in by hand
against the pollster's report or the Commission des sondages notice: the disagreements between sources, the
client of overlapping polls, and a random sample of 30 Wikipedia polls per election.

## Where things stand

**Collection, parsing, thinning and the manual validation are done, and the final dataset is built (`data/final/`). The calibration statistics are next.**

| Step | State on 2 November 2026 |
|---|---|
| Collect and parse (notebook 01) | done: 746 Wikipedia polls (2002–2022), 98 france-politique (2002), 351 NSPPolls (2022) |
| Candidate and pollster mappings (`config/`) | done, nothing unmapped |
| Thin rolling polls (notebook 02) | done: drops 6 Wikipedia polls in 2017, 32 in 2022, and 121 NSPPolls polls |
| Client lookups ([`flagged_clients.csv`](validation/README.md)) | done, 19 of 19 |
| Cross-source comparison (notebook 03) | run; 31 flagged overlaps (2002, 2022) resolved automatically |
| Settle disagreements ([`crosscheck_disagreements.csv`](validation/README.md)) | done, 79 of 79 |
| Spot check ([`spot_check_sample.csv`](validation/README.md)) | done, 150 of 150 (13 with no document) |
| Apply the validation answers to the tables | done (notebook 04): 136 corrections applied |
| Final dataset ([`data/final/polls.csv`](#final-dataset)) | done: 708 polls, 1,164 scenarios |
| Calibration statistics | not started |

## Next steps

<details>
<summary><strong>1 · Disagreements: done</strong></summary>

<br>

All 79 rows are settled. In 2002: france-politique 14, Wikipedia 1, no document found 4. In 2022: NSPPolls 35,
Wikipedia 23, no document found 2. No row is `neither`: the earlier `neither` answers came from dead links and
were redone with the documents found by the link search ([`validation/link_search/`](validation/link_search/README.md)).

Two 2022 rows (Ifop 18–19 June 2020 s3, Ifop 2–8 April 2021 s8) name the source with the bigger error, and `notes`
gives the one value that source also gets wrong. The code that applies the answers must read those notes.

</details>

<details>
<summary><strong>2 · The spot check: done</strong></summary>

<br>

All 150 polls are checked; 13 have no document (2002: 5, 2007: 3, 2012: 5) and are `NA`. What it found:

* **Main candidates' shares are reliable.** Real errors are rare (one to three polls per election) and of a
  point or less. The three 2022 polls with wrong shares are the ones the cross-check already corrected.
* **Small candidates are missing in 2007 and 2012** (Lepage, Dupont-Aignan, Nihous, Schivardi, Boutin, Morin,
  Villepin, Chevènement…), almost all at 2% or less, so shares do not sum to 100.
* **Dates in 2007 and 2012 are publication dates**, usually 1 to 5 days after the fieldwork.
* **Sample sizes in 2017 and 2022 are the base of respondents** giving a voting intention (about 91–95% of the
  full sample written in `notes`), not the full sample.
* **Before a party chose its candidate**, Wikipedia files the share under the eventual candidate (Mamère for
  Voynet or Lipietz in 2002, Joly for Hulot in 2012).

Corrections are in `notes`, in the format described in [`validation/README.md`](validation/README.md).

</details>

<details>
<summary><strong>3 · Final dataset: done</strong></summary>

<br>

Notebook 04 builds `data/final/polls.csv` (see [Final dataset](#final-dataset)). Decided on 2 November 2026:

* **Wikipedia is the base for every election**, so one source covers all five. For 2002 and 2022 the cross-check
  corrections are applied to it; polls only france-politique or NSPPolls has are not added.
* **2007 and 2012 stay as they are.** The dates stay publication dates and the missing small candidates are not
  added, not even for the polls checked by hand: correcting half the polls would mix two standards in one table
  and still leave the gap. These are reported as limits of the data. The same goes for the Green candidate's name
  before nomination (Mamère for Voynet or Lipietz in 2002).
* **Sample size is the base of respondents giving a voting intention**, as Wikipedia gives it, since the shares
  are percentages of that base. The full sample written in the spot check's `notes` is not used.
* **One-off errors are corrected**: wrong shares, candidates listed but not tested, and wrong dates where the data
  has fieldwork dates (2002, 2017, 2022).

Four items held for a check were settled on 3 November 2026 and their notes corrected: Ifop, June 2011
(Wikipedia had Joly, Chevènement and Hulot in the wrong scenarios: both now sum to 100); CSA, 16–17 April 2012
(the small candidates are in the document: only Hollande is corrected); YouGov, 4–7 April 2022 (dates kept: the
notice's cover page gives 4–7 April; its methodology page repeats the previous wave's 28–31 March); Odoxa, April 2015 (Wikipedia files Sarkozy's 26 under Juppé
in the Valls hypothesis: corrected).

Not added: NSPPolls' extra scenario for Ifop, June 2020 (answered `NSPPolls`), which is a one-candidate fragment
of its Bertrand hypothesis (Roussel 2); Wikipedia's scenario is right, as the answer for that poll's s3 says.

</details>

<details>
<summary><strong>4 · Loose ends</strong></summary>

<br>

* **The results file is pinned to a merged pull request.** It points to the commit of
  [strategic-voting-abm-2RS#24](https://github.com/clarasalas/strategic-voting-abm-2RS/pull/24), merged on
  2 October 2026. Blank `results.commit` in `config/sources.yaml` and rerun notebook 01 to re-pin to `main`.
* **Share sums.** 32 of 1,862 scenarios have shares summing outside 98–102: 19 on the 2012 Wikipedia page, and 4
  in NSPPolls, some summing to 0. They are listed at the end of notebook 01 and not investigated.
* **One parse error**: a 2017 Wikipedia cell reading `640-646` (`data/interim/parse_errors.csv`).
* **OpinionWay in 2022.** Its CNews releases overlap its *Les Echos* rolling releases, possibly one rolling sample
  sold to two clients. To check against the Commission des sondages notices (end of notebook 02).

</details>

## Reproduce

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/01_collect_and_parse.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_thin_rolling.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_cross_check.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/04_final_dataset.ipynb
```

Part 1 of notebook 01 needs the network. It downloads only what isn't already in `data/raw/`, so a rerun with
everything cached makes no requests except to resolve pins left blank. Part 2 reads only `data/raw/` and can be
run offline. Notebooks 02 to 04 read only `data/interim/` and `validation/`.

If notebook 01 stops with "unmapped candidate names" or "unmapped pollster names", open `config/candidates.csv` or
`config/institutes.csv`, fill in the empty columns for the listed rows, set `match` to `manual`, and rerun. Rows
already filled are never overwritten, so hand edits persist. The same holds for the worklists in `validation/`.

<details>
<summary><strong>Repository layout</strong></summary>

<br>

```
config/
  sources.yaml          pinned sources: Wikipedia revision IDs, git commits, Wayback capture
  candidates.csv        hand-editable map (election, candidate_raw) -> candidate
  institutes.csv        hand-editable map institute_raw -> institute, institute_family
  parties.csv           party for poll rows Wikipedia leaves without a label, and hand overrides (src/polls/parties.py)
  validation.yaml       seed and size of the spot-check sample (fixed before drawing)
  elections.yaml        first-round dates and official lists of candidates (time axis of the study)
data/
  raw/                  downloads exactly as received; never edited
    manifest.csv        one row per download: source, url, pinned_id, retrieved_utc (UTC), sha256, local_path, archive_url
    wikipedia/          MediaWiki API action=parse responses (JSON) for each pinned revision
    france_politique/   2002 page, live copy and Wayback copy
    nsppolls/           presidentielle.json at the pinned commit
    results/            FR-electoral_data.csv at the pinned commit
  interim/              parsed tables (regenerated by the notebooks)
    polls_wikipedia.csv, polls_france_politique.csv, polls_nsppolls.csv
    results.csv
    parse_errors.csv    cells that could not be parsed, with their raw contents
    thinning.csv        one row per poll: kept after removing rolling overlap, and why (notebook 02)
    crosscheck_{2002,2022}_{polls,shares}.csv   poll matches and share-by-share verdicts (notebook 03)
    flags_resolved.csv  flagged overlaps resolved from the other source (notebook 03)
  abm_input/            poll input for the ABM's empirical mode, prepared not used (notebook 07)
  final/                the final dataset (notebook 04)
    polls.csv           Wikipedia polls kept by thinning, with the validation applied
    corrections.csv     every correction in the worklists, applied or not, with the reason
    scenarios.csv       one row per scenario: ballot-scenario match, stand-ins, extra candidates
notebooks/
  01_collect_and_parse.ipynb
  02_thin_rolling.ipynb  removes sample overlap within a pollster/client series (Erikson & Wlezien)
  03_cross_check.ipynb   compares sources (2002, 2022), resolves flagged overlaps, draws the spot-check sample
  04_final_dataset.ipynb applies the validation and writes data/final/
  05_polls_descriptive.ipynb  the study, part 1: the polls themselves (docs/study_plan.md)
  06_polls_vs_results.ipynb   the study, part 2: polls against results
  07_parameters.ipynb         the study, part 3: parameter bounds and the empirical poll input
validation/             worklists filled in by hand; written once by notebook 03, never overwritten
  README.md                      how to fill them in
  crosscheck_disagreements.csv   polls where two sources disagree: settle against the original document
  flagged_clients.csv            overlapping polls (2017, one pair in 2022) whose client must be looked up
  spot_check_sample.csv          30 random Wikipedia polls per election (seed in config/validation.yaml)
src/polls/              functions used by the notebooks (fetch, parsers, mapping, thinning, checks, metrics)
tests/                  tests of the study's metrics and time axis (python -m pytest tests)
results/tables/         tables produced by the study notebooks; results/figures/ is regenerated, not committed
docs/study_plan.md      the study of the polls: plan, decisions, progress
```

</details>

<details>
<summary><strong id="final-dataset">Final dataset</strong></summary>

<br>

`data/final/polls.csv`: one row per poll × scenario × candidate, Wikipedia polls only, thinned. Columns are those
of the interim tables (below), plus:

| Column | Meaning |
|---|---|
| `party` | the label at the time of the poll: the poll's Wikipedia row (Juppé is UMP in 2014, LR from 2015), else `config/parties.csv` |
| `slot` | the final-ballot candidate whose place this candidate fills: the same person, or the same party at the time, allowing for renamings (UMP → LR, FN → RN, DLR → DLF, EM → LREM, LV → EELV, LCR → NPA). Empty for SE candidates and for parties absent from the ballot |
| `ballot_scenario` | this scenario is the poll's ballot scenario (see below) |
| `date` | `fieldwork_end`, or `reported_date` where the source gives no fieldwork (2007, 2012: publication date) |
| `corrected` | the row was changed by the validation (see `corrections.csv`) |
| `checked_against` | `other source` (matched in france-politique or NSPPolls), `original document` (spot check), both, or empty |

**Ballot scenario.** A scenario is a ballot scenario when every final candidacy with at least 2% of the vote has
its slot filled. It may also test candidates who will not be on the ballot (Taubira in 2022, Bayrou and Jadot in
2017): that is the poll voters saw. A candidate from another party never fills a slot, even if that party later
backed the final candidate. Per poll, the ballot scenario chosen has the most slots filled by the same person, then
the fewest extra candidates. Polls with one: 49 of 98 (2002, from February 2002), 107 of 107 (2007), 116 of 124
(2012), 109 of 148 (2017), 184 of 231 (2022). Rules in `src/polls/matching.py`.

`data/final/scenarios.csv`: one row per scenario: whether it is a ballot scenario and chosen, the required
candidacies missing, the candidates filling a slot for someone else, and the extra candidates with their total share.

`data/final/corrections.csv`: one row per item of the two worklists, with `applied` and, when not applied, the
`reason`. `old` and `new` give the value before and after.

**Limits to report**: 2007 and 2012 dates are publication dates, usually 1 to 5 days after fieldwork; small
candidates (mostly at 2% or less) are missing in many 2007 and 2012 polls, so shares can sum below 100; before a
party chose its candidate, the share can be filed under the eventual candidate; sample sizes are absent before 2017.

</details>

<details>
<summary><strong>Output tables</strong></summary>

<br>

One row per poll × scenario × candidate. Shares are in percent.

**Pollsters.** `institute_raw` is the name as written in the source; `institute` is the pollster at the time,
without partner names ("Ifop-Fiducial" → Ifop, "Cevipof Ipsos-Sopra Steria" → Ipsos); `institute_family` groups
renamings of one company (Sofres, TNS Sofres, Kantar Sofres, Kantar Public → "Kantar (Sofres)"; Louis Harris, LH2 →
"LH2 (Louis Harris)"; Atlas Político → AtlasIntel). Harris Interactive is a separate company from Louis
Harris/LH2. `poll_id` is built from `institute_raw`, so editing the mapping never changes ids.

**Columns beyond the base specification.** `scenario_label` (NSPPolls hypothesis), `reported_date` (a single date
when the source doesn't say whether it is the end of fieldwork or the publication date), `date_raw`,
`share_upper_bound`, `candidate_column` (the source column, when the candidate is named inside the cell),
`table_label`, and `source_poll_ref` (location in the source, or the NSPPolls poll id).

**`share_status`.**

| Value | Meaning | Share |
|---|---|---|
| `value` | a number | the number |
| `not_tested` | candidate not in this scenario (`—`, `ns`) | null |
| `grouped_others` | tested but counted in "others" (france-politique `autres`) | null |
| `below_threshold` | `<0,5 %`, `<1 %` | null; bound in `share_upper_bound` |
| `missing` | blank cell | null |

The pseudo-candidate `__others__` is the aggregate "Autres" row of the IFOP tables on france-politique. On
Wikipedia, the "Autres (candidats)" column lists extra named candidates and becomes ordinary candidate rows.

**`rolling`** is true only where the source says so: the `rolling` field in NSPPolls and "(rolling)" after the
pollster's name on the 2022 Wikipedia page. Otherwise it is null.

**Thinning** deletes nothing from the poll tables: join `data/interim/thinning.csv` on `poll_id` and filter on
`kept`.

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

Pins are in `config/sources.yaml`; every download is logged with its SHA-256 in `data/raw/manifest.csv`.

</details>

<details>
<summary><strong>Updating a pinned source</strong></summary>

<br>

Pins are only ever set when blank, never changed automatically.

* **Wikipedia page**: set that year's `revision_id` (and `revision_timestamp`) to `null` in `config/sources.yaml`
  to pin the current revision on the next run, or write a specific revision ID.
* **NSPPolls / results file**: set `commit` to `null` (pins the latest commit: on `master` for NSPPolls, the
  latest commit that modified the file for the results), or write a specific hash.
* **france-politique**: set `wayback_timestamp` to `null` and delete the local copy in
  `data/raw/france_politique/` to download the page again and request a new Wayback capture.

Old raw files stay in `data/raw/` and in the manifest; parsing uses only the files the current pins point to.

</details>

---

<sub>Clara Salas (ENS-PSL). Poll data for the agent-based model
[strategic-voting-abm-2RS](https://github.com/clarasalas/strategic-voting-abm-2RS). Companion project on the
geography of coordination: [strategic-voting-geo-2RS](https://github.com/clarasalas/strategic-voting-geo-2RS).</sub>
