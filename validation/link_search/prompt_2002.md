I am checking a dataset of French presidential first-round voting-intention polls for the 2002 election ("sondages d'intentions de vote au premier tour, présidentielle 2002"). For each poll in the table below, I need a link to an **original document that shows its results**, so I can check the numbers by hand.

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

## The polls (44 polls)

`client` is who commissioned the poll, when known. `old_link` is a link I already have that did not work or pointed to the wrong document: check it, and replace it if it is wrong. `leaders` are the top three candidates in the first scenario, as in my data.


| poll_id | pollster | client | fieldwork | sample size | scenarios | leaders | old_link |
|---|---|---|---|---|---|---|---|
| 2002_wp_bva_2002-02-02_1 | BVA | Paris Match | 2002-01-31 to 2002-02-02 |  | 1 | Jospin 22, Chirac 21, Chevènement 10 |  |
| 2002_wp_bva_2002-03-16_1 | BVA | Paris Match | 2002-03-14 to 2002-03-16 |  | 1 | Chirac 25, Jospin 22, Le Pen 10 |  |
| 2002_wp_bva_2002-04-06_1 | BVA | Paris Match | 2002-04-04 to 2002-04-06 |  | 1 | Jospin 20, Chirac 20, Le Pen 12 |  |
| 2002_wp_bva_2002-04-18_1 | BVA |  | (as written: "18 avril") |  | 1 | Chirac 19, Jospin 18, Le Pen 14 |  |
| 2002_wp_csa_2000-11-15_1 | CSA |  | 2000-11-14 to 2000-11-15 |  | 1 | Jospin 28, Chirac 27, Le Pen 10 |  |
| 2002_wp_csa_2001-05-30_1 | CSA |  | 2001-05-29 to 2001-05-30 |  | 1 | Jospin 28, Chirac 27, Le Pen 8 |  |
| 2002_wp_csa_2001-11-15_1 | CSA | Libération; BFM | 2001-11-14 to 2001-11-15 |  | 1 | Chirac 25, Jospin 23, Chevènement 10 |  |
| 2002_wp_csa_2002-01-30_1 | CSA |  | 2002-01-29 to 2002-01-30 |  | 1 | Chirac 23, Jospin 22, Chevènement 14 |  |
| 2002_wp_csa_2002-02-14_1 | CSA |  | 2002-02-13 to 2002-02-14 |  | 1 | Chirac 24.5, Jospin 21.5, Chevènement 10 |  |
| 2002_wp_csa_2002-03-14_1 | CSA |  | 2002-03-13 to 2002-03-14 |  | 1 | Chirac 25.5, Jospin 22, Le Pen 9.5 |  |
| 2002_wp_csa_2002-03-22_1 | CSA | Libération; La Dépêche du Midi | 2002-03-21 to 2002-03-22 |  | 1 | Chirac 23, Jospin 21, Le Pen 11 |  |
| 2002_wp_csa_2002-03-28_1 | CSA |  | 2002-03-27 to 2002-03-28 |  | 1 | Jospin 20, Chirac 20, Le Pen 12 |  |
| 2002_wp_csa_2001-03-26_1 | CSA |  | (as written: "26 mars") |  | 1 | Jospin 28, Chirac 28, Bayrou 7 |  |
| 2002_wp_ifop_2001-10-12_1 | Ifop | L'Express | 2001-10-11 to 2001-10-12 |  | 1 | Chirac 24, Jospin 23.5, Chevènement 10 |  |
| 2002_wp_ifop_2001-12-30_1 | Ifop | L'Express | 2001-12-29 to 2001-12-30 |  | 1 | Chirac 26, Jospin 22.5, Chevènement 10 |  |
| 2002_wp_ifop_2002-01-11_1 | Ifop |  | 2002-01-10 to 2002-01-11 |  | 1 | Chirac 27, Jospin 21, Chevènement 11 |  |
| 2002_wp_ifop_2002-01-18_1 | Ifop |  | 2002-01-17 to 2002-01-18 |  | 1 | Chirac 24, Jospin 20, Chevènement 11 |  |
| 2002_wp_ifop_2002-02-02_1 | Ifop | Journal du Dimanche | 2002-01-31 to 2002-02-02 |  | 1 | Chirac 24, Jospin 22, Chevènement 11 |  |
| 2002_wp_ifop_2002-02-08_1 | Ifop | L'Express; BFM/I-Télévision | 2002-02-07 to 2002-02-08 |  | 1 | Chirac 24, Jospin 19, Chevènement 13 |  |
| 2002_wp_ifop_2002-02-22_1 | Ifop | Journal du Dimanche | 2002-02-21 to 2002-02-22 |  | 1 | Chirac 25, Jospin 23, Chevènement 10 |  |
| 2002_wp_ifop_2002-02-23_1 | Ifop | L'Express; BFM/I-Télévision | 2002-02-22 to 2002-02-23 |  | 1 | Chirac 23, Jospin 22, Chevènement 12 |  |
| 2002_wp_ifop_2002-03-01_1 | Ifop | L'Express; BFM/I-Télévision | 2002-02-28 to 2002-03-01 |  | 1 | Chirac 22, Jospin 21, Chevènement 10 |  |
| 2002_wp_ifop_2002-03-16_1 | Ifop | L'Express; BFM/I-Télévision | 2002-03-15 to 2002-03-16 |  | 1 | Chirac 22, Jospin 19, Chevènement 11 |  |
| 2002_wp_ifop_2002-03-22_1 | Ifop | Journal du Dimanche | 2002-03-21 to 2002-03-22 |  | 1 | Chirac 23, Jospin 21, Le Pen 12 |  |
| 2002_wp_ifop_2002-03-24_1 | Ifop | L'Express; BFM/I-Télévision | 2002-03-23 to 2002-03-24 |  | 1 | Chirac 20, Jospin 19, Le Pen 10 |  |
| 2002_wp_ifop_2002-03-29_1 | Ifop | Journal du Dimanche | 2002-03-28 to 2002-03-29 |  | 1 | Chirac 21, Jospin 20.5, Laguiller 10 |  |
| 2002_wp_ifop_2002-04-06_1 | Ifop | L'Express; BFM/I-Télévision | 2002-04-05 to 2002-04-06 |  | 1 | Chirac 21, Jospin 17.5, Le Pen 13 |  |
| 2002_wp_ifop_2002-04-12_1 | Ifop |  | 2002-04-11 to 2002-04-12 |  | 1 | Chirac 19, Jospin 17, Le Pen 9.5 |  |
| 2002_wp_ipsos_2002-01-12_1 | Ipsos |  | 2002-01-11 to 2002-01-12 |  | 1 | Chirac 28, Jospin 24, Chevènement 10 |  |
| 2002_wp_ipsos_2002-02-09_1 | Ipsos |  | 2002-02-08 to 2002-02-09 |  | 1 | Chirac 23, Jospin 21, Chevènement 12 |  |
| 2002_wp_ipsos_2002-02-16_1 | Ipsos |  | 2002-02-15 to 2002-02-16 |  | 1 | Chirac 25, Jospin 20, Chevènement 12 |  |
| 2002_wp_ipsos_2002-03-02_1 | Ipsos |  | 2002-03-01 to 2002-03-02 |  | 1 | Chirac 24, Jospin 21, Chevènement 10 |  |
| 2002_wp_ipsos_2002-03-09_1 | Ipsos |  | 2002-03-08 to 2002-03-09 |  | 1 | Chirac 24, Jospin 22, Chevènement 11 |  |
| 2002_wp_ipsos_2002-04-18_1 | Ipsos |  | 2002-04-17 to 2002-04-18 |  | 1 | Chirac 20, Jospin 18, Le Pen 14 |  |
| 2002_wp_louis-harris_2002-02-02_1 | Louis Harris |  | 2002-02-01 to 2002-02-02 |  | 1 | Chirac 23, Jospin 23, Chevènement 13 |  |
| 2002_wp_louis-harris_2002-04-17_1 | Louis Harris |  | 2002-04-16 to 2002-04-17 |  | 1 | Chirac 20, Jospin 18, Le Pen 13 |  |
| 2002_wp_sofres_2001-05-16_1 | Sofres |  | 2001-05-15 to 2001-05-16 |  | 1 | Jospin 27, Chirac 26, Le Pen 8 |  |
| 2002_wp_sofres_2001-06-23_1 | Sofres |  | 2001-06-22 to 2001-06-23 |  | 1 | Jospin 27, Chirac 26, Le Pen 10 |  |
| 2002_wp_sofres_2001-09-08_1 | Sofres |  | 2001-09-07 to 2001-09-08 |  | 1 | Jospin 27, Chirac 26, Chevènement 9 |  |
| 2002_wp_sofres_2001-12-15_1 | Sofres |  | 2001-12-14 to 2001-12-15 |  | 1 | Chirac 27, Jospin 22, Chevènement 9 |  |
| 2002_wp_sofres_2002-01-12_1 | Sofres |  | 2002-01-11 to 2002-01-12 |  | 1 | Chirac 27, Jospin 22, Chevènement 9 |  |
| 2002_wp_sofres_2002-03-15_1 | Sofres | LCI/Politique Opinion | 2002-03-14 to 2002-03-15 |  | 1 | Chirac 24, Jospin 20, Le Pen 10 |  |
| 2002_wp_sofres_2002-03-16_1 | Sofres |  | 2002-03-13 to 2002-03-16 |  | 1 | Chirac 23.5, Jospin 21, Le Pen 10 |  |
| 2002_wp_sofres_2002-04-04_1 | Sofres | LCI/Politique Opinion | 2002-04-03 to 2002-04-04 |  | 1 | Chirac 24, Jospin 19, Le Pen 12 |  |
