"""Check the new field journal, full bilingual copy and retained document access."""
import json
import hashlib
import re
import subprocess
from pathlib import Path
from lxml import html as LH
from PIL import Image
from navigation_consolidation import RETIRED

ROOT=Path(__file__).parent
D=ROOT/'dist'
material=json.loads((ROOT/'content/internship-editorial.json').read_text())
errors=[]
baseline=json.loads((ROOT/'content/portable-baseline.json').read_text())
original_files=set(baseline['internship_documents'])
expected_photos=len(material['photos'])+2  # Two existing global-learning cover photographs.
for name in ['internships.html','zh-internships.html']:
    tree=LH.parse(str(D/name));zh=name.startswith('zh-')
    files=set(tree.xpath('//*[@data-filter-item][self::a]/@href'))
    if files!=original_files:errors.append((name,'Original document URL set changed'))
    tabs=tree.xpath('//*[@data-intern-tab]')
    panels=tree.xpath('//*[@role="tabpanel"]')
    if len(tabs)!=4 or len(panels)!=4:errors.append((name,'Expected four linked work areas'))
    for tab in tabs:
        panel=tree.xpath('//*[@id=$id]',id=tab.get('aria-controls'))
        if len(panel)!=1 or panel[0].get('aria-labelledby')!=tab.get('id'):errors.append((name,'Broken tab relationship'))
        if len(panel)==1 and len(panel[0].xpath('.//*[@data-gallery-open]'))!=1:errors.append((name,'Each work tab must contain exactly one photograph',tab.get('id')))
    if tree.xpath('//*[@role="tabpanel"][@hidden]'):errors.append((name,'Work content must be readable without JavaScript'))
    if len(tree.xpath('//*[@id="photo-dialog"]'))!=1:errors.append((name,'Photo viewer missing'))
    if len(tree.xpath('//*[@data-gallery-open]'))!=expected_photos:errors.append((name,'Independent photograph count changed'))
    if tree.xpath('//main//blockquote'):errors.append((name,'Feature must not become a testimonial'))
    if len(tree.xpath('//*[@data-ambient-surface]'))!=1:errors.append((name,'Expected one purposeful motion region'))
    for key,p in material['photos'].items():
        image=tree.xpath('//main//figure//img[@src=$src]',src=p['path'])
        alt=material['translations'][p['alt']] if zh else p['alt']
        if len(image)!=1 or image[0].get('alt')!=alt:errors.append((name,'Wrong photo/alt: '+key))
        width,height=Image.open(D/p['path']).size
        if (int(image[0].get('width')),int(image[0].get('height')))!=(width,height):errors.append((name,'Wrong image dimensions: '+key))
    if zh:
        text=tree.xpath('//main//text()[not(ancestor::svg|ancestor::script)]')
        untranslated=[str(x).strip() for x in text if re.search('[A-Za-z]{3,}',re.sub(r'ViTrox|PDF|DOCX','',str(x))) ]
        if untranslated:errors.append((name,'Untranslated visible text',untranslated))
    public=(D/name).read_text()
    if re.search(r'1113114204|113114204|Mr\. Yu|于先生|熊本地震|Untitled document\.pdf',public):errors.append((name,'Unneeded private or unverified report detail leaked'))

# This refinement intentionally updates curated copy across the website.
# Published source bodies and factual tables remain unchanged.
preserved_sources=0
preserved_tables=0
for page in D.glob('*.html'):
    after=LH.parse(str(page))
    # The labelled certificate reading aid is new presentation, not a published
    # table. Both original certificate tables still participate in this guard.
    for selector,label,key in [('//*[contains(concat(" ",@class," ")," source-body ")]','Published source content','publication_bodies'),('//main//table[not(contains(concat(" ",normalize-space(@class)," ")," certificate-table "))]','Published table','tables')]:
        current_values=[hashlib.sha256(' '.join(e.text_content().split()).encode()).hexdigest() for e in after.xpath(selector)]
        # Retired curated pages are empty redirects. Original source-reading
        # pages and their factual tables remain protected by the baseline.
        previous_values=[] if key=='tables' and page.name.removeprefix('zh-') in RETIRED else baseline[key].get(page.name,[])
        if previous_values!=current_values:errors.append((page.name,label+' changed'))
        if label=='Published source content':preserved_sources+=len(current_values)
        else:preserved_tables+=len(current_values)

report={'languages':2,'work_areas_per_language':4,'photos_per_work_tab':1,'independent_photos':expected_photos,'original_document_urls_retained':len(original_files),'published_bodies_preserved':preserved_sources,'published_tables_preserved':preserved_tables,'errors':errors}
(ROOT/'internship-check-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
