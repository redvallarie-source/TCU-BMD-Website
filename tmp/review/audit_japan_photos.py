from pathlib import Path
from collections import defaultdict
from PIL import Image
from lxml import html as LH
import json,hashlib

root=Path(__file__).resolve().parents[2];dist=root/'dist'
selected=json.loads((root/'content/japan-photo-selection.json').read_text(encoding='utf-8'))
material=json.loads((root/'content/internship-editorial.json').read_text(encoding='utf-8'))
paths={p['path'] for p in selected['photos'].values()}|{p['path'] for p in material['photos'].values()}
placements=defaultdict(list)
for page in ('student-life.html','internships.html'):
    for im in LH.parse(str(dist/page)).xpath('//main//img[not(ancestor::dialog)]'):
        if im.get('src') in paths:placements[im.get('src')].append(page)
hashes=defaultdict(list)
for path in paths:hashes[hashlib.sha256((dist/path).read_bytes()).hexdigest()].append(path)
def signature(path):
    im=Image.open(dist/path).convert('L').resize((9,8))
    return sum(1<<(y*8+x) for y in range(8) for x in range(8) if im.getpixel((x,y))>im.getpixel((x+1,y)))
perceptual={p:signature(p) for p in sorted(paths)}
pairs=[{'first':a,'second':b,'distance':(perceptual[a]^perceptual[b]).bit_count()} for i,a in enumerate(perceptual) for b in list(perceptual)[i+1:]]
errors=[]
for path in paths:
    if len(placements[path])!=1:errors.append({'path':path,'placements':placements[path]})
for group in hashes.values():
    if len(group)>1:errors.append({'identical_files':group})
if any(p['distance']<8 for p in pairs):errors.append('Review near-duplicate photos')
campus=selected.get('additional_campus_photos',{})
all_paths=paths|{p['path'] for p in campus.values()}
units={p:set() for p in all_paths}
for page in dist.glob('*.html'):
    if page.name.startswith('zh-'):continue
    tree=LH.parse(str(page))
    for i,im in enumerate(tree.xpath('//main//img[not(ancestor::dialog)]')):
        src=im.get('src')
        if src not in units:continue
        trigger=im.xpath('ancestor::a[@data-story-open]')
        unit=page.name+'#'+(trigger[0].get('data-story-open') if trigger else 'photo-'+str(i))
        units[src].add(unit)
    for script in tree.xpath('//script[@id="editorial-story-data"]'):
        for story in json.loads(script.text):
            for im in story['images']:
                if im['src'] in units:units[im['src']].add(page.name+'#'+story['id'])
for path,uses in units.items():
    if len(uses)!=1:errors.append({'path':path,'editorial_units':sorted(uses)})
all_hashes=[hashlib.sha256((dist/p).read_bytes()).hexdigest() for p in all_paths]
if len(all_hashes)!=len(set(all_hashes)):errors.append('Owner photograph duplicated under different filenames')
report={'scope':'Owner-selected Japan and campus photographs across all English pages, including story JSON. Language counterparts and the enlarged view of the same story intentionally share assets. Other pre-existing campus/news/source photos are outside this audit.','new_selected_photos':len(selected['photos']),'distinct_japan_photos':len(paths),'each_photo_used_once':not errors,'closest_perceptual_pair_distance':min(p['distance'] for p in pairs),'new_webp_total_bytes':sum((dist/p['path']).stat().st_size for p in selected['photos'].values()),'placements':dict(placements),'additional_campus_photos':len(campus),'owner_editorial_units':{p:sorted(v) for p,v in units.items()},'new_pages_or_web_assets':0,'errors':errors}
(root/'japan-photo-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
