"""Verify the broad gateway, explicit sources, and retired navigation routes."""
from pathlib import Path
from urllib.parse import urlsplit
from lxml import html as LH
import json
from navigation_consolidation import RETIRED

ROOT=Path(__file__).parent;D=ROOT/'dist';errors=[]
data=json.loads((ROOT/'content/global-learning.json').read_text())
for prefix in ['', 'zh-']:
    page=LH.parse(str(D/(prefix+'internships.html')))
    programme_ids=page.xpath('//*[@data-programme]/@data-programme')
    if set(programme_ids)!={'taiwan','malaysia','usa','uk','japan','academic'}:errors.append((prefix,'Programme coverage incomplete'))
    for item in page.xpath('//*[@data-programme]'):
        if not item.xpath('.//a[starts-with(@href,"https://mdm.tcu.edu.tw/")]'):errors.append((prefix,item.get('data-programme'),'Official source link missing'))
    story=page.xpath('//details[@id="japan-field-journal"]')
    if len(story)!=1 or story[0].get('open') is not None:errors.append((prefix,'Tokyo must be an optional case, closed by default'))
    if not page.xpath('//*[@id="global-opportunities"]'):errors.append((prefix,'General programme gateway missing'))
    if page.xpath('//*[contains(concat(" ",@class," ")," beyond-cover ")]//*[contains(concat(" ",@class," ")," intern-place-mark ")]'):errors.append((prefix,'Japan-specific masthead retained'))
    for p in data['photos'].values():
        image=page.xpath('//figure//img[@src=$path]',path=p['path'])
        if len(image)!=1:errors.append((prefix,'Global cover photo missing',p['path']))
    records=json.loads((D/('assets/search-index-zh.json' if prefix else 'assets/search-index.json')).read_text())
    urls={r['url'] for r in records}
    if any(prefix+old in urls for old in RETIRED):errors.append((prefix,'Removed page remains in search results'))
    beyond=next((r for r in records if r['url']==prefix+'internships.html'),{})
    if 'ViTrox' not in beyond.get('text',''):errors.append((prefix,'Broader content missing from search'))
    for old,new in RETIRED.items():
        alias=LH.parse(str(D/(prefix+old)))
        if alias.xpath('//meta[@name="bmd-redirect"]/@content')!=[prefix+new]:errors.append((prefix+old,'Wrong bookmark redirect'))
        if not alias.xpath('//meta[@name="robots" and @content="noindex,follow"]'):errors.append((prefix+old,'Alias must not be indexed'))

for path in D.glob('*.html'):
    page=LH.parse(str(path));prefix='zh-' if path.name.startswith('zh-') else ''
    expected=[prefix+'student-life.html',prefix+'internships.html',prefix+'careers.html']
    menus=page.xpath('//details[contains(concat(" ",@class," ")," nav-group ")]')
    student=menus[3]
    if student.xpath('.//a/@href')!=expected:errors.append((path.name,'Student Life menu is not the three intended destinations'))
    if path.name.removeprefix('zh-') in RETIRED:continue
    for link in page.xpath('//a[@href]'):
        if link.xpath('ancestor::*[contains(concat(" ",@class," ")," source-body ")]'):continue
        if urlsplit(link.get('href')).path.removeprefix('zh-') in RETIRED:errors.append((path.name,'Link still points to a removed standalone page',link.get('href')))

report={'source_linked_pathways':6,'countries_explicitly_named':['Taiwan','Malaysia','United States','United Kingdom','Japan'],'other_learning':'International workshop at BMD','student_life_menu_items':3,'bookmark_redirects':6,'languages':2,'errors':errors}
(ROOT/'global-learning-check-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
