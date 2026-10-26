I am checking a dataset of French presidential first-round voting-intention polls for the 2007 election ("sondages d'intentions de vote au premier tour, présidentielle 2007"). For each poll in the table below, I need a link to an **original document that shows its results**, so I can check the numbers by hand.

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

## The polls (30 polls)

`client` is who commissioned the poll, when known. `old_link` is a link I already have that did not work or pointed to the wrong document: check it, and replace it if it is wrong. `leaders` are the top three candidates in the first scenario, as in my data.


| poll_id | pollster | client | fieldwork | sample size | scenarios | leaders | old_link |
|---|---|---|---|---|---|---|---|
| 2007_wp_bva_2007-04-12_1 | BVA |  | (as written: "12 avril") |  | 1 | Sarkozy 28, Royal 24, Bayrou 18 |  |
| 2007_wp_bva_2007-02-21_1 | BVA |  | (as written: "21 février") |  | 1 | Sarkozy 33, Royal 26, Bayrou 15 |  |
| 2007_wp_bva_2007-03-22_1 | BVA |  | (as written: "22 mars") |  | 1 | Sarkozy 31, Royal 24, Bayrou 17 |  |
| 2007_wp_csa_2007-01-17_1 | CSA |  | (as written: "17 janvier") |  | 1 | Sarkozy 30, Royal 29, Le Pen 15 |  |
| 2007_wp_csa_2006-10-18_1 | CSA |  | (as written: "18 octobre") |  | 1 | Royal 32, Sarkozy 31, Le Pen 15 |  |
| 2007_wp_csa_2007-04-19_1 | CSA |  | (as written: "19 avril") |  | 1 | Sarkozy 27, Royal 26, Bayrou 17 |  |
| 2007_wp_csa_2007-04-05_1 | CSA |  | (as written: "5 avril") |  | 1 | Sarkozy 26, Royal 23.5, Bayrou 21 |  |
| 2007_wp_csa_2007-03-07_1 | CSA |  | (as written: "7 mars") |  | 1 | Sarkozy 26, Royal 25, Bayrou 24 |  |
| 2007_wp_ifop_2005-01-21_1 | Ifop |  | 2005-01-20 to 2005-01-21 |  | 3 | Sarkozy 34, Fabius 18, Le Pen 12 |  |
| 2007_wp_ifop_2007-02-12_1 | Ifop |  | (as written: "12 février") |  | 1 | Sarkozy 33.5, Royal 26, Bayrou 14 |  |
| 2007_wp_ifop_2006-11-18_1 | Ifop |  | (as written: "18 novembre") |  | 1 | Sarkozy 29, Royal 29, Le Pen 11 |  |
| 2007_wp_ifop_2007-01-19_1 | Ifop |  | (as written: "19 janvier") |  | 1 | Sarkozy 32.5, Royal 28, Bayrou 12.5 |  |
| 2007_wp_ifop_2007-03-25_1 | Ifop |  | (as written: "25 mars") |  | 1 | Sarkozy 26, Royal 25, Bayrou 22 |  |
| 2007_wp_ifop_2007-02-26_1 | Ifop |  | (as written: "26 février") |  | 1 | Sarkozy 28, Royal 28, Bayrou 17 |  |
| 2007_wp_ipsos_2007-02-19_1 | Ipsos |  | (as written: "19 février") |  | 1 | Sarkozy 33, Royal 23, Bayrou 16 |  |
| 2007_wp_ipsos_2006-12-01_1 | Ipsos |  | (as written: "1er décembre") |  | 1 | Sarkozy 35, Royal 31, Le Pen 12.5 |  |
| 2007_wp_ipsos_2007-04-20_1 | Ipsos |  | (as written: "20 avril") |  | 1 | Sarkozy 30, Royal 23, Bayrou 18 |  |
| 2007_wp_ipsos_2007-02-26_1 | Ipsos |  | (as written: "26 février") |  | 1 | Sarkozy 31, Royal 26, Bayrou 17.5 |  |
| 2007_wp_ipsos_2007-03-29_1 | Ipsos |  | (as written: "29 mars") |  | 1 | Sarkozy 31.5, Royal 25, Bayrou 17.5 |  |
| 2007_wp_ipsos_2007-04-03_1 | Ipsos |  | (as written: "3 avril") |  | 1 | Sarkozy 31.5, Royal 24, Bayrou 19 |  |
| 2007_wp_ipsos_2007-03-08_1 | Ipsos |  | (as written: "8 mars") |  | 1 | Sarkozy 32.5, Royal 27, Bayrou 19 |  |
| 2007_wp_lh2_2007-03-12_1 | LH2 |  | (as written: "12 mars") |  | 1 | Sarkozy 28, Royal 26, Bayrou 22 |  |
| 2007_wp_lh2_2007-03-26_1 | LH2 |  | (as written: "26 mars") |  | 1 | Sarkozy 27, Royal 27, Bayrou 20 |  |
| 2007_wp_lh2_2007-02-03_1 | LH2 |  | (as written: "3 février") |  | 1 | Sarkozy 33, Royal 27, Bayrou 13 |  |
| 2007_wp_lh2_2007-04-09_1 | LH2 |  | (as written: "9 avril") |  | 1 | Sarkozy 28, Royal 24, Bayrou 18 |  |
| 2007_wp_sofres_2006-11-11_1 | Sofres |  | (as written: "11 novembre") |  | 1 | Sarkozy 34, Royal 34, Le Pen 13 |  |
| 2007_wp_sofres_2007-04-13_1 | Sofres |  | (as written: "13 avril") |  | 1 | Sarkozy 30, Royal 26, Bayrou 17 |  |
| 2007_wp_sofres_2007-01-18_1 | Sofres |  | (as written: "18 janvier") |  | 1 | Sarkozy 35, Royal 31, Le Pen 13 |  |
| 2007_wp_sofres_2007-03-05_1 | Sofres |  | (as written: "5 mars") |  | 1 | Sarkozy 31, Royal 25.5, Bayrou 18.5 |  |
| 2007_wp_sofres_2006-10-05_1 | Sofres |  | (as written: "5 octobre") |  | 1 | Sarkozy 38, Royal 29.5, Le Pen 9.5 |  |
