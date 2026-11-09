"""Publication checks for the bilingual, photo-led campus refinement."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from collections import Counter
from lxml import html as LH
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).parent
D=ROOT/'dist'
errors=[]
pages={p.name:LH.parse(str(p)) for p in D.glob('*.html')}
asset_refs=0
links=0
preserved=0
baseline=json.loads((ROOT/"content/portable-baseline.json").read_text())
for name,tree in pages.items():
    if len(tree.xpath('//main//h1'))!=1:errors.append((name,'Expected one main heading'))
    ids=Counter(tree.xpath('//*[@id]/@id'))
    errors.extend((name,'Duplicate ID: '+v) for v,c in ids.items() if c>1)
    expected='zh-Hant' if name.startswith('zh-') else 'en'
    if tree.getroot().get('lang')!=expected:errors.append((name,'Wrong document language'))
    switch=tree.xpath('//a[contains(concat(" ",@class," ")," language-switch ")]')
    counterpart=name[3:] if name.startswith('zh-') else 'zh-'+name
    if len(switch)!=1 or switch[0].get('href')!=counterpart:errors.append((name,'Wrong language counterpart'))
    if tree.xpath('//*[contains(concat(" ",@class," ")," topline ")]'):errors.append((name,'Removed upper utility strip still present'))
    if not tree.xpath('//header//*[contains(concat(" ",@class," ")," header-actions ")]/a[contains(concat(" ",@class," ")," language-switch ")]'):errors.append((name,'Header language control missing'))
    if len(tree.xpath('//nav[@id="primary-nav"]/a[contains(concat(" ",@class," ")," nav-apply ")]'))!=1:errors.append((name,'Admissions navigation repeated or missing'))
    for el in tree.xpath('//*[@href or @src]'):
        for attr in ['href','src']:
            value=el.get(attr)
            if not value:continue
            url=urlsplit(value)
            if url.scheme or url.netloc:continue
            path=unquote(url.path)
            target=(D/path) if path else (D/name)
            if not target.exists():errors.append((name,'Missing local target: '+value))
            if attr=='href':links+=1
            if url.fragment and (not path or path.endswith('.html')) and target.exists():
                dest=pages.get(target.name)
                if dest is not None and not dest.xpath('//*[@id=$value]',value=url.fragment):errors.append((name,'Missing fragment: '+value))
            if attr in {'src','href'} and path.endswith(('.css','.js')) and target.exists():
                sha=hashlib.sha256(target.read_bytes()).hexdigest()[:12]
                if url.query!='v='+sha:errors.append((name,'Outdated asset fingerprint: '+value))
                asset_refs+=1
    if name.startswith('zh-'):
        en=pages[name[3:]]
        original=en.xpath('//*[contains(concat(" ",@class," ")," source-body ")]')
        translated=tree.xpath('//*[contains(concat(" ",@class," ")," source-body ")]')
        if [e.text_content() for e in original]!=[e.text_content() for e in translated]:errors.append((name,'Original publication body modified'))
        preserved+=len(original)
    else:
        after=tree.xpath('//*[contains(concat(" ",@class," ")," source-body ")]')
        hashes=[hashlib.sha256(' '.join(el.text_content().split()).encode()).hexdigest() for el in after]
        if hashes!=baseline['publication_bodies'].get(name,[]):errors.append((name,'Source content differs from the exported baseline'))
    public=(D/name).read_text()
    if re.search(r'password|密碼|帳號|7486dbf7229b|15640,r1',public,re.I):errors.append((name,'Excluded access content found'))
for index_name in ['search-index.json','search-index-zh.json']:
    records=json.loads((D/'assets'/index_name).read_text())
    for record in records:
        url=urlsplit(record['url'])
        if not url.scheme and not (D/url.path).exists():errors.append((index_name,'Missing search result: '+record['url']))
    if re.search(r'password|密碼|帳號|7486dbf7229b|15640,r1',json.dumps(records,ensure_ascii=False),re.I):errors.append((index_name,'Excluded access content found'))
for page in ['index.html','zh-index.html']:
    t=pages[page]
    data=json.loads(t.xpath('//script[@id="calendar-data"]')[0].text)
    if len(data)!=32:errors.append((page,'Calendar records changed'))
    if not t.xpath('//button[@data-film-play]'):errors.append((page,'Video play control missing'))
    if not t.xpath('//a[@href="https://www.youtube.com/watch?v=8ODH3C1lykA"]'):errors.append((page,'User-selected video link missing'))
    for region in ['editorial-motion','home-final-shell']:
        if not t.xpath('//*[contains(concat(" ",@class," "),$region)]//*[contains(concat(" ",@class," ")," ambient-layer ")]',region=' '+region+' '):errors.append((page,'Moving green background missing: '+region))
for p in D.glob('assets/*.js'):
    result=subprocess.run(['node','--check',str(p)],capture_output=True,text=True)
    if result.returncode:errors.append((p.name,result.stderr))
report={'pages':len(pages),'checked_local_links':links,'versioned_asset_references':asset_refs,'original_publication_bodies_preserved':preserved,'errors':errors}
(ROOT/'refinement-check-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
