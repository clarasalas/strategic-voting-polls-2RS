<h1 align="center">docs</h1>

<p align="center">
The interactive page, and the plan of the study with every decision taken along the way.
</p>

<p align="center"><sub><a href="../README.md">← Back to the project</a></sub></p>

## What is in here

| File | What it holds |
|---|---|
| `index.html` | the interactive page, published with GitHub Pages: the story of the five campaigns, from notebooks 05 and 06. Generated: do not edit by hand |
| [`study_plan.md`](study_plan.md) | the purpose of the study; the foundations (what a poll, a party, a slot and a ballot scenario are, the time axis, the poll average); the three parts with what each block measures; conventions; limits |

Read the study plan for the *why* behind a choice. The *how* is in the notebooks, which follow its blocks in order, and the
numbers are in [`results/tables/`](../results/README.md).

<details>
<summary><strong>The interactive page</strong><br>Rebuilding and publishing it</summary>

<br>

`index.html` is built by `src/polls/page.py` from the final dataset and the tables in `results/tables/`, with the
text, the style and the charts in `src/polls/page_template.html`. Edit the template, then rebuild:

```bash
PYTHONPATH=src python -m polls.page
```

The file is standalone (data and charts embedded; only the font is loaded from Google Fonts), so it also opens
directly in a browser. It shows one topic at a time, chosen in a sidebar (a row of buttons on a phone), in three groups: concentration,
how the races unfolded, how accurate the polls were. Each topic has its own link (`#concentration`, `#runoff`…). The
parameters of notebook 07 are left out. Candidates who withdrew are drawn
when they have at least 5 polls with the full ballot in the window and a poll average reaching 2%.

**Publish.** On GitHub, open **Settings → Pages**, set **Source** to **Deploy from a branch**, select `main` and
`/docs`, and save. The page is then live at <https://clarasalas.github.io/strategic-voting-polls-2RS/>, and every
push of a rebuilt `docs/index.html` to `main` redeploys it.

</details>
