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

**Collection, parsing and thinning are done. The disagreements are settled; the spot check is not done yet. Nothing after it exists yet.**

| Step | State on 29 October 2026 |
|---|---|
| Collect and parse (notebook 01) | done: 746 Wikipedia polls (2002–2022), 98 france-politique (2002), 351 NSPPolls (2022) |
| Candidate and pollster mappings (`config/`) | done, nothing unmapped |
| Thin rolling polls (notebook 02) | done: drops 6 Wikipedia polls in 2017, 32 in 2022, and 121 NSPPolls polls |
| Client lookups ([`flagged_clients.csv`](validation/README.md)) | done, 19 of 19 |
| Cross-source comparison (notebook 03) | run; 31 flagged overlaps (2002, 2022) resolved automatically |
| Settle disagreements ([`crosscheck_disagreements.csv`](validation/README.md)) | done, 79 of 79 |
| Spot check ([`spot_check_sample.csv`](validation/README.md)) | **links found for 137 of 150; checks not started** |
| Apply the validation answers to the tables | not started: no code reads them |
| Final dataset, calibration statistics | not started: only `data/interim/` exists |

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
<summary><strong>2 · The spot check</strong></summary>

<br>

150 polls, none checked yet (`sample_size_ok` is `NA` for 2002–2012: those sources give no sample size).
`document_url` is filled in for 137; 13 have no document (2002: 5, 2007: 3, 2012: 5), and about 27 link to a
commentary or a chart that shows only the leading candidates (`link_check` says `partly`). Mark the ones with no
document `NA` rather than replacing them: the sample is drawn with a fixed seed and must not be redrawn.

</details>

<details>
<summary><strong>3 · Apply the answers, then build the final dataset</strong></summary>

<br>

Nothing reads the worklists' answers yet, apart from the clients, which notebook 02 uses. To decide: how
corrections are applied (a corrections table read when the final dataset is built?), which source is used for 2002
and 2022, and what the final table looks like. The calibration statistics come after that.

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
```

Part 1 of notebook 01 needs the network. It downloads only what isn't already in `data/raw/`, so a rerun with
everything cached makes no requests except to resolve pins left blank. Part 2 reads only `data/raw/` and can be
run offline. Notebooks 02 and 03 read only `data/interim/` and `validation/`.

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
  validation.yaml       seed and size of the spot-check sample (fixed before drawing)
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
notebooks/
  01_collect_and_parse.ipynb
  02_thin_rolling.ipynb  removes sample overlap within a pollster/client series (Erikson & Wlezien)
  03_cross_check.ipynb   compares sources (2002, 2022), resolves flagged overlaps, draws the spot-check sample
validation/             worklists filled in by hand; written once by notebook 03, never overwritten
  README.md                      how to fill them in
  crosscheck_disagreements.csv   polls where two sources disagree: settle against the original document
  flagged_clients.csv            overlapping polls (2017, one pair in 2022) whose client must be looked up
  spot_check_sample.csv          30 random Wikipedia polls per election (seed in config/validation.yaml)
src/polls/              functions used by the notebooks (fetch, parsers, mapping, thinning, checks)
```

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
