# Tzu Chi BMD website

This is an existing website, exported from published version 15. Continue its
design and implementation. The owner wants thoughtful refinements to the current
site. Read `MULAI-DI-CODEX.md`, `README.md`, and `SOURCE-VERSION.json` first.

## Project structure

- A static HTML/CSS/JavaScript site, with a Python generator; no npm build step.
- `build.py` renders English pages, then `localization.py` renders Traditional
  Chinese counterparts and translated interaction data.
- `dist/` contains the current ready-to-preview site and its local assets.
- `content/` contains source records, verified faculty names, translations, and
  maintained editorial content.
- `compact_editorial.py`, `content/compact-editorial.json`, and
  `dist/assets/edition.css` / `edition.js` implement the latest refinement.
- Page generators include `homepage.py`, `interior.py`, `student_life.py`,
  `internship_editorial.py`, and `global_learning.py`. Older presentation passes
  are still part of the build; follow the import order in `build.py`.
- Edit maintained generators, content, and original asset scripts. Rebuild
  generated HTML, `*-localized.js`, dictionaries, and search indexes afterward.

## Design preferences

- Preserve the established white/light-green/forest-green campus identity,
  branding, navigation structure, and existing features.
- Keep language concise, specific, and natural. Remove duplicated introductions
  and filler rather than adding generic marketing paragraphs.
- Strong Archivo headlines, readable Public Sans body text, and selected
  Newsreader serif headlines provide variety. Chinese text needs corresponding
  hierarchy and readable font sizes. Retain the local font licenses.
- Prefer varied editorial photo compositions and authentic department photos.
  Image tiles may open brief contextual stories with a few photos and sources.
- Preserve subtle image zoom/green wash, the homepage word/photo sequence, and
  gentle background motion with pause and reduced-motion behavior.
- Avoid repeated arrow decorations, excessive empty space, and uniform card
  grids everywhere. Desktop body text is generally 17px; mobile generally 16px.
- Student-life material is institutional page content, not a fabricated quote
  or testimonial. The Japan journal remains an optional example within the
  broader Beyond Campus page.

## Content and functionality

- Update English and Traditional Chinese together, including alt text, photo
  captions, dialog data, interactive labels, search text, and internal routes.
- Retain verified Chinese faculty names and English search aliases.
- Retain original publications, factual tables, source links, and document
  access. Never invent achievements, statistics, placements, or student stories.
- Historical programme notices must remain labelled as archives. Illustrative
  stock images must remain labelled and credited until replaced.
- Keep legacy account-access instructions excluded from public HTML and search.
- Preserve the clickable history years, accessible tabs, photo viewers,
  filtering/search, the Taiwan-date calendar, and the existing YouTube film.
- Photo replacement locations are documented in `content/*photo-slots.json`.

## Local workflow

1. The included `dist/` can be previewed immediately with `python preview.py`.
2. For rebuilding, use Python 3.12 and install the tested dependencies with
   `python -m pip install -r requirements.txt` (a virtual environment is useful).
3. After edits, run `python -X utf8 build.py`.
4. Run `python -X utf8 run_checks.py`. Node.js is used for JavaScript syntax
   checks; the site itself needs no Node runtime or npm dependencies.
5. Inspect affected desktop/mobile layouts and English/Chinese interactions
   when browser tooling supports them; describe verification limits accurately.

The portable tests use `content/portable-baseline.json` to check retained
publication bodies, tables, document URLs, and the pre-refinement copy baseline.
They work without the original Git history. The repository is connected to
https://github.com/redvallarie-source/TCU-BMD-Website. GitHub Pages publishes
`dist/` through `.github/workflows/pages.yml` on pushes to `main`; rebuild and
validate source changes before pushing. The VS Code entry point is
`BMD-Website.code-workspace`, with Live Server rooted at `dist/`. The portable
ZIP omits Git metadata and hosting credentials.
