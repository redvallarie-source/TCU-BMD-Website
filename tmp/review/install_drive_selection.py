from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
from lxml import html as LH
import json,hashlib
root=Path(__file__).resolve().parents[2]
content=root/'content';dist=root/'dist'
selection=json.loads((Path(__file__).parent/'drive-selection.json').read_text(encoding='utf-8'))
records={p['slot']:p for p in selection}
copy={
'baking':('assets/international-student-campus-visit.webp','Students working together in a baking class','Baking class · Participant photograph','學生在烘焙課程中一起實作','烘焙課程・參與者提供'),
'yide':('assets/life/photo-booth.webp','Participants together at a Yide Ri gathering','Yide Ri gathering · Participant photograph','懿德日活動合影','懿德日・參與者提供'),
'hospital':('assets/life/hualien-life.webp','Volunteers and hospital staff together at Taipei Tzu Chi Hospital','Volunteering · Taipei Tzu Chi Hospital','臺北慈濟醫院志工活動合影','臺北慈濟醫院・志工活動'),
'flower':('assets/life/final-project.webp','A flower arrangement from a flower-arranging activity','Hua dao · Flower-arranging practice','花道活動中的插花作品','花道練習'),
'taiwan-tea':('assets/life/presentations.webp','Tea bowls and refreshments on a table during tea practice','Cha dao · Tea practice','茶道練習時桌上的茶碗與茶點','茶道練習')}
# Reuse existing asset slots. Never replace an image belonging to a source archive.
archive_src={s for p in dist.glob('source-*.html') for s in LH.parse(str(p)).xpath('//img/@src')}
manifest_path=content/'japan-photo-selection.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
manifest['additional_campus_photos']={};translations=manifest['translations']
sheet=Image.new('RGB',(1200,620),'#f2f5ee');draw=ImageDraw.Draw(sheet)
for i,(slot,(dest,alt,caption,zh_alt,zh_caption)) in enumerate(copy.items()):
    assert (dist/dest).is_file(), 'Replacement slot must already exist'
    assert dest not in archive_src, 'Do not alter an archive photograph'
    raw=Path(__file__).parent/'drive-sources'/(slot+'.jpg')
    im=ImageOps.exif_transpose(Image.open(raw)).convert('RGB');original=im.size
    im.thumbnail((1600,1600),Image.Resampling.LANCZOS);im.save(dist/dest,'WEBP',quality=85,method=6)
    p=records[slot]
    manifest['additional_campus_photos'][slot]={'path':dest,'alt':alt,'caption':caption,'width':im.width,'height':im.height,'source_file':'https://drive.google.com/file/d/'+p['file_id']+'/view','source_folder':'https://drive.google.com/drive/folders/1lq7nN1iUxvBs_ckktFh4FnWF9ZoQyfNe','source_filename':p['source_filename'],'source_dimensions':list(original),'sha256':hashlib.sha256((dist/dest).read_bytes()).hexdigest(),'origin':'Site-owner participant photograph; activity context confirmed by the owner'}
    translations.update({alt:zh_alt,caption:zh_caption})
    thumb=ImageOps.contain(im,(380,260));x=(i%3)*400+10;y=(i//3)*310+30;sheet.paste(thumb,(x,y));draw.text((x,y-22),slot,fill='#193f32')
sheet.save(Path(__file__).parent/'japan-selection-contact-sheet.jpg')
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
edition_path=content/'compact-editorial.json';edition=json.loads(edition_path.read_text(encoding='utf-8'))
# Preserve the original project photographs through their existing canonical files.
canonical={'assets/life/presentations.webp':'assets/photos/cafe-project.webp','assets/life/final-project.webp':'assets/photos/design-workshop.webp'}
for story in edition['learning_stories']:
    for p in story['images']:p['src']=canonical.get(p['src'],p['src'])
    if story['id']=='study-culinary':
        p=manifest['additional_campus_photos']['baking'];story['images']=[{'src':p['path'],'alt':p['alt'],'caption':p['caption']}]
    if story['id']=='study-sustainability':story['images']=[p for p in story['images'] if p['src']!='assets/life/photo-booth.webp']
for story in edition['intro_stories']:
    if story['id']=='intro-learning':
        story.update(label='Student life',title='Creative practice',body='From arranging flowers to preparing tea: two moments from student life.')
        story['images']=[{'src':manifest['additional_campus_photos'][slot]['path'],'alt':manifest['additional_campus_photos'][slot]['alt'],'caption':manifest['additional_campus_photos'][slot]['caption']} for slot in ('flower','taiwan-tea')]
        story['links']=[{'href':'student-life.html','label':'Student life'}]
    if story['id']=='intro-community':story['images']=[p for p in story['images'] if p['src']!='assets/life/photo-booth.webp']
translations.update({'Creative practice':'創意實作','From arranging flowers to preparing tea: two moments from student life.':'從花道到茶道，記錄學生生活中的兩個片刻。','Additional campus photographs: participant-provided collection.':'其他校園活動照片由參與者提供。'})
edition['translations'].update(translations)
edition_path.write_text(json.dumps(edition,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Use the existing generator and collage; do not add a page or photo section.
life_path=root/'student_life.py';s=life_path.read_text(encoding='utf-8')
s=s.replace("'image':'assets/life/presentations.webp'","'image':'assets/photos/cafe-project.webp'").replace("'image':'assets/life/final-project.webp'","'image':'assets/photos/design-workshop.webp'")
s=s.replace("selected=json.loads((Path(__file__).parent/'content/japan-photo-selection.json').read_text(encoding='utf-8'))['photos']", "collection=json.loads((Path(__file__).parent/'content/japan-photo-selection.json').read_text(encoding='utf-8'))\n    selected=collection['photos']\n    campus=collection['additional_campus_photos']\n    def campus_photo(slot,cls,priority=False):\n        p=campus[slot]\n        return photo(p['path'],p['alt'],p['caption'],cls,priority).replace('<img ',f'<img width=\"{p[\"width\"]}\" height=\"{p[\"height\"]}\" ')")
s=s.replace("photo('assets/life/photo-booth.webp','Students posing at a photo booth during the Myanmar-relief fair','Student photo booth · Myanmar-relief fair, 2025','life-cover-main',True)","campus_photo('yide','life-cover-main',True)")
s=s.replace("photo('assets/life/hualien-life.webp','Local and international students kayaking at Liyu Lake','Liyu Lake, Hualien · Department archive','life-cover-side')","campus_photo('hospital','life-cover-side')")
s=s.replace('Japan internship photographs: participant-provided collection (2026).</p>','Japan internship photographs: participant-provided collection (2026).</p><p>Additional campus photographs: participant-provided collection.</p>')
life_path.write_text(s,encoding='utf-8')
source_path=dist/'assets/photos/source-manifest.json';sources=json.loads(source_path.read_text(encoding='utf-8'))
for p in manifest['additional_campus_photos'].values():
    row=next((r for r in sources if r['relative_file']==p['path']),None)
    if row is None:row={'relative_file':p['path']};sources.append(row)
    row.update(source_url=p['source_file'],source_page=p['source_folder'],caption=p['caption'],width=p['width'],height=p['height'],credit='Site-owner participant photograph',usage='Replacement photograph in one editorial placement; source archives are unchanged.')
source_path.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
slots_path=content/'student-life-photo-slots.json';slots=json.loads(slots_path.read_text(encoding='utf-8'));slots['note']='Current replacements use the existing collage. Caption and alt text must follow each photograph. Project tabs retain their canonical department photographs.'
for slot in slots['slots']:
    if slot['slot']=='Presentations tab':slot['file']='assets/photos/cafe-project.webp'
    if slot['slot']=='Final project tab':slot['file']='assets/photos/design-workshop.webp'
slots_path.write_text(json.dumps(slots,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Replaced five existing image files; no new pages, galleries, or web assets.')
