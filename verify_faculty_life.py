"""Verify official-name coverage, bilingual search and the student-life interaction data."""
from pathlib import Path
import hashlib
import json
import re
from lxml import html as LH
from faculty_update import update_roster

root=Path(__file__).parent;dist=root/'dist';content=root/'content';errors=[]
authority=json.loads((content/'faculty-verified.json').read_text())['people']
roster=update_roster(json.loads((content/'official-en/faculty-roster.json').read_text()),content)
en_dir=LH.parse(str(dist/'faculty.html'));zh_dir=LH.parse(str(dist/'zh-faculty.html'))
cards=zh_dir.xpath('//article[contains(concat(" ",@class," ")," person ")]')
names=[p.xpath('.//h3')[0].text_content().strip() for p in cards]
if set(names)!={p['name_zh'] for p in authority}:errors.append('Chinese directory does not match the verified official-name set')
if len(cards)!=len(roster):errors.append('Faculty count differs between language versions')
indices={lang:json.loads((dist/'assets'/file).read_text()) for lang,file in [('en','search-index.json'),('zh','search-index-zh.json')]}
for person in authority:
    f=next(f for f in roster if re.sub(r'^Dr\.\s*','',f['name']).split(',')[0]==person['name_en'])
    name='faculty-'+hashlib.sha1(f['url'].encode()).hexdigest()[:10]+'.html'
    t=LH.parse(str(dist/('zh-'+name)))
    if t.xpath('//main//h1')[0].text_content().strip()!=person['name_zh']:errors.append('Wrong Chinese profile heading: '+person['name_en'])
    for lang,path in [('en',name),('zh','zh-'+name)]:
        record=next((r for r in indices[lang] if r['url']==path),None)
        if not record or person['name_zh'] not in (record['title']+' '+record['text']):errors.append('Chinese faculty name absent from search: '+path)
        if lang=='zh' and record and person['name_en'] not in record['text']:errors.append('English faculty alias absent from Chinese search: '+path)
for name in ['student-life.html','zh-student-life.html']:
    tree=LH.parse(str(dist/name));data=json.loads(tree.xpath('//script[@id="life-project-data"]')[0].text)
    if len(data)!=3:errors.append('Project choices missing: '+name)
    if len(tree.xpath('//*[@data-gallery-open]'))<8:errors.append('Photo collage slots missing: '+name)
    if len(tree.xpath('//dialog[@id="photo-dialog"]'))!=1:errors.append('Photo viewer missing: '+name)
    if tree.xpath('//blockquote'):errors.append('Student-life copy incorrectly formatted as a testimonial: '+name)
    if tree.xpath('//*[@id="life-project-title"]')[0].text!=data[0]['title']:errors.append('Initial project title and data differ: '+name)
    for topic in ['life-learning','life-projects','life-international','life-community']:
        if not tree.xpath('//*[@id=$topic]',topic=topic):errors.append('Topic missing: '+topic)
    if name.startswith('zh-'):
        for item in data:
            if not re.search('[\u4e00-\u9fff]',item['body']):errors.append('Untranslated interactive project body')
report={'verified_faculty_names':len(authority),'faculty_profiles_checked':len(roster),'student_life_languages':2,'photo_slots':len(LH.parse(str(dist/'student-life.html')).xpath('//*[@data-gallery-open]')),'errors':errors}
(root/'faculty-life-check-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
