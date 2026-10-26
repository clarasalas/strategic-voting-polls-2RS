# Finding the source documents

The links in `crosscheck_disagreements.csv` (`document_to_use`) and `spot_check_sample.csv` (`notice_url`,
`upstream_source_url`) are often wrong or dead, and 2002–2012 have none. These files are for finding a working
link for every poll in the two worklists, before checking them by hand.

* `prompt_2002.md` … `prompt_2022.md`: one self-contained prompt per election for a chatbot with web browsing
  (e.g. ChatGPT with search). Paste the whole file. It asks for one CSV block back:
  `poll_id,url,source_type,matches,archive_url,notes`.
* `polls_to_find.csv`: the same 200 polls in one table (`worklist` says which worklist each comes from).

Save each answer as `found_<year>.csv` in this folder. The links still have to be opened and checked by hand:
chatbots invent plausible URLs. Then copy the good ones into `document_url` in the worklists.
