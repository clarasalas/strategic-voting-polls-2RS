This is a second pass: an earlier search was cut off before reaching these polls. For `2012_wp_ipsos_2012-03-06_1`, an earlier search found an Ipsos article titled 'Tassement des deux principaux favoris au premier tour sur fond de lass…' (6 March 2012) but did not keep its address: give the full URL.

I am checking a dataset of French presidential first-round voting-intention polls for the 2012 election ("sondages d'intentions de vote au premier tour, présidentielle 2012"). For each poll in the table below, I need a link to an **original document that shows its results**, so I can check the numbers by hand.

## What counts as a good source, best first

1. The **Commission des sondages notice** for the poll (notice PDF on commission-des-sondages.fr). The Commission's online notices mostly cover recent years and may not exist for this election; move on to the other sources if nothing comes up.
2. The **pollster's own report** (PDF or results page on the pollster's site: ifop.com, elabe.fr, harris-interactive.fr, ipsos.com/fr-fr, opinion-way.com, odoxa.fr, bva-xsight.com, csa.eu, kantarpublic.com / tns-sofres.com, lh2.fr, yougov.com/fr, cluster17.com, etc.).
3. An **archived copy** of either of the above on the Wayback Machine (web.archive.org). Old pollster sites (TNS Sofres, LH2, Louis Harris, BVA, CSA) often survive only there.
4. The **article of the client** (the newspaper, TV or radio that commissioned it) that publishes the full results table.
5. Anything else that shows the full table of results, e.g. a CEVIPOF or Sciences Po archive, Persée, or a digitised newspaper (Gallica, Europresse).

Do not give the Wikipedia page or poll aggregators (Wikipedia, NSPPolls, france-politique.fr, Politico Poll of Polls, etc.); those are the sources I am checking.

## Rules

- **Only give a URL you have actually opened** and in which you saw this poll's results. Do not build a URL from a pattern or guess one. If you cannot open it, say so.
- Check that the document matches the poll: **same pollster, same fieldwork dates (± 1 day), and the leading candidates' shares** match the `leaders` column (or are within 1 point). If it is a different poll by the same pollster, it does not count.
- Polls often test several scenarios (`scenarios` column). The document should cover all of them; say in the notes if it does not.
- If you cannot find a document, write `not_found` and list where you looked. That is a useful answer; a wrong link is not.
- Work through the whole table. If you run out of space, stop at the end of a row and tell me which `poll_id` to continue from.

## Answer format

Answer with **one CSV code block** (comma-separated, values containing commas in double quotes), with these columns, one row per poll, in the same order as the table:

```
poll_id,url,source_type,matches,archive_url,notes
```

- `poll_id`: copied exactly from the table.
- `url`: the document's URL, or `not_found`.
- `source_type`: `commission_notice`, `pollster_report`, `wayback`, `client_article`, or `other`.
- `matches`: `yes` if you checked the dates and the leaders' shares against the document; `partly` if only some match (say which in notes); `unverified` if you could not open the document.
- `archive_url`: a Wayback Machine copy if there is one (optional).
- `notes`: anything I should know: a discrepancy, a missing scenario, where you looked if not found.

## The polls (12 polls)

`client` is who commissioned the poll, when known. `old_link` is a link I already have that did not work or pointed to the wrong document: check it, and replace it if it is wrong. `leaders` are the top three candidates in the first scenario, as in my data.


| poll_id | pollster | client | fieldwork | sample size | scenarios | leaders | old_link |
|---|---|---|---|---|---|---|---|
| 2012_wp_bva_2012-02-01_1 | BVA |  | (as written: "1er février") |  | 1 | Hollande 34, Sarkozy 25, Le Pen 15 |  |
| 2012_wp_bva_2012-01-21_1 | BVA |  | (as written: "21 janvier") |  | 1 | Hollande 30, Sarkozy 23, Le Pen 18 |  |
| 2012_wp_bva_2011-03-26_1 | BVA |  | (as written: "26 mars") |  | 2 | Aubry 24, Le Pen 20, Sarkozy 19 |  |
| 2012_wp_ipsos_2012-03-06_1 | Ipsos |  | (as written: "6 mars") |  | 1 | Hollande 29.5, Sarkozy 25, Le Pen 17.5 |  |
| 2012_wp_lh2_2012-04-01_1 | LH2 |  | (as written: "1er avril") |  | 1 | Hollande 28.5, Sarkozy 27.5, Mélenchon 15 |  |
| 2012_wp_lh2_2012-02-20_1 | LH2 |  | (as written: "20 février") |  | 1 | Hollande 32, Sarkozy 26, Le Pen 14 |  |
| 2012_wp_opinionway_2011-12-16_1 | OpinionWay |  | (as written: "16 décembre") |  | 1 | Hollande 29, Sarkozy 25, Le Pen 17 |  |
| 2012_wp_opinionway_2012-02-20_1 | OpinionWay |  | (as written: "20 février") |  | 1 | Hollande 29, Sarkozy 27, Le Pen 16.5 |  |
| 2012_wp_opinionway_2009-04-30_1 | OpinionWay |  | (as written: "30 avril 2009") |  | 1 | Sarkozy 30, Royal 21, Bayrou 20 |  |
| 2012_wp_opinionway_2012-02-08_1 | OpinionWay |  | (as written: "8 février") |  | 1 | Hollande 29, Sarkozy 25.5, Le Pen 18 |  |
| 2012_wp_sofres_2012-03-13_1 | Sofres |  | (as written: "13 mars") |  | 1 | Hollande 30, Sarkozy 26, Le Pen 16 |  |
| 2012_wp_sofres_2011-11-30_1 | Sofres |  | (as written: "30 novembre") |  | 1 | Hollande 31, Sarkozy 28, Le Pen 16.5 |  |
