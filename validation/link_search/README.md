# Finding the source documents

The links in `crosscheck_disagreements.csv` (`document_to_use`) and `spot_check_sample.csv` (`notice_url`,
`upstream_source_url`) are often wrong or dead, and 2002–2012 have none. These files are for finding a working
link for every poll in the two worklists, before checking them by hand.

* `prompt_2002.md` … `prompt_2022.md`: one self-contained prompt per election for a chatbot with web browsing
  (e.g. ChatGPT with search). Paste the whole file. It asks for one CSV block back:
  `poll_id,url,source_type,matches,archive_url,notes`.
* `polls_to_find.csv`: the same 200 polls in one table (`worklist` says which worklist each comes from).

Save each answer as `found_<year>.csv` in this folder, then run, from the repository root:

```bash
PYTHONPATH=src python -m polls.links
```

It copies the links into `document_url` in both worklists (only where it is empty, so links typed by hand are
kept) and adds two columns: `link_check` (source type and the chatbot's own `matches`, or `not_found`) and
`link_notes`. The poll ids here are Wikipedia ids: they match `poll_id_wikipedia` in
`crosscheck_disagreements.csv` and `poll_id` in `spot_check_sample.csv`.

The links still have to be opened and the verdicts filled in by hand: chatbots invent plausible URLs.

`prompt_2012_retry.md` is a second pass for the 12 polls of 2012 that the first search did not reach. Save its
answer as `found_2012_retry.csv`: when a poll appears in several files, the file that sorts last wins.
