# Content migration and source coverage

Captured on **30 October 2026**. The detailed, auditable URL inventory is in `content-audit.json`.

## Coverage

The redesign maps the **major English and Traditional Chinese menus and their discoverable pages** into a coherent department website. The capture includes:

| Source group | Captured URL/file records |
| --- | ---: |
| Official English pages | 64 |
| Complementary official Traditional Chinese pages | 14 |
| Latest Chinese announcements | 8 |
| Original user GitHub HTML pages | 4 |
| Failed official URL | 1 |

These are URL records, not a count of unique semantic pages. Aliases, language variants, and duplicate content can appear separately.

The captured material covers About/Introduction, Faculty and profiles, Curriculum and entry-year documents, Certification, Career paths, Student life, Virtual Corporation, News, Regulations, Internships, Admissions, International exchange, International students, Student outcomes, and Graduate destination tables.

## Source-to-page mapping

Every captured official source URL maps to `source-<sha1(full URL)[:12]>.html`. Full query strings are retained when deriving identifiers. Faculty profiles additionally map to `faculty-<sha1(profile URL)[:10]>.html`. The audit records the related curated core route for each source.

The agreed curated routes are: `index.html`, `introduction.html`, `vision.html`, `history.html`, `academics.html`, `curriculum.html`, `requirements.html`, `faculty.html`, `student-life.html`, `internships.html`, `exchange.html`, `international.html`, `outcomes.html`, `admissions.html`, `news.html`, `events.html`, `resources.html`, `regulations.html`, `contact.html`.

The four original GitHub pages are design/source references mapped to their corresponding curated page purpose. They are not treated as authoritative evidence for official academic facts.

## Documents, media, and external services

- 61 distinct linked document URLs are preserved as source resources.
- 19 distinct video/audio URLs and 0 iframe URLs were discovered.
- 209 distinct remote image references were inventoried.
- Eight genuine editorial photographs were inspected and optimized locally; eight latest original announcement posters were also captured. Faculty portrait download records are listed separately in the source research.

**External linked sites and documents remain their original destinations.** Their complete contents, application workflows, social feeds, or historical archives have not all been rehosted or transcribed. Image-only pages retain original posters/graphics and source links; text summaries do not imply complete OCR of every graphic.

## Source discrepancies and archival material

1. **History dates:** English introduction infographics show 1997/2002/2022 for three milestones, whereas other official academic records show 2000/2004/2023. The audit preserves both versions and source provenance. The agreed 2013 rename and 1 August 2024 merger are also recorded. Do not silently blend the discrepant dates.
2. **Language collision:** `/p/412-1021-64.php?Lang=en` is Virtual Corporation; the Traditional Chinese version of the same path is International Students. They must remain distinct sources.
3. **Legacy admissions:** International program material associated with 2019 refers to former TCUST/Marketing and Distribution Management and 128 credits. It belongs in a dated archive. Current and cohort-specific requirements come from the relevant current curriculum documents.
4. **Other dated resources:** Freshman orientation 2019 and online seminar 2022 are archival examples, not current event announcements. Previous-entry-year curriculum documents remain cohort-specific resources rather than automatically obsolete files.
5. **News dates:** No publication date is invented when the source does not expose one. Event dates, competition years, headline dates, and cache timestamps are not publication dates. The Chinese latest-section order is preserved separately from older English achievements.
6. **Graduate destinations:** Positive-outcome counts include employment, further study, or military service. They are not simple employment-only rates; tracked-student counts differ from cohort sizes.

## Known limits

The capture covered the major menus and linked pages to a bounded depth. English archive pages 1 and 2 were included; deeper pagination and **every external historical page were not exhaustively replicated**. There are 57 discovered internal URL variants not in the captured record set; that list includes print views, language variants, pagination, and possible additional content. See the JSON before treating these as substantive omissions.

One official English news URL returned HTTP 404: `https://mdm.tcu.edu.tw/p/406-1021-64534,r1.php?Lang=en`. Unavailable source content must remain clearly identified rather than reconstructed from guesses.

This audit documents captured evidence and agreed integration targets. It does not independently certify the final deployment or claim that all external content has been fully migrated.


## Content review update

One legacy account-access notice is excluded from publication and search; 85 of the 86 captured source records remain published. Historical notices appear under the explicit Archive filter.

The academic calendar now uses Asia/Taipei for month rollover and 32 selected entries checked against the retained 2026–2027 university PDF (revision 2026-06-26). The October 21 gathering is correctly scoped to the Jianguo programmes described in that PDF. The official calendar update page is linked.

Graduate-destination tables distinguish Business Management from the International Service Industry Management bachelor’s programme; the reported statuses include employment, further study and military service.

Curriculum PDFs with verified local copies can be previewed without embedding the university’s restricted origin. The original files remain linked. Publisher-listed PowerPoint sizes are shown as source metadata, rather than described as compressed PDFs.

Career Pathways was retired at the owner’s request on 14 November 2026. Its English and Traditional Chinese routes redirect to Life at BMD and are excluded from navigation and search. Original department source-reading pages remain available.
