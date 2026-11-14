# Portable Codex desktop project — BMD v15

Website: **https://redvallarie-source.github.io/TCU-BMD-Website/**

Untuk Visual Studio Code, buka **BMD-Website.code-workspace** di folder ini.
Halaman utama BMD adalah **dist/index.html**. Live Server diarahkan ke `dist/`.
File `index.html` pada folder di luar proyek ini adalah proyek Whisper Tour
yang terpisah, bukan halaman utama BMD.

Mulai dari **MULAI-DI-CODEX.md** untuk petunjuk dalam bahasa Indonesia.
Open this entire folder in the Codex app. `AGENTS.md` records the existing
website and the owner's accepted design preferences.

Quick preview (standard-library Python only):

```bash
python preview.py
```

Rebuild and validate (tested with Python 3.12; Node.js for JS syntax checks):

```bash
python -m pip install -r requirements.txt
python -X utf8 build.py
python -X utf8 run_checks.py
```

The ready-built website is in `dist/`. GitHub Pages publishes this directory
when a commit is pushed to `main`. Rebuild and validate maintained-source changes
before pushing. The portable ZIP excludes Git metadata and hosting credentials.
The portable verification scripts compare immutable publication data with
`content/portable-baseline.json`, rather than requiring the hosted Git history.
The development history below describes the retained implementation.

---

# TCU Business Management — student redesign

This is a complete static website project, designed for GitHub Pages or static hosting. The published content is in `dist/`. It uses HTML, CSS and JavaScript without a frontend build dependency.

## Use on GitHub Pages

GitHub Pages is enabled with **GitHub Actions** as its source. The workflow in `.github/workflows/pages.yml` publishes `dist/` when a commit is pushed to `main`, or when started manually. The public website is `https://redvallarie-source.github.io/TCU-BMD-Website/`.

The workflow publishes the already-built site; after editing maintained sources, rebuild with `python -X utf8 build.py` and include the updated `dist/` files in the push. Open the site through HTTP; the global search loads its local JSON index with fetch and therefore requires a web server.

## Editing

- `dist/assets/style.css`: visual identity, page layouts and responsive rules.
- `dist/assets/site.js`: navigation, search, filters, timeline and academic calendar.
- `homepage.py`: homepage composition with campus slideshow, information and news carousels, and the embedded academic calendar.
- `dist/assets/homepage.css` and `dist/assets/homepage.js`: homepage styling and slider interactions, including keyboard controls and reduced-motion support.
- `dist/assets/refinement.css`: retained baseline styling. `dist/assets/edition.css` now supplies the active Archivo, Public Sans, and Newsreader typography.
- `dist/assets/refinement.js`: homepage entrance transitions, ambient background animation visibility, and the background motion pause control. The student-life and final admissions sections carry the moving backgrounds; the photo hero retains its own slideshow controls.
- `interior.py`: source-preserving layouts for the About pages, academic explorer, cohort document groups, faculty directory, student photo journal, and other interior pages.
- `dist/assets/interior.css` and `dist/assets/interior.js`: interior presentation and interactions, including illustrated history chapters, cohort expansion, document pagination and the student-life photo viewer.
- `editorial.py` and `dist/assets/finishing.css`: plain page labels, concrete activity captions, purpose-specific navigation icons, and the quieter visual finish. Homepage slide copy is generated into the page so the initial text and slideshow use the same source.
- `content_support.py`: document availability states, graduate programme labels, source-backed international experiences, original-file metadata and verified PDF preview buttons.
- `content/academic-events.json`, `calendar_data.py`, and `dist/assets/calendar-date.js`: selected dates checked against the retained university PDF, calendar HTML rendered for Taiwan time, and client-side month rollover. The calendar covers August 2026 to July 2027 and links to the university's calendar update page.
- `content/document-previews.json`: provenance and hashes for the curriculum PDFs available as local previews. Original university download links remain available. Files that could not be verified are not offered as embedded previews.
- `build.py`: generates all HTML pages and search data from retained content.
- `content/`: captured source data and existing-site inputs used by the generator.
- `CONTENT-MIGRATION.md` and `content-audit.json`: scope and provenance notes.

To regenerate: use Python 3 with `lxml` installed and run `python build.py`. Optimized images are retained in `dist/assets/`; image downloading is not required to rebuild.

## Source scope

The site contains curated department pages, 37 faculty/staff profiles, original document links, news summaries and posters, an academic calendar, and a searchable source collection. Archived 2019/2022 materials are labelled. One linked news article returned HTTP 404 and three legacy-hosted photos returned HTTP 503. External university systems and documents remain linked to their original publications. Every route has an English and Traditional Chinese presentation. The language switch retains the current page and fragment. Original source bodies, personal names, some qualifications, document titles and files retain their publication language, with a note where appropriate.

The existing public GitHub website was used as a reference and has not been overwritten by this project.

One historical notice with account-access instructions is excluded from both published content and search. Other historical department notices are labelled and separated from the default news feed. This yields 85 published source-reading pages from the 86 captured records.

## Fonts

The local Latin subsets of Manrope and DM Sans originate from the official Google Fonts repository (`ofl/manrope` and `ofl/dmsans`). Copyright notices and the SIL Open Font License 1.1 are included beside the font files in `dist/assets/fonts/`. Chinese text uses the reader's system font. No external font request is needed at runtime.


## Editorial refinement

`personality.py` applies final page-specific copy and photo captions after the existing content-support pass. `assets/editorial.css` refines the established layouts without changing the shared palette or font system. The student-life gallery, introduction, project notes and international accounts use distinct compositions. Photography stays attributed to the department archive; the Indonesian-cohort presentation image is identified accurately.

Header Admissions uses one anchor across desktop/mobile. Home learning cards deep-link to the matching academic tabs. Taiwan calendar logic and exclusion guards remain in the build. `editorial-check-report.json` records the latest responsive and functional QA; `external-link-report.json` records all 217 unique external URL checks, including 44 unverified responses. A rejected HEAD request is not treated as evidence of a broken URL.


## Cinematic and editorial motion

`motion_design.py` refines seven presentation pages after the retained editorial pass. `assets/campus-motion.css` and `assets/campus-motion.js` provide slow campus-photo movement, a synchronized vertical-word/photo feature, selected heading entrances and gentle desktop photo travel. The opening uses the existing campus photographs. A separate section below the learning directions loads the user-selected official TCU YouTube film only after pressing Play. Reference footage from the department was reviewed but its older identity and baked-in graphic/news text did not suit the main background.

The hero and student-life feature have separate pause controls. Device reduced-motion settings, hidden tabs and offscreen regions are respected; text remains readable without JavaScript. The homepage keeps its section order and existing carousels/calendar. CSS and script URLs now use content hashes. `motion-check-report.json` records scope, functional QA and responsive checks.


## Quieter UI details

`quiet_ui.py` removes repeated decorative diagonal markers, shared link-arrow SVGs and repeated navigation pictograms from the generated presentation layer. Arrow controls for genuine directional actions remain. Original source-body text, every link destination, every button and embedded interactive JSON are preserved. `assets/quiet-ui.css` provides text-led links, a lighter four-column academic index, simpler photo actions and document rows without pseudo-arrow icons. The established branding, motion, navigation and section order remain.

The homepage has zero decorative diagonal markers (previously 33). The source and interaction preservation checks, mobile/tablet QA and sampled counts are recorded in `quiet-ui-check-report.json`. Harvard Business School and Oxford Saïd were reviewed as design references; their content and assets were not imported.


## Compact, bilingual campus refinement

`campus_refinement.py` adds the lower-home video, career photography and abstract campus silhouettes after the retained motion pass. `dist/assets/campus-refinement.css` is the final presentation layer: white primary surfaces, closer spacing, a consistent gentle photo hover, and responsive Chinese typography. The new interior background motion has its own pause control and respects reduced-motion and data-saving preferences.

`localization.py` generates the `zh-*.html` counterparts and `assets/search-index-zh.json`. Curated translations live in `content/translations-zh-Hant.txt` as `English | Traditional Chinese` lines. Dynamic calendar, timeline, search, filters, captions and motion controls use the same dictionary. The `*-localized.js` assets are generated from the original maintained JavaScript; edit the original scripts, then rebuild.

Replace `assets/photos/career-collaboration.webp` and `career-hospitality.webp` with your own photographs when available. Their captions currently identify them as illustrative stock photography. Credits and source URLs are recorded in `assets/photos/source-manifest.json`. The homepage film uses YouTube video `8ODH3C1lykA`, published by TCU OGA. Its local poster is 1280 × 720; the iframe is created only on demand and a direct YouTube link remains available.

Run `python build.py` followed by `python verify_refinement.py` before publication. The latter checks all 318 pages, local destinations, fragment IDs, versioned assets, language counterparts, search records, exclusion guards, original source body preservation and JavaScript syntax. Browser QA covers the desktop layouts, language switch, Mandarin search, filters, history years, learning tabs, captions and Taiwan calendar. The cloud browser renders the YouTube player but streaming remained at 0:00; playback is not claimed as verified. Browser viewport resizing was unavailable, so the responsive breakpoint changes were inspected in source rather than claimed as device-tested.


## Navigation, cinema and restored green motion

The upper utility strip is removed. The language switch sits beside Search in the shared header, with compact labels on phones. Every English/Chinese counterpart retains the same route and fragment behavior.

The lower-home film now spans the content viewport, with a dark green surround and a stable widescreen frame before and after Play. The existing student-life photo/word sequence is retained, with a larger photograph.

Green contours and moving gradients are visible again in student life and the closing admission section. The same motion is applied behind the existing introduction approach and admissions FAQ, with white retained elsewhere. The homepage foreground and background controls share pause state. Interior controls synchronize with each other; offscreen, hidden-tab, reduced-motion and data-saving rules remain active.


## Student-life journal and official Chinese faculty names

`student_life.py` and `assets/student-life.css` create a photo-led Life at BMD page from the site owner's editorial brief. The copy covers accounting, financial decisions, management, leadership, sustainability, presentations, podcast work, final projects, internships, NPOs and volunteering. It is institutional copy, not a testimonial or an attributed student quotation. Interactive project tabs share the existing photo viewer; `assets/student-life.js` handles keyboard selection and translated panel updates.

The Myanmar-relief fair and Tokyo service-learning examples are linked to official TCU publications. Their real photographs carry source credits. The Thailand destination comes from the owner's brief; no current host, date, funding or guaranteed place is invented. Current placement enquiries go to the department.

`content/student-life-photo-slots.json` names the ten independent image files for later replacement. All are under `assets/life/`, so replacing a Life at BMD image does not alter Home or other pages. Update the corresponding captions and alt text in `student_life.py` and the Traditional Chinese dictionary to match new photos.

`content/faculty-verified.json` records 37 official Chinese names, corresponding profile sources, and four faculty additions found in the current Chinese listing. `faculty_update.py` preserves the earlier source records while applying verified names and current listing order to the curated directory. Chinese names appear on cards, profile headings, image alt text and search results. Directory filtering and search accept both English and Chinese names. One newly listed email duplicated with the chair was omitted rather than assigned to another person.

Run `python verify_faculty_life.py` as well as `python verify_refinement.py` after rebuilding. Original source collection bodies remain in their publication language.


## Internship field journal (November 2026)

The internship page combines current official BMD preparation resources with a participant-provided Tokyo 2026 journal and presentation. The usual 09:00–17:00 office window applies to the featured placement, not all internships. Four accessible work-area tabs, a six-photo viewer, optional ambient motion, and original document search are available in English and Traditional Chinese.

Edit copy, Chinese translations, source provenance and photo captions in `content/internship-editorial.json`. Replace the six independent image files listed in `content/internship-photo-slots.json`; these do not share image paths with Home or Life at BMD. The full personal report is not shipped. All 32 existing internship document URLs remain available, with readable document titles.

Run `python build.py`, `python verify_internships.py`, and `python verify_refinement.py` after updates. Mobile breakpoints are included; browser QA in this change used the supported desktop viewport.


## Beyond Campus consolidation (November 2026)

The Student Life menu has two destinations: Life at BMD and Beyond Campus. Career Pathways was removed at the owner’s request; old career-page bookmarks redirect to Life at BMD. Beyond Campus retains the stable `internships.html` route and covers Taiwan placement guidance, ViTrox in Malaysia, the 2025 US notice, Nottingham Trent summer learning, the 2026 Japan notice, and international academic contact at BMD. Every entry links directly to an official department source or published film. Records are clearly distinguished from open applications.

The detailed Tokyo journal keeps the approved photography and interactions inside an optional expandable case. It opens automatically for its own section links and older Tokyo anchors. Cover copy, programme rows, sources, and two independent cover-photo slots live in `content/global-learning.json`; the Japan case remains in `content/internship-editorial.json`.

The former Exchange, Student Projects, and International Students pages are no longer standalone destinations or search results. Their old URLs redirect to the consolidated gateway, the project section within Life at BMD, and Admissions respectively. Original publication archives remain intact. `navigation_consolidation.py` updates internal links without editing original source bodies. Run `python verify_global_learning.py` alongside the existing checks after changes.


## Compact editorial edition (November 2026)

`compact_editorial.py` is the last curated-content pass before page generation and localization. Copy and brief story data live in `content/compact-editorial.json`. It removes redundant introductions, simplifies academic/resource navigation, and keeps the original publication bodies and factual tables intact. The internship preparation paragraphs are replaced by one expandable shelf containing all 32 original forms.

`assets/edition.css` applies the final type hierarchy and spacing. Archivo is used for display/navigation, Public Sans for reading, and Newsreader for selected editorial headlines; selected Chinese headings use a local Noto Serif TC subset. Fonts are self-hosted with SIL OFL notices and provenance in `content/editorial-font-provenance.json`. Shared baseline files remain available but no longer determine the active font variables.

Home learning areas, two introduction features, career photography, and the six Beyond Campus experiences open brief native dialog stories through `assets/edition.js`. Stories contain one concise paragraph, one to three photographs, and relevant source links. The image links retain real destination fallbacks without JavaScript, modified-click behavior, native keyboard controls, and focus restoration. Green photo washes replace the reference site's red identity. Stock images are labelled as illustrative and credited.

Story summaries stay in both search indexes even though they are presented in dialogs. Traditional Chinese translations include interactive text and local story destinations. `verify_compact_editorial.py` checks bilingual story/photo coverage, search inclusion, source fallbacks, font assets, and the reduction of visible curated paragraphs. Run it together with `verify_refinement.py`, `verify_faculty_life.py`, `verify_global_learning.py`, and `verify_internships.py` after rebuilding. The internship guard now compares retained publication bodies and factual tables rather than requiring unrelated curated copy to remain unchanged, since this edition intentionally edits the whole site.

Browser QA for this edition covered desktop Home, Introduction, Life at BMD, Academics, Beyond Campus, Faculty, and History, including an English photo story, a Mandarin programme story, filtering, document search, global search, native dialog closing, and a history-year change. Loaded fonts and computed text sizes were checked. Responsive source rules were reviewed; device viewport emulation was unavailable. Existing film playback and all remote historical links were not re-certified in this typography/copy edit.
