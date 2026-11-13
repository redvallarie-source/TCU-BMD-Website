"""Install owner photographs into existing editorial placements."""
from pathlib import Path
from PIL import Image, ImageOps
import hashlib, json

root=Path(__file__).resolve().parents[2]
content=root/'content'; dist=root/'dist'
records={p['slot']:p for p in json.loads((Path(__file__).parent/'drive-selection.json').read_text(encoding='utf-8'))}
manifest_path=content/'japan-photo-selection.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
campus=manifest['additional_campus_photos']; translations=manifest['translations']
copy={
 'home-jianguo':('assets/home-jianguo.webp','A campus building and garden at Jianguo Campus','Jianguo Campus · Hualien','建國校區的校舍與庭園','建國校區・花蓮'),
 'home-jieren':('assets/campus-mountain-building.webp','The entrance sign and buildings at Jieren Campus','Jieren Campus · Hualien','介仁校區入口標誌與校舍','介仁校區・花蓮'),
 'class-operations':('assets/photos/class-learning.webp','An educator speaking beside a management presentation in class','Management learning · In class','教師在課堂上以管理簡報進行教學','管理學習・課堂現場'),
 'intro-group':('assets/photos/department-group.webp','BMD participants together in a classroom group photograph','The BMD community · Participant photograph','經管系參與者在教室中的團體合影','經管系的我們・參與者提供'),
 'learning-computers':('assets/photos/library-computers.webp','Students working together at library computer workstations','Learning with digital tools · Library computers','學生在圖書館電腦區一起學習','運用數位工具學習・圖書館電腦區'),
 'home-practice':('assets/photos/class-study.webp','Two students studying and writing at classroom desks','Studying together · In class','兩位學生在教室桌前閱讀與書寫','一起學習・課堂現場'),
 'life-learning':('assets/life/learning-together.webp','Students sharing a relaxed moment during class','Learning together · In class','學生在課堂中交流的片刻','一起學習・課堂裡'),
 'hospital-building':('assets/life/hospital-visit.webp','The entrance of Taipei Tzu Chi Hospital','Taipei Tzu Chi Hospital · Participant photograph','臺北慈濟醫院入口','臺北慈濟醫院・參與者提供'),
 'baking-individual':('assets/life/baking-practice.webp','A student preparing chocolate cake in a baking class','Hands-on baking · Student practice','學生在烘焙課程中製作巧克力蛋糕','烘焙實作・學生練習'),
 'smart-computers':('assets/life/podcast-project.webp','Students studying together at library computers','Digital study · Library computers','學生一起使用圖書館電腦學習','數位學習・圖書館電腦區'),
}
new_assets=[]
for slot,(dest,alt,caption,zh_alt,zh_caption) in copy.items():
    target=dist/dest
    if not target.exists():new_assets.append(dest)
    im=ImageOps.exif_transpose(Image.open(Path(__file__).parent/'drive-sources'/(slot+'.jpg'))).convert('RGB')
    original=im.size; im.thumbnail((1600,1600),Image.Resampling.LANCZOS)
    im.save(target,'WEBP',quality=85,method=6)
    source=records[slot]
    folder=('https://drive.google.com/drive/folders/1VJWwFWnDnRPTOt7HMa0AYawJsqH3NIPj' if slot.startswith('home-') and slot!='home-practice' else
      'https://drive.google.com/drive/folders/1tO8ZMaJDN6_CD1F9VlPQOd4bY2xrsZ5C' if slot in ('class-operations','learning-computers','home-practice','smart-computers') else
      'https://drive.google.com/drive/folders/1lq7nN1iUxvBs_ckktFh4FnWF9ZoQyfNe')
    campus[slot]={'path':dest,'alt':alt,'caption':caption,'width':im.width,'height':im.height,'source_file':'https://drive.google.com/file/d/'+source['file_id']+'/view','source_folder':folder,'source_filename':source['source_filename'],'source_dimensions':list(original),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'origin':'Owner-provided authentic photograph; description follows visible content'}
    if source.get('download_url'):campus[slot]['download_note']='Drive display JPEG, 1200 × 900; original HEIC retained in Drive.'
    translations.update({alt:zh_alt,caption:zh_caption})
translations.update({'Owner photograph':'使用者提供的照片','Show photo: Jianguo Campus · Hualien':'顯示照片：建國校區・花蓮','Show photo: Jieren Campus · Hualien':'顯示照片：介仁校區・花蓮','Jianguo Campus · Hualien selected.':'已選擇建國校區・花蓮。','Jieren Campus · Hualien selected.':'已選擇介仁校區・花蓮。'})
manifest['latest_campus_update']={'date':'2026-11-13','new_selected_photos':list(copy),'existing_sections_only':True,'added_optimized_asset_files':new_assets,'deferred_until_owner_supplies_photos':['UK summer study','Mao Mao Xiaoyin food stall','Whisper Tour','Student presentations','Sustainable Innovation / Grace','ZY campus identity']}
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

edition_path=content/'compact-editorial.json';edition=json.loads(edition_path.read_text(encoding='utf-8'))
def image(slot):
    p=campus[slot];return {'src':p['path'],'alt':p['alt'],'caption':p['caption']}
for story in edition['learning_stories']:
    if story['id']=='study-operations':story['images']=[image('home-practice')]
    if story['id']=='study-smart':story['images']=[image('smart-computers')]
edition['translations'].update(translations)
edition_path.write_text(json.dumps(edition,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

sources_path=dist/'assets/photos/source-manifest.json';sources=json.loads(sources_path.read_text(encoding='utf-8'))
for slot in copy:
    p=campus[slot];row=next((r for r in sources if r['relative_file']==p['path']),None)
    if row is None:row={'relative_file':p['path']};sources.append(row)
    row.update(source_url=p['source_file'],source_page=p['source_folder'],caption=p['caption'],width=p['width'],height=p['height'],credit='Owner-provided photograph',usage='One editorial placement; bilingual pages and the same photograph viewer share this asset.')
sources_path.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

life_path=root/'student_life.py';s=life_path.read_text(encoding='utf-8')
s=s.replace("'image':'assets/life/podcast-project.webp'","'image':'assets/photos/digital-learning.webp'")
s=s.replace("campus_photo('hospital','life-cover-side')","campus_photo('hospital-building','life-cover-side')")
life_path.write_text(s,encoding='utf-8')

js_path=dist/'assets/interior.js';s=js_path.read_text(encoding='utf-8')
tabs=[campus['class-operations'],{'path':'assets/photos/digital-learning.webp','alt':'Students use digital tools in their learning','caption':'Digital-learning classroom · Department photo archive','width':1200,'height':800},{'path':'assets/photos/design-thinking.webp','alt':'Collaborative creative learning in the department','caption':'Workshop with a visiting educator · Department archive','width':960,'height':719},campus['baking-individual']]
start=s.index('    const images=');end=s.index('\n',start)
s=s[:start]+'    const images='+json.dumps([[p['path'],p['alt'],p['caption'],p['width'],p['height']] for p in tabs],ensure_ascii=False)+';'+s[end:]
s=s.replace("photo.alt=images[i][1];document", "photo.alt=images[i][1];photo.width=images[i][3];photo.height=images[i][4];document.getElementById('program-photo-caption').textContent=images[i][2];document")
js_path.write_text(s,encoding='utf-8')
slots_path=content/'student-life-photo-slots.json';slots=json.loads(slots_path.read_text(encoding='utf-8'))
for p in slots['slots']:
    if p['slot']=='Hero inset':p['file']=campus['hospital-building']['path'];p['suggested_replacement']='A different participant photograph from the hospital visit; the volunteer group photograph is used only on Home.'
    if p['slot']=='Podcast tab':p['file']='assets/photos/digital-learning.webp'
slots['note']='Existing page sections retained. Caption, alt text, and dynamic viewers must follow the photograph. New owner photos have one editorial placement each.'
slots['latest_replacements']={k:{'file':campus[k]['path'],'caption':campus[k]['caption']} for k in copy}
slots_path.write_text(json.dumps(slots,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Installed',len(copy),'authentic photographs; retained all existing pages and sections.')
