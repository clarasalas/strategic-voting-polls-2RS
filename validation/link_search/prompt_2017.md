I am checking a dataset of French presidential first-round voting-intention polls for the 2017 election ("sondages d'intentions de vote au premier tour, présidentielle 2017"). For each poll in the table below, I need a link to an **original document that shows its results**, so I can check the numbers by hand.

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

## The polls (30 polls)

`client` is who commissioned the poll, when known. `old_link` is a link I already have that did not work or pointed to the wrong document: check it, and replace it if it is wrong. `leaders` are the top three candidates in the first scenario, as in my data.


| poll_id | pollster | client | fieldwork | sample size | scenarios | leaders | old_link |
|---|---|---|---|---|---|---|---|
| 2017_wp_bva_2016-06-12_1 | BVA |  | 2016-06-10 to 2016-06-12 | 910 | 4 | Juppé 36, Le Pen 26, Hollande 14 | http://www.bva.fr/data/sondage/sondage_fiche/1872/fichier_pop2017_-_intentions_de_vote_-_vague_3ff173.pdf |
| 2017_wp_bva_2016-09-11_1 | BVA |  | 2016-09-09 to 2016-09-11 | 912 | 8 | Juppé 36, Le Pen 30, Mélenchon 12 | http://www.bva.fr/data/sondage/sondage_fiche/1900/fichier_intentions_de_vote_-_vague_5_-_pop2017_-_septembre_20164d4a8.pdf |
| 2017_wp_bva_2016-10-19_1 | BVA |  | 2016-10-14 to 2016-10-19 | 916 | 6 | Juppé 37, Le Pen 29, Mélenchon 12.5 | http://www.bva.fr/data/sondage/sondage_fiche/1913/fichier_intentions_de_vote_-_vague_6_-_pop2017_-_octobre_20169c21a.pdf |
| 2017_wp_csa_2013-04-28_1 | CSA |  | 2013-04-26 to 2013-04-28 | 1027 | 1 | Sarkozy 34, Le Pen 23, Hollande 19 | http://www.csa.eu/multimedia/data/sondages/data2013/opi20130429-les-francais-et-francois-hollande-avril-2013-v2.pdf |
| 2017_wp_dedicated-research_2017-02-14_1 | Dedicated Research |  | 2017-02-10 to 2017-02-14 | 2066 | 2 | Le Pen 22.1, Macron 21.3, Fillon 16.7 | http://www.lalibre.be/actu/international/sondage-lalibre-rtbf-dedicated-emmanuel-macron-president-de-la-republique-58aa982fcd703b981556229b |
| 2017_wp_elabe_2017-01-31_1 | Elabe |  | 2017-01-30 to 2017-01-31 | 650 | 2 | Le Pen 26, Macron 22, Fillon 19 | http://elabe.fr/wp-content/uploads/2017/02/01022017_les_echos_radio_classique_intentions-de-vote-presidentielles_vague_6.pdf |
| 2017_wp_elabe_2017-02-20_1 | Elabe |  | 2017-02-18 to 2017-02-20 | 1051 | 2 | Le Pen 27, Fillon 20, Macron 17 | http://elabe.fr/intentions-de-vote-election-presidentielle-2017-2/ |
| 2017_wp_elabe_2017-04-05_1 | Elabe |  | (as written: "5 avr.") | 995 | 1 | Macron 23.5, Le Pen 23.5, Fillon 19 | http://elabe.fr/wp-content/uploads/2017/04/05042017_bfmtv_lexpress_intentions-de-vote-presidentielles-vague-7.pdf |
| 2017_wp_future-thinking-ssi_2013-04-29_1 | Future Thinking - SSI |  | 2013-04-26 to 2013-04-29 | 1000 | 3 | Sarkozy 32, Le Pen 22, Hollande 15 | http://www.groupe-acticall.com/sites/default/files/images/presse/communiques/CP_Sondage_Intention_de_vote_des_Francais_un_an_apres_le_premier_tour_de_la_presidentielle_01.pdf |
| 2017_wp_harris-interactive_2017-03-08_1 | Harris Interactive |  | 2017-03-06 to 2017-03-08 | 4533 | 1 | Macron 26, Le Pen 25, Fillon 20 | http://harris-interactive.fr/wp-content/uploads/sites/6/2017/03/Rapport-Harris-Intentions-vote-election-presidentielle-France-TV-2.pdf |
| 2017_wp_harris-interactive_2017-04-06_1 | Harris Interactive |  | 2017-04-05 to 2017-04-06 | 1014 | 1 | Macron 24, Le Pen 23, Fillon 19 | http://harris-interactive.fr/wp-content/uploads/sites/6/2017/04/Rapport-Harris-Intentions-vote-election-presidentielle-LCP.pdf |
| 2017_wp_ifop_2016-06-17_1 | Ifop |  | 2016-06-14 to 2016-06-17 | 1858 | 9 | Juppé 35, Le Pen 29, Hollande 14 | http://www.ifop.com/media/poll/3432-1-study_file.pdf |
| 2017_wp_ifop-fiducial_2016-11-30_1 | Ifop |  | 2016-11-28 to 2016-11-30 | 1882 | 2 | Fillon 28, Le Pen 24, Macron 15 | http://www.ifop.com/media/poll/3576-1-study_file.pdf |
| 2017_wp_ifop-fiducial_2017-02-22_1 | Ifop |  | 2017-02-20 to 2017-02-22 | 1399 | 1 | Le Pen 26.5, Macron 19, Fillon 19 | http://cdn1-new-parismatch.ladmedia.fr/var/ifop/22-02-2017.pdf |
| 2017_wp_ifop-fiducial_2017-03-02_1 | Ifop |  | 2017-02-28 to 2017-03-02 | 1394 | 1 | Le Pen 26, Macron 24, Fillon 21 | http://cdn3-new-parismatch.ladmedia.fr/var/ifop/02-03-2017.pdf |
| 2017_wp_ifop-fiducial_2017-03-21_1 | Ifop |  | 2017-03-18 to 2017-03-21 | 1695 | 1 | Le Pen 26, Macron 25.5, Fillon 17.5 | http://dataviz.ifop.com:8080/IFOP_ROLLING/IFOP_21-03-2017.pdf |
| 2017_wp_ifop-fiducial_2017-03-29_1 | Ifop |  | 2017-03-26 to 2017-03-29 | 2241 | 1 | Macron 26, Le Pen 25.5, Fillon 17.5 | http://cdn1-new-parismatch.ladmedia.fr/var/ifop/29-03-2017.pdf?version=14aa3f6b |
| 2017_wp_cevipof-ipsos-sopra-steria_2016-01-31_1 | Ipsos |  | 2016-01-22 to 2016-01-31 | 21326 | 3 | Le Pen 26, Sarkozy 21, Hollande 20 | http://www.ipsos.fr/decrypter-societe/2016-02-09-alain-juppe-en-position-force-avant-primaire-et-presidentielle/ |
| 2017_wp_cevipof-ipsos-sopra-steria_2016-09-18_1 | Ipsos |  | 2016-09-09 to 2016-09-18 | 18659 | 4 | Le Pen 29, Sarkozy 22, Hollande 13 | http://www.youscribe.com/catalogue/tous/actualite-et-debat-de-societe/politique/l-action-du-president-de-la-republique-l-election-presidentielle-la-2760685 |
| 2017_wp_ipsos_2017-03-27_1 | Ipsos |  | 2017-03-25 to 2017-03-27 | 1005 | 1 | Le Pen 25, Macron 24, Fillon 18 | http://www.ipsos.fr/decrypter-societe/2017-03-28-presidentielle-2017-l-etat-d-esprit-francais-4-semaines-l-election-presidentielle |
| 2017_wp_kantar-sofres_2017-02-24_1 | Kantar Sofres |  | 2017-02-23 to 2017-02-24 | 1005 | 1 | Le Pen 27, Macron 25, Fillon 20 | http://fr.kantar.com/elections/presidentielle/2017/intentions-de-vote-marine-le-pen-et-emmanuel-macron-creusent-l-ecart/ |
| 2017_wp_kantar-sofres-onepoint_2017-03-04_1 | Kantar Sofres |  | 2017-03-02 to 2017-03-04 | 1027 | 2 | Le Pen 26, Macron 25, Fillon 17 | http://fr.kantar.com/elections/presidentielle/2017/intentions-de-vote-francois-fillon-nettement-distance-par-marine-le-pen-et-emmanuel-macron/ |
| 2017_wp_odoxa_2015-04-30_1 | Odoxa |  | 2015-04-29 to 2015-04-30 | 1021 | 2 | Le Pen 29, Sarkozy 28, Hollande 17 | http://www.odoxa.fr/wp-content/uploads/2015/05/Odoxa-pour-le-Parisien-Aujourdhui-en-France-Quels-sc%C3%A9narios-pour-2017.pdf |
| 2017_wp_odoxa_2015-05-22_1 | Odoxa |  | 2015-05-21 to 2015-05-22 | 1021 | 2 | Le Pen 30, Sarkozy 25, Hollande 17 | http://www.odoxa.fr/wp-content/uploads/2015/05/Odoxa-pour-le-Parisien-Aujourdhui-en-France-2017-lhypothèse-Juppé.pdf |
| 2017_wp_odoxa_2017-04-13_1 | Odoxa |  | 2017-04-12 to 2017-04-13 | 1001 | 1 | Macron 24.5, Le Pen 23, Mélenchon 19 | http://www.odoxa.fr/sondage/presidentielle-lincertitude-totale-1er-tour-bien-2nd-tour-macron-se-qualifiait/ |
| 2017_wp_opinionway_2013-04-17_1 | OpinionWay |  | 2013-04-16 to 2013-04-17 | 1022 | 1 | Sarkozy 28, Hollande 23, Le Pen 21 | http://www.lefigaro.fr/assets/pdf/OpinionwayHollandeunan.pdf |
| 2017_wp_opinionway_2017-02-17_1 | OpinionWay |  | 2017-02-13 to 2017-02-17 | 1500 | 1 | Le Pen 26, Fillon 20, Macron 20 | http://opinionlab.opinion-way.com/dokumenty/PresiTRACK-OpinionWay-ORPI-Resultats-semaine13-17-fev.pdf |
| 2017_wp_opinionway_2017-04-21_1 | OpinionWay |  | 2017-04-19 to 2017-04-21 | 1500 | 1 | Macron 23, Le Pen 22, Fillon 21 | http://opinionlab.opinion-way.com/dokumenty/PresiTRACK-OpinionWay-Orpi-Resultatsdelasemainedu17au21avril.pdf |
| 2017_wp_scan-research-le-terrain_2017-03-27_1 | Scan Research - Le Terrain |  | 2017-03-23 to 2017-03-27 | 586 | 1 | Macron 24.5, Le Pen 24, Mélenchon 19.5 | https://www.slideshare.net/mustaphasmail/la-perce-de-mlenchon |
| 2017_wp_tns-sofres_2015-12-15_1 | TNS Sofres |  | 2015-12-14 to 2015-12-15 | 1000 | 3 | Le Pen 26, Sarkozy 24, Hollande 19 | http://www.tns-sofres.com/etudes-et-points-de-vue/presidentielle-2017-intentions-de-vote-15-decembre-2015# |
