"""Check concise bilingual story data and retained factual access after the edition."""
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit
from lxml import html as LH
from PIL import Image

ROOT=Path(__file__).parent
D=ROOT/'dist'
errors=[]
totals={'previous_paragraph_words':0,'current_paragraph_words':0}
counts={}
baseline=json.loads((ROOT/'content/portable-baseline.json').read_text())
index={prefix:{r['url']:r for r in json.loads((D/('assets/search-index-zh.json' if prefix else 'assets/search-index.json')).read_text())} for prefix in ['', 'zh-']}

def prose_count(tree):
    return sum(len(e.text_content().split()) for e in tree.xpath('//main//p[not(ancestor::dialog or ancestor::details or ancestor::script)]'))

primary=['index','introduction','vision','history','academics','student-life','internships','careers','faculty','admissions','curriculum','requirements','resources','regulations','news','events','contact']
for page in primary:
    path=page+'.html'
    previous=baseline['paragraph_baseline'][path]
    current=prose_count(LH.parse(str(D/path)))
    totals['previous_paragraph_words']+=previous
    totals['current_paragraph_words']+=current
    counts[path]={'before':previous,'after':current}

stories_checked=0
for prefix in ['', 'zh-']:
    for page,expected in [('index',4),('introduction',2),('internships',6),('careers',1)]:
        path=prefix+page+'.html'
        tree=LH.parse(str(D/path))
        data=json.loads(tree.xpath('//script[@id="editorial-story-data"]')[0].text)
        ids={s['id'] for s in data}
        if len(ids)!=expected:errors.append((path,'Story count changed'))
        triggers=tree.xpath('//*[@data-story-open]')
        if {t.get('data-story-open') for t in triggers}!=ids:errors.append((path,'Missing story trigger'))
        if len(tree.xpath('//dialog[@id="edition-story-dialog"]'))!=1:errors.append((path,'One detail dialog expected'))
        for trigger in triggers:
            href=trigger.get('href','')
            target=urlsplit(href)
            if not href:errors.append((path,'No-JavaScript fallback missing'))
            elif not target.scheme and target.path and not (D/target.path).exists():errors.append((path,'Broken fallback: '+href))
        for s in data:
            stories_checked+=1
            if len(s['body'].split())>65:errors.append((path,s['id'],'Summary exceeds 65 words'))
            if not 1<=len(s['images'])<=3:errors.append((path,s['id'],'Photo count must be 1–3'))
            if prefix and not re.search('[\u4e00-\u9fff]',s['body']):errors.append((path,s['id'],'Mandarin summary missing'))
            if s['body'] not in index[prefix][path]['text']:errors.append((path,s['id'],'Story summary absent from search'))
            for p in s['images']:
                if not (D/p['src']).exists():errors.append((path,p['src'],'Missing image'));continue
                if Image.open(D/p['src']).size!=(p['width'],p['height']):errors.append((path,p['src'],'Image dimensions wrong'))
                if not p['alt'] or not p['caption']:errors.append((path,p['src'],'Accessible photo context missing'))
            for link in s['links']:
                target=urlsplit(link['href'])
                if not target.scheme and target.path:
                    if not (D/target.path).exists():errors.append((path,'Missing story destination',link))
                    if prefix and not target.path.startswith('zh-'):errors.append((path,'Story link leaves Chinese edition',link))
        if not tree.xpath('//link[contains(@href,"assets/edition.css")]'):errors.append((path,'Editorial style missing'))
        if not tree.xpath('//script[contains(@src,"assets/edition.js")]'):errors.append((path,'Story interaction missing'))
    internships=LH.parse(str(D/(prefix+'internships.html')))
    if internships.xpath('//*[contains(concat(" ",@class," ")," intern-preparation ")]//h3'):errors.append((prefix,'Removed preparation boilerplate remains'))
    if len(internships.xpath('//details[contains(concat(" ",@class," ")," intern-resources ")]//a[@data-filter-item]'))!=32:errors.append((prefix,'32 internship forms must remain available'))

reduction=1-totals['current_paragraph_words']/totals['previous_paragraph_words']
if reduction<.25:errors.append('Curated visible paragraphs were not meaningfully shortened')
for font in ['archivo-latin','public-sans-latin','newsreader-latin','newsreader-italic-latin','noto-serif-tc-headings']:
    if not (D/'assets/fonts'/(font+'.woff2')).exists():errors.append('Missing font '+font)
for license in ['archivo','publicsans','newsreader','notoseriftc']:
    if not (D/'assets/fonts'/(license+'-OFL.txt')).exists():errors.append('Missing font license '+license)
report={**totals,'visible_paragraph_reduction_percent':round(reduction*100,1),'bilingual_stories_checked':stories_checked,'curated_pages':counts,'errors':errors}
(ROOT/'compact-editorial-check-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
