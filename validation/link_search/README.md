<h1 align="center">validation/link_search</h1>

<p align="center">
How a working link to the original document was found for every poll in the two worklists, before checking them by
hand.
</p>

<p align="center"><sub><a href="../README.md">← Back to validation</a></sub></p>

## What is in here

The links in `crosscheck_disagreements.csv` (`document_to_use`) and `spot_check_sample.csv` (`notice_url`,
`upstream_source_url`) were often wrong or dead, and 2002–2012 had none.

| File | What it holds |
|---|---|
| `prompt_2002.md` … `prompt_2022.md` | one self-contained prompt per election for a chatbot with web browsing |
| `prompt_2012_retry.md` | a second pass for the 12 polls of 2012 the first search did not reach |
| `polls_to_find.csv` | the same 200 polls in one table (`worklist` says which worklist each comes from) |
| `found_{year}.csv` | the answers, one CSV per election |

## How it was used

Each prompt is pasted whole into a chatbot with search (ChatGPT, for example). It asks for one CSV block back:
`poll_id,url,source_type,matches,archive_url,notes`. Each answer is saved as `found_<year>.csv` in this folder,
then, from the repository root:

```bash
PYTHONPATH=src python -m polls.links
```

It copies the links into `document_url` in both worklists (only where it is empty, so links typed by hand are
kept) and adds two columns: `link_check` (source type and the chatbot's own `matches`, or `not_found`) and
`link_notes`. The poll ids here are Wikipedia ids: they match `poll_id_wikipedia` in
`crosscheck_disagreements.csv` and `poll_id` in `spot_check_sample.csv`.

The links still have to be opened and the verdicts filled in by hand: chatbots invent plausible URLs.

Answers to the retry prompt go in `found_2012_retry.csv`: when a poll appears in several files, the file that sorts
last wins.
