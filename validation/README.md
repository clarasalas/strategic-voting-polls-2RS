# Validation worklists

Written once by `notebooks/03_cross_check.ipynb`, then filled in by hand. The notebook never overwrites
an existing file; on a rerun it only reports how many rows have answers and whether its list of polls
has changed. Files saved from a French-locale Excel (`;` separator) are read correctly.

Progress on 12 October 2026: see the status table in the [main README](../README.md).

## crosscheck_disagreements.csv (21 of 79)

One row per scenario where two sources disagree: france-politique vs Wikipedia (2002), NSPPolls vs
Wikipedia (2022). Settle each against the original document.

* `scenario`, `scenario_label`, `scenario_identified_by`: how to find the scenario in the document
  (position in the poll, NSPPolls' own label, the candidates that set it apart).
* `disagreements`: `candidate: source a vs Wikipedia`. Full lists are in `shares_source_a` and
  `shares_wikipedia`.
* `document_to_use`: the Commission des sondages notice, when NSPPolls gives one. Empty for 2002 and
  for 4 of the 2022 rows.

To fill in:

* `correct_source`: `NSPPolls`, `Wikipedia` or `neither` (the values used so far); `france-politique`
  for 2002.
* `document_url`: the document actually read, if not `document_to_use`.
* `notes`: for `neither`, the values in the document. Not done yet for the 15 existing `neither` rows.

Rows are sorted by election and pollster. Rows 20–40 (2022: BVA, Cluster17, Elabe, Harris Interactive)
are done; the 19 rows for 2002 and the 2022 rows from Ifop onwards are not.

## flagged_clients.csv (19 of 19, done)

Overlapping polls by one pollster whose client Wikipedia doesn't give (2017, and one pair in 2022).
`client` is who commissioned the poll, `client_found_in` where that was read. Notebook 02 reads this
file: two overlapping polls with the same pollster and client are treated as one series and thinned.

## spot_check_sample.csv (0 of 150)

30 Wikipedia polls per election, stratified by pollster, drawn with the seed in
`config/validation.yaml`. Do not redraw. Check each poll against the original document
(`upstream_source_url` or `notice_url` when there is one; `shares_as_parsed` lists the shares by scenario).

To fill in: `document_url`, then `dates_ok`, `sample_size_ok`, `shares_ok` with `yes`, `no` or `n.a.`,
and `notes` for anything that is wrong.
