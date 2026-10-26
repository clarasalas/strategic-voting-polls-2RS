I am checking a dataset of French presidential first-round voting-intention polls for the 2022 election ("sondages d'intentions de vote au premier tour, présidentielle 2022"). For each poll in the table below, I need a link to an **original document that shows its results**, so I can check the numbers by hand.

## What counts as a good source, best first

1. The **Commission des sondages notice** for the poll (notice PDF on commission-des-sondages.fr). Old links in the form `http://www.commission-des-sondages.fr/notices/files/notices/...` may have moved; search for the notice on the current site if they fail.
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

## The polls (66 polls)

`client` is who commissioned the poll, when known. `old_link` is a link I already have that did not work or pointed to the wrong document: check it, and replace it if it is wrong. `leaders` are the top three candidates in the first scenario, as in my data.


| poll_id | pollster | client | fieldwork | sample size | scenarios | leaders | old_link |
|---|---|---|---|---|---|---|---|
| 2022_wp_atlas-politico_2022-04-06_1 | Atlas Político |  | 2022-04-04 to 2022-04-06 | 1946 | 1 | Macron 27.8, Le Pen 21.3, Mélenchon 18.6 | https://atlasintel.org/poll/france-national-2022-04-07 |
| 2022_wp_bva_2021-11-15_1 | BVA | Orange, RTL | 2021-11-12 to 2021-11-15 | 1051 | 6 | Macron 26, Le Pen 18, Zemmour 15 | http://www.commission-des-sondages.fr/notices/files/notices/2021/novembre/9242-p-bva-cnews.pdf |
| 2022_wp_bva_2022-03-02_1 | BVA | RTL, Orange | 2022-03-01 to 2022-03-02 | 1072 | 1 | Macron 29, Le Pen 16, Pécresse 13 |  |
| 2022_wp_bva_2022-03-09_1 | BVA |  | 2022-03-08 to 2022-03-09 | 1500 | 1 | Macron 30, Le Pen 17, Zemmour 13 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9442-bva-orange-rtl-vague-9-le-11-mars-pdf.pdf |
| 2022_wp_bva_2022-03-23_1 | BVA |  | 2022-03-22 to 2022-03-23 | 1500 | 1 | Macron 28, Le Pen 19, Mélenchon 14.5 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9500-bva-orange-rtl-vague-11-25-mars.pdf |
| 2022_wp_cluster17_2021-12-22_1 | Cluster17 |  | 2021-12-19 to 2021-12-22 | 1554 | 1 | Macron 20, Pécresse 16, Zemmour 14 | https://cluster17.com/wp-content/uploads/2021/12/20211222_Cluster17_Notice-Technique_Rolling-Hebdomadaire_Publique.pdf |
| 2022_wp_cluster17_2022-01-22_1 | Cluster17 | Marianne | 2022-01-18 to 2022-01-22 | 2634 | 1 | Macron 22, Le Pen 15, Pécresse 14 | http://www.commission-des-sondages.fr/notices/files/notices/2022/janvier/9318-p-cluster-17-marianne.pdf |
| 2022_wp_elabe_2020-07-01_1 | Elabe | BFM TV | 2020-06-30 to 2020-07-01 | 893 | 4 | Macron 30, Le Pen 27.5, Mélenchon 12.5 | http://www.commission-des-sondages.fr/notices/files/notices/2020/juillet/9070-pdt-elabe-bfm.pdf |
| 2022_wp_elabe_2021-06-29_1 | Elabe | BFM TV | 2021-06-28 to 2021-06-29 | 815 | 3 | Macron 29, Le Pen 25, Bertrand 14 | http://www.commission-des-sondages.fr/notices/files/notices/2021/juillet/9197-p-elabe-bfm.pdf |
| 2022_wp_elabe_2021-09-13_1 | Elabe | BFM TV | 2021-09-11 to 2021-09-13 | 948 | 4 | Macron 26, Le Pen 23, Bertrand 16 | http://www.commission-des-sondages.fr/notices/files/notices/2021/septembre/9206-p-elabe-bfmtv.pdf |
| 2022_wp_elabe_2021-10-06_1 | Elabe |  | 2021-10-05 to 2021-10-06 | 1309 | 6 | Macron 25, Le Pen 16, Bertrand 13 | https://elabe.fr/wp-content/uploads/2021/10/pr2022.pdf |
| 2022_wp_elabe_2021-10-27_1 | Elabe | BFM TV, L'Express, SFR | 2021-10-25 to 2021-10-27 | 948 | 3 | Macron 23, Le Pen 19, Zemmour 15 | http://www.commission-des-sondages.fr/notices/files/notices/2021/octobre/9230-p-elabe-bfm-l-express.pdf |
| 2022_wp_elabe_2021-11-24_1 | Elabe | BFM TV, L'Express, SFR | 2021-11-23 to 2021-11-24 | 1042 | 5 | Macron 25, Le Pen 20, Bertrand 13 | http://www.commission-des-sondages.fr/notices/files/notices/2021/novembre/9247-p-elabe-bfmtv.pdf |
| 2022_wp_elabe_2022-01-11_1 | Elabe | BFM TV, L'Express, SFR | 2022-01-10 to 2022-01-11 | 1071 | 2 | Macron 22.5, Le Pen 16.5, Pécresse 16 | http://www.commission-des-sondages.fr/notices/files/notices/2022/janvier/9289-p-elabe-bfm.pdf |
| 2022_wp_elabe_2022-02-22_1 | Elabe | BFM TV, L'Express, SFR | 2022-02-21 to 2022-02-22 | 1125 | 1 | Macron 24, Le Pen 18, Zemmour 13.5 | http://www.commission-des-sondages.fr/notices/files/notices/2022/fevrier/9388-p-elabe-bfmtv-23-2.pdf |
| 2022_wp_elabe_2022-03-30_1 | Elabe |  | 2022-03-28 to 2022-03-30 | 1531 | 1 | Macron 28, Le Pen 21, Mélenchon 15.5 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9517-elabe-bfmtv-le-30-mars.pdf |
| 2022_wp_elabe_2022-04-05_1 | Elabe |  | 2022-04-04 to 2022-04-05 | 1358 | 1 | Macron 28, Le Pen 23, Mélenchon 15.5 | http://www.commission-des-sondages.fr/notices/files/notices/2022/avril/9545-elabe-bfm-5-avril.pdf |
| 2022_wp_harris-interactive_2021-01-20_1 | Harris Interactive | L'Opinion | 2021-01-19 to 2021-01-20 | 976 | 4 | Le Pen 26, Macron 24, Bertrand 16 | http://www.commission-des-sondages.fr/notices/files/notices/2021/janvier/9092-p-hi-l-opinion.pdf |
| 2022_wp_harris-interactive_2021-05-31_1 | Harris Interactive | Challenges | 2021-05-28 to 2021-05-31 | 1057 | 2 | Le Pen 28, Macron 25, Bertrand 14 |  |
| 2022_wp_harris-interactive_2021-06-14_1 | Harris Interactive |  | 2021-06-11 to 2021-06-14 | 1304 | 4 | Le Pen 29, Macron 28, Bertrand 14 | https://www.commission-des-sondages.fr/notices/files/notices/2021/juin/9186-presidentielles-challenges-v6-hi.pdf |
| 2022_wp_harris-interactive_2021-08-30_1 | Harris Interactive | Challenges | 2021-08-27 to 2021-08-30 | 1083 | 4 | Macron 24, Le Pen 23, Bertrand 16 | http://www.commission-des-sondages.fr/notices/files/notices/2021/septembre/9202-p-hi-v11-challenges.pdf |
| 2022_wp_harris-interactive_2021-11-22_1 | Harris Interactive |  | 2021-11-19 to 2021-11-22 | 2624 | 5 | Macron 23, Zemmour 16, Le Pen 16 | https://harris-interactive.fr/wp-content/uploads/sites/6/2021/11/DGTENVF-AX5.pdf |
| 2022_wp_harris-interactive_2022-01-31_1 | Harris Interactive | Challenges | 2022-01-28 to 2022-01-31 | 2141 | 1 | Macron 24, Le Pen 17, Pécresse 15 | http://www.commission-des-sondages.fr/notices/files/notices/2022/fevrier/9329-hi-challenges-v31.pdf |
| 2022_wp_harris-interactive_2022-02-14_1 | Harris Interactive | Challenges | 2022-02-11 to 2022-02-14 | 2053 | 1 | Macron 25, Le Pen 17.5, Zemmour 14.5 | http://www.commission-des-sondages.fr/notices/files/notices/2022/fevrier/9363-p-hi-challenges.pdf |
| 2022_wp_harris-interactive_2022-02-21_1 | Harris Interactive | Challenges | 2022-02-18 to 2022-02-21 | 2018 | 1 | Macron 24, Le Pen 17, Zemmour 15.5 | http://www.commission-des-sondages.fr/notices/files/notices/2022/fevrier/9389-harris-interactive-challenges-v34-le-23-fevrier.pdf |
| 2022_wp_harris-interractive_2022-03-28_1 | Harris Interactive |  | 2022-03-25 to 2022-03-28 | 2384 | 1 | Macron 28.5, Le Pen 21, Mélenchon 15 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9513-harris-interactive-challenges-v39-le-30-mars.pdf |
| 2022_wp_ifop_2020-06-19_1 | Ifop | CNews, Sud Radio | 2020-06-18 to 2020-06-19 | 992 | 2 | Le Pen 28, Macron 26, Bertrand 12 | http://www.commission-des-sondages.fr/notices/files/notices/2020/juin/9063-pdt-ifop-c-news.pdf |
| 2022_wp_ifop_2021-02-24_1 | Ifop |  | 2021-02-23 to 2021-02-24 | 902 | 1 | Macron 31, Bertrand 21, Zemmour 17 | https://www.commission-des-sondages.fr/notices/files/notices/2021/mars/9103-p-ifop-club-de-la-presse.pdf |
| 2022_wp_ifop_2021-04-08_1 | Ifop | Journal du Dimanche, Sud Radio | 2021-04-02 to 2021-04-08 | 1730 | 10 | Macron 28, Le Pen 27, Mélenchon 13 | http://www.commission-des-sondages.fr/notices/files/notices/2021/avril/9113-p-ifop-jddpdf.pdf |
| 2022_wp_ifop_2021-05-20_1 | Ifop |  | 2021-05-18 to 2021-05-20 | 1363 | 5 | Le Pen 29, Macron 27, Mélenchon 12 | https://www.commission-des-sondages.fr/notices/files/notices/2021/mai/9139-p-ifop-le-figaro.pdf |
| 2022_wp_ifop_2021-09-02_1 | Ifop | LCI, Le Figaro | 2021-08-31 to 2021-09-02 | 1334 | 8 | Macron 24, Le Pen 24, Bertrand 17 | http://www.commission-des-sondages.fr/notices/files/notices/2021/septembre/9203-p-ifop-v3-le-figaro.pdf |
| 2022_wp_ifop_2021-10-13_1 | Ifop | LCI, Le Figaro | 2021-10-09 to 2021-10-13 | 4503 | 3 | Macron 25, Le Pen 17, Zemmour 16 | http://www.commission-des-sondages.fr/notices/files/notices/2021/octobre/9224-p-ifop-le-figaro.pdf |
| 2022_wp_ifop_2021-12-15_1 | Ifop | Sud Radio | 2021-12-14 to 2021-12-15 | 1017 | 1 | Macron 25.5, Pécresse 18, Le Pen 16 | http://www.commission-des-sondages.fr/notices/files/notices/2021/decembre/9268-p-ifop-sud-radio.pdf |
| 2022_wp_ifop_2022-01-20_1 | Ifop | Paris Match, LCI, Sud Radio | 2022-01-18 to 2022-01-20 | 1377 | 1 | Macron 25.5, Le Pen 18, Pécresse 16 | http://www.commission-des-sondages.fr/notices/files/notices/2022/janvier/9304-rdp-ifop-pm.pdf |
| 2022_wp_ifop_2022-02-10_1 | Ifop |  | 2022-02-07 to 2022-02-10 | 1502 | 1 | Macron 25.5, Le Pen 17.5, Pécresse 15 | https://www.ifop.com/wp-content/uploads/2022/02/ROL22_2022.02.10.pdf |
| 2022_wp_ifop_2022-02-17_1 | Ifop | Paris Match, LCI, Sud Radio | 2022-02-14 to 2022-02-17 | 1371 | 1 | Macron 26, Le Pen 16.5, Zemmour 16 | http://www.commission-des-sondages.fr/notices/files/notices/2022/fevrier/9370-rdp-ifop-pm-17-fev.pdf |
| 2022_wp_ifop_2022-03-18_1 | Ifop | Paris Match, LCI, Sud Radio | 2022-03-15 to 2022-03-18 | 1397 | 1 | Macron 29.5, Le Pen 18.5, Mélenchon 13 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9474-rdp-ifop-paris-match.pdf |
| 2022_wp_ifop_2022-03-21_1 | Ifop |  | 2022-03-17 to 2022-03-21 | 1508 | 1 | Macron 28, Le Pen 18.5, Mélenchon 14 | https://www.ifop.com/wp-content/uploads/2022/03/ROL22_2022.03.21.pdf |
| 2022_wp_ipsos_2021-01-28_1 | Ipsos | L'Obs, France Info | 2021-01-27 to 2021-01-28 | 750 | 7 | Le Pen 25, Macron 24, Bertrand 14 | http://www.commission-des-sondages.fr/notices/files/notices/2021/fevrier/9095-pres-ipsos-l-obs.pdf |
| 2022_wp_ipsos_2021-09-03_1 | Ipsos | France Info, Le Parisien | 2021-09-02 to 2021-09-03 | 490 | 6 | Macron 25, Le Pen 22, Bertrand 17 | http://www.commission-des-sondages.fr/notices/files/notices/2021/septembre/9204-p-ipsos-le-parisien.pdf |
| 2022_wp_ipsos_2022-02-27_1 | Ipsos | Le Monde, Cevipof, Fondation Jean Jaurès | 2022-02-24 to 2022-02-27 | 9009 | 1 | Macron 26.5, Le Pen 15.5, Zemmour 15 |  |
| 2022_wp_ipsos_2022-03-14_1 | Ipsos |  | 2022-03-10 to 2022-03-14 | 8790 | 1 | Macron 29, Le Pen 16, Zemmour 13 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9466-p-ipsos-le-monde-fjj-cevipof-panel-elec-toral-v7.pdf |
| 2022_wp_ipsos_2022-03-24_1 | Ipsos | Le Monde, Cevipof, Fondation Jean Jaurès | 2022-03-21 to 2022-03-24 | 8908 | 1 | Macron 28, Le Pen 17.5, Mélenchon 14 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9506-ipsos-cevipof-lm-28-mars.pdf |
| 2022_wp_ipsos_2022-03-30_2 | Ipsos | Le Parisien, France Info | 2022-03-27 to 2022-03-30 | 990 | 1 | Macron 27, Le Pen 20.5, Mélenchon 15.5 |  |
| 2022_wp_ipsos_2022-03-30_1 | Ipsos | Le Parisien, France Info | 2022-03-28 to 2022-03-31 | 990 | 1 | Macron 27.5, Le Pen 20, Mélenchon 15.5 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9520-ipsos-le-parisien-aujourd-hui-en-france-france-info-barometre-2022-vague-17-31-mars.pdf |
| 2022_wp_ipsos_2022-04-02_1 | Ipsos | Le Parisien, France Info | 2022-03-30 to 2022-04-02 | 1122 | 1 | Macron 26, Le Pen 21, Mélenchon 15.5 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9532-ipsos-le-parisien-aujourd-hui-en-france-france-info-barometre-2022-vague-19-2-avril-p-df.pdf |
| 2022_wp_kantar_2022-03-09_1 | Kantar Public |  | 2022-03-07 to 2022-03-09 | 1394 | 1 | Macron 31, Le Pen 17, Zemmour 13 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9438-p-kantar-v2-le-10-mars.pdf |
| 2022_wp_odoxa_2021-09-23_1 | Odoxa |  | 2021-09-22 to 2021-09-23 | 1005 | 4 | Macron 26, Le Pen 20.5, Bertrand 14 | https://www.odoxa.fr/sondage/intentions-de-vote-a-la-presidentielle-et-match-zemmour-melenchon-dans-lopinion |
| 2022_wp_odoxa_2022-02-16_1 | Odoxa | L'Obs, Mascaret | 2022-02-15 to 2022-02-16 | 1799 | 1 | Macron 24.5, Le Pen 18, Zemmour 14 | http://www.commission-des-sondages.fr/notices/files/notices/2022/fevrier/9368-p-odoxa-l-obs-fev-22.pdf |
| 2022_wp_odoxa_2022-03-11_1 | Odoxa |  | 2022-03-09 to 2022-03-11 | 2010 | 1 | Macron 29.5, Le Pen 19.5, Mélenchon 11.5 | http://www.odoxa.fr/sondage/macron-renforce-encore-son-statut-de-favori-tandis-que-m-le-pen-distance-ses-rivaux-pour-la-qualification-au-second-tour/ |
| 2022_wp_opinionway_2021-12-15_1 | OpinionWay | Les Echos, CNews, Radio Classique | 2021-12-13 to 2021-12-15 | 1470 | 1 | Macron 24, Pécresse 17, Le Pen 16 | http://www.commission-des-sondages.fr/notices/files/notices/2021/decembre/9266-p-ow-cnews-v4.pdf |
| 2022_wp_opinionway_2022-01-14_1 | OpinionWay |  | 2022-01-11 to 2022-01-14 | 1577 | 1 | Macron 24, Le Pen 18, Pécresse 18 | http://www.commission-des-sondages.fr/notices/files/notices/2022/janvier/9295-rpw-ow-kea-partners-les-echos-radio-classique-14-janvier.pdf |
| 2022_wp_opinionway_2022-01-21_1 | OpinionWay | Les Echos, Radio Classique, Kea Partners | 2022-01-18 to 2022-01-21 | 1613 | 1 | Macron 25, Pécresse 18, Le Pen 17 | http://www.commission-des-sondages.fr/notices/files/notices/2022/janvier/9309-rpw-ow-kea-radio-classique.pdf |
| 2022_wp_opinionway_2022-02-07_1 | OpinionWay |  | 2022-02-04 to 2022-02-07 | 1630 | 1 | Macron 24, Pécresse 17, Le Pen 17 | http://www.commission-des-sondages.fr/notices/files/notices/2022/fevrier/9345-opinionway-kea-les-echos-7-fev.pdf |
| 2022_wp_opinionway_2022-02-21_1 | OpinionWay | Les Echos, Radio Classique, Kea Partners | 2022-02-18 to 2022-02-21 | 1638 | 1 | Macron 25, Le Pen 16, Pécresse 14 | http://www.commission-des-sondages.fr/notices/files/notices/2022/fevrier/9381-rpw-ow-les-echos.pdf |
| 2022_wp_opinionway_2022-03-03_1 | OpinionWay | Les Echos, Radio Classique, Kea Partners | 2022-03-01 to 2022-03-04 | 1624 | 1 | Macron 28, Le Pen 17, Pécresse 13 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9423-rpw-opinionway-kea-partners-les-echos-radio-classique-4-mars.pdf |
| 2022_wp_opinionway_2022-03-06_1 | OpinionWay |  | 2022-03-05 to 2022-03-06 | 1091 | 1 | Macron 29, Le Pen 18, Pécresse 14 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9427-p-opinionway-cnews-vague-12-le-7-mars.pdf |
| 2022_wp_opinionway_2022-03-07_2 | OpinionWay |  | 2022-03-04 to 2022-03-07 | 1672 | 1 | Macron 30, Le Pen 18, Pécresse 13 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9425-opinionway-kea-partners-les-echos-radio-classique-notice-a-la-commission-7-mars.pdf |
| 2022_wp_opinionway_2022-03-13_1 | OpinionWay | CNews | 2022-03-12 to 2022-03-13 | 1110 | 1 | Macron 30, Le Pen 19, Pécresse 11 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9449-opinionway-pour-cnews-notice-a-la-commission-vague-17-le-14-mars.pdf |
| 2022_wp_opinionway_2022-03-21_1 | OpinionWay | CNews | 2022-03-20 to 2022-03-21 | 1092 | 1 | Macron 28, Le Pen 18, Mélenchon 14 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9485-opinionway-cnews-vague-23-le-22-mars.pdf |
| 2022_wp_opinionway_2022-03-22_1 | OpinionWay | CNews | 2022-03-21 to 2022-03-22 | 1093 | 1 | Macron 29, Le Pen 18, Mélenchon 14 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9493-ow-pour-cnews-23-mars-vague-24.pdf |
| 2022_wp_opinionway_2022-03-31_1 | OpinionWay | CNews | 2022-03-30 to 2022-03-31 | 1044 | 1 | Macron 27, Le Pen 21, Mélenchon 15 | http://www.commission-des-sondages.fr/notices/files/notices/2022/mars/9527-opinionway-pour-cnews-vague-31-le-1er-avril.pdf |
| 2022_wp_opinionway_2022-04-06_1 | OpinionWay | Les Echos, Radio Classique, Kea Partners | 2022-04-03 to 2022-04-06 | 1902 | 1 | Macron 26, Le Pen 22, Mélenchon 16 | http://www.commission-des-sondages.fr/notices/files/notices/2022/avril/9549-opinionway-kea-partners-les-echos-radio-classique-6-avril.pdf |
| 2022_wp_opinionway_2022-04-07_2 | OpinionWay |  | 2022-04-04 to 2022-04-07 | 2043 | 1 | Macron 26, Le Pen 22, Mélenchon 17 | http://www.commission-des-sondages.fr/notices/files/notices/2022/avril/9555-opinionway-kea-partners-les-echos-radio-classique-notice-a-la-commission-7-avril.pdf |
| 2022_wp_yougov_2022-03-31_1 | YouGov | Datapraxis | 2022-03-28 to 2022-03-31 | 1883 | 1 | Macron 27, Le Pen 25, Mélenchon 15 | http://www.commission-des-sondages.fr/notices/files/notices/2022/avril/9553-yougov-datapraxis-iv-presidentielles-avril-2022.pdf |
| 2022_wp_yougov_2022-04-07_1 | YouGov |  | 2022-04-04 to 2022-04-07 | 1984 | 1 | Macron 26, Le Pen 23, Mélenchon 16 | http://www.commission-des-sondages.fr/notices/files/notices/2022/avril/9566-yougov-datapraxis-8-avril-2022.pdf |
