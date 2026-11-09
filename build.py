from pathlib import Path
import json,re,hashlib,html,shutil,urllib.parse
from content_support import normalize_document
from lxml import html as LH
from navigation_consolidation import RETIRED,reconcile_links
ROOT=Path(__file__).parent; D=ROOT/'dist'; R=ROOT/'content'
E=json.loads((R/'official-en/pages.json').read_text());Z=json.loads((R/'official-zh/manifest.json').read_text())['pages']; F=json.loads((R/'official-en/faculty-roster.json').read_text());LATEST=json.loads((R/'official-zh/latest-news.json').read_text())
if isinstance(LATEST,dict):LATEST=LATEST.get('items',LATEST.get('news',LATEST.get('pages',[])))
from faculty_update import update_roster
F=update_roster(F,R)
POR=json.loads((R/'official-en/portrait-map.json').read_text());IM={}
if (R/'source-image-map.json').exists():IM=json.loads((R/'source-image-map.json').read_text())
if isinstance(IM,dict) and 'mapping' in IM:IM=IM['mapping']
if isinstance(POR,list):POR={x.get('url',x.get('source_url','')):x.get('path',x.get('local_path','')) for x in POR}
if isinstance(POR,dict) and 'mapping' in POR:POR=POR['mapping']
h=lambda s:html.escape(str(s or ''),quote=True)
def sha(s,n=12):return hashlib.sha1(s.encode()).hexdigest()[:n]
def source_path(u):return 'source-'+sha(u)+'.html'
def profile_path(u):return 'faculty-'+sha(u,10)+'.html'
for item in LATEST:
 Z.append({'url':item['url'],'title':item['title_en'],'status':'success','depth':1,'category':'latest_announcements','blocks':item.get('paragraphs',[]) or [item['summary_en']],'tables':[],'documents':[],'links':[],'images':[{'url':item['local_image'],'alt':item['title_en']}]})
SOURCES={}
for p in E+Z:
 if p.get('status') not in ('failed','error','excluded'):SOURCES[p['url']]=p
for p in E:
 if p.get('status')=='excluded':
  for prefix in ['news-','source-']:(D/(prefix+sha(p['url'])+'.html')).unlink(missing_ok=True)
source_map={u:source_path(u) for u in SOURCES}
def icon(name='arrow'):
 paths={'arrow':'<path d="M4 12h16m-6-6 6 6-6 6"/>','search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>','menu':'<path d="M4 6h16M4 12h16M4 18h16"/>','close':'<path d="m6 6 12 12M6 18 18 6"/>','external':'<path d="M8 4h12v12M20 4 4 20"/>','leaf':'<path d="M4 20C0 8 10 3 21 3c0 13-7 20-17 17Zm0 0L18 6m-9 9V8m5 4h5"/>'}
 return '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">'+paths.get(name,paths['arrow'])+'</svg>'
def a(url,label,cls='',external=False):return f'<a href="{h(url)}"'+(f' class="{cls}"' if cls else '')+(' target="_blank" rel="noopener"' if external else '')+'>'+label+'</a>'
def button(url,label,style=''):return a(url,h(label)+icon(),'button '+style)
NAV=[('About',[('introduction.html','Department introduction'),('vision.html','Vision & mission'),('history.html','Department history')]),('Academics',[('academics.html','Learning directions'),('curriculum.html','Curriculum by entry year'),('requirements.html','Certificate requirements'),('resources.html','Forms & learning resources')]),('Faculty',[('faculty.html','Meet our people')]),('Student Life',[('student-life.html','Life at BMD'),('internships.html','Beyond Campus'),('careers.html','Career pathways')]),('News',[('news.html','News & achievements') ,('events.html','Academic calendar')])]
SEARCH=[]
def head(title):return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{h(title)} · TCU Business Management</title><meta name="description" content="{h(title)} — Tzu Chi University Department of Business Management. Department information, people, student work, and academic resources."><link rel="icon" href="assets/mdm_logo_transparent.png"><link rel="stylesheet" href="assets/style.css"><script defer src="assets/i18n.js"></script><script defer src="assets/calendar-date.js"></script><script defer src="assets/site.js"></script></head><body><a class="skip" href="#main">Skip to content</a>'
def cache_assets(markup):
 def fingerprint(match):
  file=D/match.group(2)
  assert file.exists(),f'Missing shared asset: {file}'
  version=hashlib.sha256(file.read_bytes()).hexdigest()[:12]
  return match.group(1)+match.group(2)+'?v='+version+match.group(3)
 return re.sub(r'((?:href|src)=")(assets/[^"?]+\.(?:css|js))(")',fingerprint,markup)
def header(path="index.html"):
 nav=''.join('<details class="nav-group"><summary>'+label+'</summary><div class="dropdown">'+''.join(a(u,h(t)) for u,t in links)+'</div></details>' for label,links in NAV)
 markup='<header class="site-header"><div class="wrap header-inner"><a class="brand" href="index.html"><img src="assets/mdm_logo_transparent.png" alt=""><div><b>Business Management</b><small>TZU CHI UNIVERSITY · 慈濟大學經營管理學系</small></div></a><nav class="primary-nav" id="primary-nav" aria-label="Main navigation"><a href="index.html">Home</a>'+nav+'<a class="apply nav-apply" href="admissions.html">Study with us ↗</a></nav><div class="header-actions"><a class="language-switch" href="zh-'+h(path)+'" lang="zh-Hant" hreflang="zh-Hant" aria-label="繁體中文 — Read this page in Traditional Chinese"><span class="language-full">繁體中文</span><span class="language-short" aria-hidden="true">繁中</span></a><button class="icon-btn" data-search-open aria-label="Search the website">'+icon('search')+'</button><button class="icon-btn menu-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Toggle navigation">'+icon('menu')+'</button></div></div></header>'
 from personality import navigation
 return navigation(markup,path)
def footer():
 return '<footer class="footer"><div class="wrap"><div class="footer-grid"><div><a class="brand" href="index.html"><img src="assets/mdm_logo_transparent.png" alt=""><div><b>Business Management</b><small>TZU CHI UNIVERSITY</small></div></a></div><div><h3>DEPARTMENT</h3><ul>'+''.join('<li>'+a(u,t)+'</li>' for u,t in [('introduction.html','Our department'),('faculty.html','Our people'),('news.html','News & achievements'),('student-life.html','Student life')])+'</ul></div><div><h3>STUDENT INFORMATION</h3><ul>'+''.join('<li>'+a(u,t)+'</li>' for u,t in [('admissions.html','Admissions'),('curriculum.html','Curriculum'),('internships.html','Internship resources'),('resources.html','Documents & forms')])+'</ul></div><div><h3>CONTACT</h3><p>67 Jieren St., Hualien 97074, Taiwan<br><a href="tel:+88638572677">+886-3-857-2677 ext. 31682</a><br><a href="mailto:ss62@gms.tcu.edu.tw">ss62@gms.tcu.edu.tw</a></p><a class="text-link" href="contact.html" style="margin-top:13px">Contact the department '+icon()+'</a></div></div><div class="footer-bottom"><span>Student redesign project · Department information remains subject to the official publications.</span><span><a href="https://mdm.tcu.edu.tw/?Lang=en" target="_blank" rel="noopener">Official department ↗</a> &nbsp; · &nbsp; <a href="content-review.html">Sources & content coverage</a></span></div></div></footer><button class="back-top" aria-label="Back to top">↑</button><dialog id="search-dialog" aria-labelledby="search-heading"><div class="search-top"><h2 id="search-heading">What are you looking for?</h2><button class="icon-btn" data-search-close aria-label="Close search">'+icon('close')+'</button></div><label for="site-search" class="kicker">Search pages, people, and resources</label><input id="site-search" type="search" placeholder="Try curriculum, finance, or a faculty name…"><div id="search-results" aria-live="polite"></div></dialog></body></html>'
def save(path,title,body,category='Explore',text=''):
 if path in RETIRED:
  target=RETIRED[path]
  destination={'exchange.html':'Beyond Campus','outcomes.html':'Life at BMD','international.html':'Admissions'}[path]
  redirect_head=head('Continue to '+destination).replace('</head>','<meta name="robots" content="noindex,follow"><meta name="bmd-redirect" content="'+h(target)+'"><meta http-equiv="refresh" content="0;url='+h(target)+'"><link rel="canonical" href="'+h(target.split('#')[0])+'"><script defer src="assets/redirect.js"></script></head>')
  redirect_body=hero('This page has moved.','Use the updated page to continue.','Department information')+'<section class="wrap section">'+a(target,'Continue to '+destination,'text-link')+'</section>'
  (D/path).write_text(reconcile_links(cache_assets(redirect_head+header(path)+'<main id="main">'+redirect_body+'</main>'+footer())))
  return
 if path=='internships.html':title='Beyond Campus'
 from interior import redesign,page_class
 from editorial import polish
 from content_support import support
 from personality import refine
 from motion_design import apply_motion,MOTION_PAGES
 from campus_refinement import refine_campus
 from quiet_ui import quiet_document
 interior=path!='index.html'
 if interior:body=redesign(path,body)
 body=polish(path,body)
 body=support(path,body,R,tuple(n['path'] for n in NEWS if n['category']=='archive'))
 body=refine(path,body,R)
 body=apply_motion(path,body,R)
 body=refine_campus(path,body)
 from faculty_update import refine_people
 body=refine_people(path,body,R)
 if path=='student-life.html':
  from student_life import render_life
  body=render_life(body)
 if path=='internships.html':
  from internship_editorial import render_internships
  body=render_internships(body,R)
 from compact_editorial import compact
 body=compact(path,body,R)
 from information_design import refine_information
 body=refine_information(path,body,R)
 doc_head=head(title)
 if path=='index.html':doc_head=doc_head.replace('</head>','<link rel="stylesheet" href="assets/homepage.css"><script defer src="assets/homepage.js"></script></head>')
 doc_head=doc_head.replace('</head>','<link rel="preload" href="assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="assets/refinement.css">'+('<script defer src="assets/refinement.js"></script>' if path=='index.html' else '')+'</head>')
 if interior:doc_head=doc_head.replace('</head>','<link rel="stylesheet" href="assets/interior.css"><script defer src="assets/interior.js"></script></head>')
 doc_head=doc_head.replace('</head>','<link rel="stylesheet" href="assets/finishing.css"><link rel="stylesheet" href="assets/editorial.css"></head>')
 if path in MOTION_PAGES:doc_head=doc_head.replace('</head>','<link rel="stylesheet" href="assets/campus-motion.css"><script defer src="assets/campus-motion.js"></script></head>')
 doc_head=doc_head.replace('</head>','<link rel="stylesheet" href="assets/quiet-ui.css"><link rel="stylesheet" href="assets/campus-refinement.css"><script defer src="assets/campus-refinement.js"></script></head>')
 if path=='student-life.html':doc_head=doc_head.replace('</head>','<link rel="stylesheet" href="assets/student-life.css"><script defer src="assets/student-life.js"></script></head>')
 if path=='internships.html':doc_head=doc_head.replace('</head>','<link rel="stylesheet" href="assets/internships.css"><script defer src="assets/internships.js"></script></head>')
 doc_head=doc_head.replace('</head>','<link rel="stylesheet" href="assets/edition.css">'+('<script defer src="assets/edition.js"></script>' if 'id="editorial-story-data"' in body else '')+'</head>')
 doc_head=doc_head.replace('</head>','<link rel="stylesheet" href="assets/information-design.css"></head>')
 if path=='requirements.html':doc_head=doc_head.replace('</head>','<script defer src="assets/information-design.js"></script></head>')
 doc_head=cache_assets(doc_head)
 (D/path).write_text(reconcile_links(quiet_document(doc_head+header(path)+'<main id="main"'+(' class="'+page_class(path)+'"' if interior else '')+'>'+body+'</main>'+footer(),path)),encoding='utf-8')
 if not path.startswith(('source-','news-','faculty-')):
  index_root=LH.fragment_fromstring(body,create_parent='div')
  story_text=' '.join(' '.join(str(v.get(k,'')) for k in ('label','title','body')) for script in index_root.xpath('.//script[@id="editorial-story-data"]') for v in json.loads(script.text))
  for ignored in index_root.xpath('.//script|.//dialog'):ignored.getparent().remove(ignored)
  text=' '.join(index_root.text_content().split())
 SEARCH.append({'url':path,'title':title,'category':category,'text':text[:6000 if path=='internships.html' else 1500]+(' '+story_text if not path.startswith(('source-','news-','faculty-')) else '')})
def crumbs(section,title):return '<div class="wrap crumbs">'+a('index.html','Home')+'<span>'+h(section)+'</span><span>'+h(title)+'</span></div>'
def hero(title,desc,kicker='',image=None,section='Discover'):
 body='<div><div class="kicker">'+h(kicker or section)+'</div><h1>'+title+'</h1><p>'+desc+'</p></div>'
 if image:body+='<img src="'+image+'" alt="Tzu Chi University department learning and campus life">'
 return '<section class="wrap page-hero'+(' with-photo' if image else '')+'">'+body+'</section>'
def note(url,label='Official source'):
 return '<div class="source-note">'+a(url,h(label)+' ↗',external=True)+'</div>'
def source_link(url,label=None):return a(source_map.get(url,url),h(label or SOURCES.get(url,{}).get('title','Read source resource'))+icon('external'),'text-link',url not in source_map)
def doclist(docs):
 out='<div class="resource-list">';seen=set()
 for d in docs:
  d=normalize_document(d)
  u=d.get('url','');label=d.get('label',d.get('text','')).strip() or Path(urllib.parse.urlparse(u).path).name
  if not u.startswith(('http','assets/')) or u in seen:continue
  seen.add(u);typ=urllib.parse.urlparse(u).path.rsplit('.',1)[-1].upper();typ=typ if len(typ)<7 else 'LINK'
  out+=f'<a class="resource-link" href="{h(u)}" target="_blank" rel="noopener" data-filter-item><div><b>{h(label)}</b><small>{h(d.get("context","")[:180])}</small></div><span class="type">{typ} ↗</span></a>'
 return out+'</div>'
def source_image(u):
 v=IM.get(u) or POR.get(u)
 if isinstance(v,dict):v=v.get('local_path',v.get('path',v.get('local_asset','')))
 if v and str(v).startswith('/workspace/'):v=str(Path(v).relative_to(D)) if str(v).startswith(str(D)) else ''
 return v or u

def ep(key):return next(p for p in E if p['key']==key)
def zp(cat):return next(p for p in Z if p['category']==cat and p['depth']==0)
def tables(tabs):return ''.join('<div class="table-wrap"><table>'+''.join('<tr>'+''.join(('<th>' if ri==0 else '<td>')+h(c)+('</th>' if ri==0 else '</td>') for c in row)+'</tr>' for ri,row in enumerate(t))+'</table></div>' for t in tabs)
def seed_extra(p):
 links=[x for x in p.get('links',[]) if x.get('url') in SOURCES and x['url']!=p['url']]
 seen=set();out=''
 for l in links:
  if l['url'] in seen:continue
  seen.add(l['url']);out+='<div class="resource-link"><div><b>'+source_link(l['url'],l.get('text') or SOURCES[l['url']]['title'])+'</b></div></div>'
 return out
# News: current original-language announcements, then verified English achievements.
NEWS=[]
for p in LATEST:
 u=p.get('url',p.get('source_url',''));title=p.get('title_en') or p.get('title','Announcement');im=p.get('local_image','')
 if str(im).startswith(str(D)):im=str(Path(im).relative_to(D))
 NEWS.append({'url':u,'title':title,'summary':p.get('summary_en','Read the original department announcement and event poster.'),'image':im,'category':'announcements','label':'Department announcement','original':p})
for p in E:
 if p.get('status')=='excluded':continue
 if re.search(r'/p/406-[^?]*,r1.php',p['url']):
  title=p['title'];text=re.sub(r'^'+re.escape(title),'',p['text']).strip();words=text.split();summary=' '.join(words[:65]);ims=p.get('images',[])
  NEWS.append({'url':p['url'],'title':title,'summary':summary,'image':source_image(ims[0]['url']) if ims else '', 'category':'achievements' if 'Achievement' in title else 'archive','label':'Student achievement' if 'Achievement' in title else 'Department archive','original':p})
for n in NEWS:
 if 'acc.tccn.edu.tw' in str(n.get('image','')):n['image']=''
 n['path']='news-'+sha(n['url'])+'.html'
def news_card(n,feature=False):
 return '<article class="news-card'+(' feature' if feature else '')+'" data-filter-item data-category="'+n['category']+'">'+(a(n['path'],'<img src="'+h(n['image'])+'" alt="'+h(n['title'])+'" loading="lazy">') if n['image'] else '')+'<div class="news-meta">'+h(n['label'])+'</div><h3>'+a(n['path'],h(n['title']))+'</h3><p>'+h(n['summary'][:240])+('…' if len(n['summary'])>240 else '')+'</p>'+a(n['path'],'Read the story '+icon(),'text-link')+'</article>'
# Home
home='<section class="hero"><div class="wrap"><div class="hero-grid"><div class="hero-copy"><div class="kicker">Business Management · Tzu Chi University</div><h1>A business mind.<em>A human heart.</em></h1><p>Build the knowledge to understand business, the curiosity to explore new ideas, and the character to make a positive difference.</p><div class="hero-actions">'+button('academics.html','Find your direction')+a('introduction.html','Meet our department '+icon('external'),'text-link')+'</div></div><div class="hero-image"><img src="assets/campus-mountain-building.webp" alt="Tzu Chi University campus buildings framed by the mountains of Hualien" fetchpriority="high"><span class="hero-index">HUALIEN, TAIWAN · TZU CHI UNIVERSITY</span><div class="photo-label"><b>Big ideas start with a wider view.</b><small>A place to learn, connect, and grow.</small></div></div></div><div class="hero-foot"><b>PROFESSIONAL KNOWLEDGE. HUMANISTIC VALUES.</b><div class="talents"><span>Creativity</span><span>Teamwork</span><span>Global perspective</span><span>Workplace ethics</span></div></div></div></section>'
home+='<section class="intro-band"><div class="wrap"><h2>Business education,<br>with people at its centre.</h2><div><p>Our department brings professional management knowledge together with humanistic qualities, creative thinking, teamwork, cross-cultural perspectives, and workplace ethics.</p>'+a('vision.html','Explore our purpose '+icon(),'text-link')+'</div></div></section>'
learning_names=['Operations Management','Smart Business','Sustainable Innovation','Culinary Management']
learning='<div class="learning-layout"><div class="learning-tabs" role="tablist" aria-label="Learning directions">'+''.join(f'<button class="learning-tab" id="learning-tab-{i}" data-learning-tab role="tab" aria-selected="{str(i==0).lower()}" aria-controls="learning-panel" tabindex="{0 if i==0 else -1}"><small>0{i+1}</small>{n}{icon()}</button>' for i,n in enumerate(learning_names))+'</div><div class="learning-panel" id="learning-panel" role="tabpanel" aria-labelledby="learning-tab-0" tabindex="0"><div class="kicker">Your possibilities</div><h3 id="learning-title">Operations Management</h3><p id="learning-description">Understand operations and industries, and connect management knowledge with real business practice.</p>'+a('curriculum.html','Explore the curriculum '+icon(),'text-link')+'</div></div>'
home+='<section class="wrap section"><div class="section-head"><div><div class="kicker">Find your direction</div><h2>One department.<br><em>Different possibilities.</em></h2></div><p>Explore four distinctive learning directions. Discover the curriculum and original course resources for your entry year.</p></div>'+learning+'</section>'
home+='<section class="wrap section" style="padding-top:15px"><div class="photo-story"><img src="assets/photos/cafe-project.webp" alt="Students from the department’s Indonesian cohort presenting a project" loading="lazy"><div><div class="kicker">Learning that comes to life</div><h2>Take an idea.<br><em>Make it matter.</em></h2><p>From running a student café to developing creative projects, learning goes beyond the classroom. Connect theory with practice, collaborate with others, and discover what you can create.</p><ul><li>Student café</li><li>Project learning</li><li>Cross-cultural exchange</li></ul>'+a('student-life.html','Experience life at BMD '+icon(),'text-link')+'</div></div></section>'
home+='<section class="wrap section"><div class="section-head"><div><div class="kicker">On our radar</div><h2>New ideas.<br><em>Shared achievements.</em></h2></div>'+a('news.html','All news & stories '+icon(),'text-link')+'</div><div class="news-grid">'+''.join(news_card(n,i==0) for i,n in enumerate(NEWS[:3]))+'</div></section>'
home+='<section class="wrap cta"><div><div class="kicker">Your next chapter</div><h2>See where your curiosity takes you.</h2><p>Explore admissions, meet the department, and take your next step.</p></div>'+button('admissions.html','Study with us')+'</section>'
from homepage import render_home
home=render_home(R,NEWS,icon,button,a,h)
save('index.html','Business with purpose.',home,'Home','Business Management Tzu Chi University academic opportunities student life admissions')
# Introduction
body=crumbs('About','Introduction')+hero('More than a business education.','Professional learning and humanistic values come together to prepare thoughtful, capable business professionals.','Meet the department','assets/photos/student-community.webp')
body+='<div class="wrap page-tabs">'+a('introduction.html','Introduction','active')+a('vision.html','Vision & Mission')+a('history.html','History')+'</div><section class="wrap section split"><div class="lead"><div class="kicker">Our educational approach</div><h2>Knowledge.<br>Character.<br><em>Connection.</em></h2></div><div class="prose"><p>The department aims to cultivate professionals with humanistic qualities, creative thinking, teamwork, cross-cultural perspectives, and workplace ethics.</p><p>Its core capabilities connect operations and industry analysis, business intelligence and applications, business and financial knowledge, and social innovation with sustainable management.</p>'+source_link(ep('5576f6f319f3')['url'],'See all original department materials')+'</div></section><section class="wrap section" style="padding-top:0"><div class="feature-grid">'+''.join('<article class="feature"><div class="num">0'+str(i+1)+'</div><h3>'+t+'</h3><p>'+p+'</p></article>' for i,(t,p) in enumerate([('Learn with purpose','Connect academic knowledge with professional practice and thoughtful decision-making.'),('Grow with others','Develop teamwork, creativity, and an understanding of different cultures.'),('Lead with responsibility','Bring humanistic values and workplace ethics into your future professional life.')]))+'</div></section>'
save('introduction.html','Department introduction',body,'About')
# Vision
art='<svg class="vision-art" viewBox="0 0 320 300" aria-hidden="true"><circle cx="160" cy="150" r="115" fill="none" stroke="#c9dcba" stroke-dasharray="2 7"/><ellipse cx="160" cy="150" rx="65" ry="103" fill="none" stroke="#b8d29a" stroke-width="22" transform="rotate(40 160 150)"/><ellipse cx="160" cy="150" rx="65" ry="103" fill="none" stroke="#67965a" stroke-width="22" transform="rotate(-40 160 150)"/><circle cx="160" cy="150" r="43" fill="#f9fcf6"/><path d="M160 177v-49m0 27c-17 1-25-9-25-21 16 0 25 8 25 21Zm0-11c17 1 24-9 24-21-16 0-24 9-24 21Z" fill="#91b777" stroke="#467443" stroke-width="1.5"/></svg>'
body=crumbs('About','Vision & Mission')+hero('Vision <em>&</em> Mission','Where we’re going. How we’ll get there.','Our purpose')+'<section class="wrap section" style="padding-top:0"><div class="vision-layout"><section><div class="kicker">01 · Our vision</div><h2>A better future.<br>A broader perspective.</h2><p>Advance innovative, globally connected, and socially responsible business education.</p></section>'+art+'<section><div class="kicker">02 · Our mission</div><h2>Professional minds.<br>Compassionate hearts.</h2><p>Develop skilled business professionals with creativity, teamwork, cross-cultural understanding, and strong ethical values.</p></section></div>'+note('https://mdm.tcu.edu.tw/p/412-1021-2.php?Lang=en','Concise adaptations of the department’s educational goals and future vision')+'</section>'
save('vision.html','Vision & Mission',body,'About')
# History
body=crumbs('About','Department History')+hero('Different chapters.<br><em>One evolving story.</em>','Explore the milestones that shaped the department.','Department history')+'<section class="wrap section" style="padding-top:0"><div class="archive-layout"><div class="year-nav" role="tablist" aria-label="History milestones">'+''.join(f'<button class="year-button" id="year-{i}" role="tab" data-year="{y}" aria-selected="{str(i==0).lower()}" aria-controls="history-panel" tabindex="{0 if i==0 else -1}"><b>{y}</b><small>{n}</small></button>' for i,(y,n) in enumerate([('2000','Foundations'),('2004','Digital shift'),('2013','New direction'),('2023','Broader horizons'),('2024','A new chapter')]))+'</div><div class="history-sheet" id="history-panel" role="tabpanel" aria-labelledby="year-0" tabindex="0"><div><div id="history-year" class="history-year">2000</div><h2 id="history-title">The accounting roots</h2><p id="history-description">A four-year Accounting program was introduced, laying the foundation for the department’s academic journey.</p></div><svg viewBox="0 0 260 230" fill="none" aria-hidden="true"><ellipse cx="130" cy="204" rx="79" ry="9" fill="#dcebd1"/><g transform="rotate(-8 130 115)"><rect x="68" y="32" width="119" height="166" rx="12" fill="#fcfefb" stroke="#719065" stroke-width="1.5"/><rect x="68" y="32" width="17" height="166" rx="7" fill="#527651"/><path d="M103 70h62M103 85h43M103 112h62m-62 17h62m-62 17h62m-41-42v58" stroke="#b8c7a4" stroke-width="2"/><path d="m107 42 2-17m17 17 2-17m17 17 2-17m17 17 2-17" stroke="#a3c68e" stroke-width="3" stroke-linecap="round"/></g></svg></div></div>'+note('https://edurp.tcu.edu.tw/CLM/CLM_detail_coll.aspx?a=115&b=TCU&c=USMDM&d=CM&e=N&f=2','University academic record for the department’s earlier milestones')+'</section>'
save('history.html','Department History',body,'About')
# Academics and curriculum
body=crumbs('Academics','Learning directions')+hero('Build your knowledge.<br><em>Find your direction.</em>','Explore the department’s distinctive learning directions and the original curriculum for your admission year.','Academic possibilities','assets/photos/digital-learning.webp')+'<section class="wrap section" style="padding-top:10px">'+learning+note('https://mdm.tcu.edu.tw/p/412-1021-2.php?Lang=en','Four distinctive talent areas in the official department introduction')+'</section><section class="wrap section" style="padding-top:10px"><div class="feature-grid">'+''.join('<article class="feature"><div class="num">ACADEMIC RESOURCES</div><h3>'+t+'</h3><p>'+p+'</p><br>'+a(u,'Explore '+icon(),'text-link')+'</article>' for t,p,u in [('Curriculum by entry year','Find the course list and curriculum map that apply to your cohort.','curriculum.html'),('Professional certificates','Read the department’s certificate point system and graduation requirement.','requirements.html'),('Forms & regulations','Access original policies, internship forms, and learning resources.','resources.html')])+'</div></section>'
save('academics.html','Academic learning directions',body,'Academics')
cohorts=[p for p in E if 'Admission Courses' in p['title']]
body=crumbs('Academics','Curriculum')+hero('A clear path.<br><em>Your own possibilities.</em>','Choose your admission year to find the original bilingual course list and curriculum map. Requirements can differ by cohort.','Curriculum by entry year')+'<section class="wrap section" style="padding-top:0" data-filter-scope><div class="tool-row"><div class="filters">'+''.join(f'<button class="filter {"active" if v=="all" else ""}" data-filter="{v}" aria-pressed="{str(v=="all").lower()}">{label}</button>' for v,label in [('all','All entry years')]+[(str(y),f'{y} / {y+1911}') for y in range(115,110,-1)])+'</div></div><div class="note-box">Use the documents for your own admission year. The university’s graduation review remains the authority for your final credit requirements.</div>'
for p in sorted(cohorts,key=lambda p:p['title'],reverse=True):
 year=re.search(r'\d{3}',p['title']).group();docs=[l for l in p['links'] if re.search(r'\.(pdf|docx?|xlsx?)(?:$|\?)',l['url'],re.I)]
 body+=f'<section data-filter-item data-category="{year}" style="margin:35px 0"><div class="section-head"><div><div class="kicker">Entry year {year} · {int(year)+1911}</div><h2>{year} curriculum</h2></div>{source_link(p["url"],"View original course page")}</div>'+doclist(docs)+'</section>'
body+='<p class="empty" hidden>No resources found for this selection.</p></section>'
save('curriculum.html','Curriculum by entry year',body,'Academics','111 112 113 114 115 admission courses curriculum maps bilingual course credits')
# Certificates, regulatory and internship documents
p=ep('c32918c65d8f');body=crumbs('Academics','Certificate requirements')+hero('Turn learning<br>into <em>professional capability.</em>','Explore the department’s professional certificate requirement and point system.','Certificate requirements')+'<section class="wrap section split" style="padding-top:0"><div class="lead"><div class="kicker">Professional preparation</div><h2>A practical<br><em>next step.</em></h2><p>The published department regulation requires at least 30 certificate points before graduation. Read the original rules and point tables for accepted certifications.</p>'+note(p['url'])+'</div><div>'+tables(p['tables'])+'</div></section>'
save('requirements.html','Certificate requirements',body,'Academics',p['text'])
for cat,path,title,desc in [('regulations','regulations.html','Rules that support your learning.','Find original department regulations and committee rules. Official document titles are retained in their publication language.'),('internships','internships.html','Take learning into the real world.','Prepare for internships with original department policies, agreements, forms, and questionnaires.')]:
 p=zp(cat);docs=p['documents'];body=crumbs('Academics' if cat=='regulations' else 'Student Life',title.split('.')[0])+hero(title,desc,'Regulations & policies' if cat=='regulations' else 'Internship resources','assets/photos/international-learning.webp' if cat=='internships' else None)+'<section class="wrap section split" style="padding-top:10px"><div class="lead"><div class="kicker">Keep the essentials close</div><h2>'+('Learn confidently.' if cat=='regulations' else 'Prepare.<br>Participate.<br><em>Reflect.</em>')+'</h2><p>Use the department’s original documents for the latest forms and requirements.</p>'+source_link(p['url'],'View all source material')+'</div><div data-filter-scope><input class="filter-input" data-filter-input type="search" aria-label="Search documents" placeholder="Search document titles…">'+doclist(docs)+'<p class="empty" hidden>No documents match your search.</p></div></section>'
 save(path,'Regulations & policies' if cat=='regulations' else 'Internships',body,'Resources' if cat=='regulations' else 'Student Life',' '.join(x['label'] for x in docs))
# Faculty directory and individual profiles
body=crumbs('People','Faculty')+hero('Meet the people<br><em>behind your possibilities.</em>','Explore faculty expertise, professional backgrounds, and department contacts.','Our people')+'<section class="wrap section" style="padding-top:0" data-filter-scope><div class="tool-row"><input type="search" class="filter-input" data-filter-input aria-label="Search faculty and expertise" placeholder="Search name or expertise…"><div class="filters">'+''.join(f'<button class="filter {"active" if c=="all" else ""}" data-filter="{c}" aria-pressed="{str(c=="all").lower()}">{l}</button>' for c,l in [('all','All people'),('faculty','Core faculty'),('adjunct','Adjunct & contract'),('staff','Administration')])+'</div></div><div class="faculty-grid">'
for f in F:
 cat='staff' if 'Administrative' in f['category'] else ('adjunct' if 'Part-time' in f['category'] else 'faculty');name=f['name'];short=re.sub(r'^Dr\.\s*','',name).split(',')[0];role=name.split(',',1)[1].strip() if ',' in name else f['category'];fields=f['fields'];expertise=next((x['value'] for x in fields if 'Research' in x['label']),'');portrait=source_image(f['image']) if f.get('image') else '';path=profile_path(f['url']);pic='<img src="'+h(portrait)+'" alt="'+h(short)+'" loading="lazy">' if portrait else '<div class="initials">'+h(''.join(w[0] for w in short.split()[:2]))+'</div>'
 body+=f'<article class="person" data-filter-item data-category="{cat}"><a href="{path}" class="person-image" style="display:block">{pic}</a><h3>{a(path,h(short))}</h3><p>{h(role)}</p><p class="specialty">{h(expertise)}</p>'+a(path,'View profile '+icon(),'person-link')+'</article>'
 # Prefer per-profile fields, retain listing fields separately when the source differs.
 details=f.get('detail_tables') or [[[x['label'],x['value']] for x in fields]];flat=[]
 for tab in details:
  for row in tab:
   if len(row)>=2 and row[1].strip():flat.append((row[0],row[1]))
 profile=crumbs('Faculty',short)+hero(h(short),h(role),'Meet our faculty')+'<section class="wrap section profile" style="padding-top:0"><div>'+('<img class="portrait" src="'+h(portrait)+'" alt="'+h(short)+'">' if portrait else '<div class="person-image">'+pic+'</div>')+'</div><div><dl>'
 for label,val in flat:
  if 'Pure Expert' in label:continue
  if label.rstrip(':： ')=='Academic Position' and ('Ph.D.' in val or 'Master' in val):label='Academic qualifications'
  content=a('mailto:'+val,h(val)) if '@' in val and ' ' not in val else (a(val,h(val),external=True) if val.startswith('http') else h(val))
  profile+='<dt>'+h(label)+'</dt><dd>'+content+'</dd>'
 profile+='</dl>'
 useful=[l for l in f.get('detail_links',[]) if l['url'].startswith(('https:','http:')) and re.search(r'\.(pdf|docx?)($|\?)',l['url'],re.I)]
 if useful:profile+='<h3 style="margin:27px 0 10px">Profile resources</h3>'+doclist(useful)
 profile+=note(f['url'],'Official faculty profile — contact details and credentials as published')+'</div></section>'
 save(path,short,profile,'Faculty',role+' '+expertise)
body+='</div><p class="empty" hidden>No people match this selection.</p>'+note(ep('60a1caaaf6a6')['url'],'Official department faculty listing')+'</section>'
save('faculty.html','Faculty & administration',body,'People','Faculty research staff teaching lecturers profiles expertise')
# Student life
body=crumbs('Student Life','Life at BMD')+hero('Life is part<br>of the <em>learning.</em>','Learn with others, try something new, and connect classroom ideas with the world around you.','Student life','assets/photos/student-community.webp')+'<section class="wrap section" style="padding-top:10px"><div class="campus-grid"><figure><img src="assets/photos/cafe-project.webp" alt="Student café project" loading="lazy"><figcaption>Learning through the student café</figcaption></figure><figure><img src="assets/photos/design-workshop.webp" alt="Students participate in a collaborative design workshop" loading="lazy"><figcaption>Ideas take shape together</figcaption></figure><figure><img src="assets/photos/kayaking.webp" alt="Student activity on the water" loading="lazy"><figcaption>Experiences beyond the classroom</figcaption></figure></div></section><section class="wrap section"><div class="feature-grid">'+''.join('<article class="feature"><div class="num">EXPLORE</div><h3>'+t+'</h3><p>'+p+'</p><br>'+a(u,'Discover more '+icon(),'text-link')+'</article>' for t,p,u in [('Make something meaningful','See student projects, presentations, and applied learning.','outcomes.html'),('Explore a wider world','Discover published overseas learning and internship experiences.','exchange.html'),('Prepare for what’s next','Find internship resources and career pathway information.','internships.html')])+'</div><div style="margin-top:35px">'+source_link(ep('6ec97970ff59')['url'],'All original Student Life activities')+' &nbsp; '+source_link(ep('08f4bceb3eb0')['url'],'Virtual Corporation resource')+'</div></section>'
save('student-life.html','Life at BMD',body,'Student Life')
# Complementary topic pages
for cat,path,title,desc,img in [('international_exchange','exchange.html','The world is part of your classroom.','Explore published overseas courses, visits, internships, and cross-cultural learning opportunities.','assets/photos/international-visit.webp'),('learning_outcomes','outcomes.html','Ideas in action. Learning on display.','Discover student projects, practical experiences, and creative work from across the department.','assets/photos/design-thinking.webp'),('international_students','international.html','A wider world. A shared learning journey.','Find international-student resources, department introductions, and original campus-life information.','assets/international-student-campus-visit.webp')]:
 p=zp(cat);body=crumbs('Student Life',cat.replace('_',' ').title())+hero(title,desc,cat.replace('_',' '),img)+'<section class="wrap section split" style="padding-top:10px"><div class="lead"><h2>'+('Connect across<br><em>cultures.</em>' if cat!='learning_outcomes' else 'Create.<br>Collaborate.<br><em>Contribute.</em>')+'</h2><p>'+('Some international resources document earlier academic years and the former TCUST identity. These are kept as historical resources; use the current admission-year curriculum for current requirements.' if cat=='international_students' else 'Explore the original department resources and the experiences they document.')+'</p>'+note(p['url'])+'</div><div>'+seed_extra(p)
 if cat=='international_exchange':
  body+='<div class="feature-grid" style="grid-template-columns:1fr"><article class="feature"><h3>Overseas learning experiences</h3><p>The department’s published exchange page includes Nottingham Trent University summer learning, a ViTrox internship in Malaysia, and a visit connected with the Brand Academy in Hamburg.</p></article></div>'
 if cat=='learning_outcomes':body+='<div class="feature-grid" style="grid-template-columns:1fr"><article class="feature"><h3>The student café</h3><p>The department documents café operations as an opportunity to learn purchasing, inventory, cost control, and marketing through practice.</p></article><article class="feature"><h3>Creative student work</h3><p>Explore project presentations, intercultural activities, and the published podcast branding collection.</p></article></div>'
 if cat=='international_students':body+='<div class="note-box">Historical materials include a 2019 international introduction and orientation, a 2022 online seminar, and a Sinar Mas cooperation interview. They do not establish current admission or credit requirements.</div>'
 body+=source_link(p['url'],'Open the complete source collection')+'</div></section>'
 save(path,cat.replace('_',' ').title(),body,'Student Life')
# Careers
p=ep('c1b43ae3b734');g=zp('graduate_employment');body=crumbs('Student Life','Careers')+hero('Your learning.<br><em>A world of applications.</em>','Explore career pathways and the department’s published graduate destination information.','Career pathways')+'<section class="wrap section split" style="padding-top:0"><div class="lead"><h2>Different interests.<br>Different paths.</h2><p>The official department page identifies opportunities in marketing and logistics, retail, tourism, hospitality, local SMEs, and related industries.</p>'+note(p['url'])+'</div><div>'+tables(p['tables'])+source_link(p['url'],'View original career examples')+'</div></section><section class="wrap section" style="padding-top:0"><div class="section-head"><div><div class="kicker">Graduate destinations</div><h2>Following the next chapter.</h2></div></div><div class="note-box">The source’s positive destination figures include employment, further study, or military service. They are not employment-only rates.</div>'+tables(g['tables'])+source_link(g['url'],'View the graduate destination report')+'</section>'
save('careers.html','Career pathways & graduate destinations',body,'Student Life')
# Admissions
p=zp('admissions');body=crumbs('Admissions','Study with us')+hero('Your next chapter<br><em>starts here.</em>','Get to know the department and find the original admission presentations, guidance, and contact channels.','Study with us','assets/college-humanities-building.webp')+'<section class="wrap section split" style="padding-top:10px"><div class="lead"><h2>Curious about<br>Business Management?</h2><p>Explore the department’s latest published recruitment presentations. Confirm admission routes, dates, and eligibility through the university’s official admissions service.</p><br>'+button('https://admissions.tcu.edu.tw/','Official admissions ↗')+'</div><div><div class="kicker">Department recruitment resources</div>'+doclist(p['documents'])+seed_extra(p)+note(p['url'],'Original admission information and department contact channels')+'</div></section><section class="wrap section faq" style="padding-top:0"><div class="section-head"><h2>A few useful starting points.</h2></div><details><summary>Where can I see the courses?</summary><p>Explore the '+a('curriculum.html','curriculum by admission year')+' and original bilingual documents.</p></details><details><summary>Where do international applicants start?</summary><p>Use the university’s '+a('https://admissions.tcu.edu.tw/','official admissions website')+' for current routes and requirements.</p></details><details><summary>How can I contact the department?</summary><p>Email '+a('mailto:ss62@gms.tcu.edu.tw','ss62@gms.tcu.edu.tw')+' or call +886-3-857-2677 ext. 31682.</p></details></section>'
save('admissions.html','Admissions',body,'Admissions')
# News hub + article pages
body=crumbs('News','News & achievements')+hero('What’s happening.<br><em>What’s possible.</em>','Department announcements, student achievements, and stories from our learning community.','News & stories')+'<section class="wrap section" style="padding-top:0" data-filter-scope><div class="tool-row"><input class="filter-input" data-filter-input type="search" placeholder="Search news…" aria-label="Search news"><div class="filters">'+''.join(f'<button class="filter {"active" if c=="all" else ""}" data-filter="{c}" aria-pressed="{str(c=="all").lower()}">{l}</button>' for c,l in [('all','All stories'),('announcements','Announcements'),('achievements','Achievements'),('archive','Archive')])+'</div></div><div class="news-grid">'+''.join(news_card(n) for n in NEWS)+'</div><p class="empty" hidden>No stories match your search.</p></section>'
save('news.html','News & achievements',body,'News','Announcements achievements lectures projects competitions activities')
for n in NEWS:
 body=crumbs('News','Department story')+'<div class="wrap feature-article">'+hero(h(n['title']),h(n['summary']),n['label'])
 if n['image']:body+='<a href="'+h(n['image'])+'" target="_blank" rel="noopener"><img src="'+h(n['image'])+'" alt="'+h(n['title'])+'" style="width:100%;max-height:1100px;object-fit:contain;background:#edf3e7"></a>'
 body+='<div class="section prose"><p>'+a(n['url'],'Read the original department announcement ↗','text-link',True)+'</p><p>Event details and any registration instructions are provided in the original announcement or poster.</p></div></div>'
 save(n['path'],n['title'],body,'Historical archive' if n['category']=='archive' else 'News',n['summary'])
# Existing academic calendar
EVENTS=json.loads((R/'academic-events.json').read_text())['events']
body=crumbs('News','Academic calendar')+hero('Make room<br>for <em>what’s next.</em>','Explore the academic dates already published in your website’s 2026–2027 calendar. Select a day to filter the listed events.','Academic calendar')+'<section class="wrap section" style="padding-top:0"><div class="calendar-layout"><div class="calendar" id="calendar"><div class="calendar-head"><button id="cal-previous" aria-label="Previous month">←</button><h3 id="calendar-month">October 2026</h3><button id="cal-next" aria-label="Next month">→</button></div><div class="weekdays">'+''.join('<span>'+x+'</span>' for x in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])+'</div><div class="days" id="calendar-days"></div></div><div><div class="kicker">Dates to know</div><h2 id="event-list-title" style="font-size:31px">October 2026</h2><div id="calendar-events" aria-live="polite"></div></div></div><div class="source-note">'+a('assets/academic-calendar-2026-2027.pdf','Download the full academic calendar PDF ↗',external=True)+'</div><script type="application/json" id="calendar-data">'+json.dumps(EVENTS,ensure_ascii=False).replace('</', '<' + chr(92) + '/')+'</script></section>'
save('events.html','Academic calendar 2026–2027',body,'News','Academic calendar semester holiday exam events')
# All forms/documents
DOCS=[]
for p in E:
 for l in p.get('links',[]):
  if re.search(r'\.(pdf|docx?|xlsx?|pptx?)(?:$|\?)',l['url'],re.I):DOCS.append({'url':l['url'],'label':l.get('text') or p['title'],'context':p['title']})
for p in Z:DOCS.extend(p.get('documents',[]))
DOCS.append({'url':'assets/academic-calendar-2026-2027.pdf','label':'Academic calendar 2026–2027','context':'Original academic calendar from the existing website'})
unique={d['url']:d for d in DOCS};DOCS=[normalize_document(d) for d in unique.values()]
body=crumbs('Academics','Resources')+hero('The essentials,<br><em>all in one place.</em>','Find original curriculum documents, policies, internship forms, recruitment presentations, and faculty resources.','Resources & documents')+'<section class="wrap section" style="padding-top:0" data-filter-scope><div class="tool-row"><input class="filter-input" data-filter-input type="search" aria-label="Search resources" placeholder="Search by title, year, or keyword…">'+a('regulations.html','Department regulations '+icon(),'text-link')+'</div>'+doclist(DOCS)+'<p class="empty" hidden>No resources match your search.</p></section>'
save('resources.html','Forms & learning resources',body,'Resources',' '.join(x['label'] for x in DOCS))
# Contact
body=crumbs('Department','Contact')+hero('Start a conversation.','Questions about the department, curriculum, or studying with us? Get in touch.','Contact')+'<section class="wrap section contact-grid" style="padding-top:0"><div class="contact-card"><div class="kicker">Department of Business Management</div><h2>We’re here to help.</h2><dl><dt>Email</dt><dd>'+a('mailto:ss62@gms.tcu.edu.tw','ss62@gms.tcu.edu.tw')+'</dd><dt>Phone</dt><dd>'+a('tel:+88638572677','+886-3-857-2677 ext. 31682')+'</dd><dt>Address</dt><dd>67 Jieren St., Hualien 97074, Taiwan</dd><dt>Fax</dt><dd>+886-3-856-0713</dd></dl></div><div><img src="assets/campus-main-building.webp" alt="Tzu Chi University campus" style="width:100%;height:290px;border-radius:14px"><div style="margin-top:26px">'+a('https://www.google.com/maps/search/?api=1&query=67+Jieren+St+Hualien+Taiwan','Find the campus on Google Maps ↗','text-link',True)+'</div>'+note('https://mdm.tcu.edu.tw/?Lang=en','Contact details from the official English department website')+'</div></section>'
save('contact.html','Contact the department',body,'Contact','email phone address Hualien')
# Complete source reading pages, linked from hubs and coverage directory.
noise=['字體大小調整','本功能需使用支援','This function need','Small','Middle','Large','首頁']
for u,p in SOURCES.items():
 title=p.get('title','Department resource').replace(' - 慈濟大學-經營管理學系','').strip();content='';archival=bool(re.search(r'44332|44331|44230|15707|2009|2019|5429',u)) or any(n['url']==u and n['category']=='archive' for n in NEWS)
 if p in E:
  raw=p.get('clean_html','')
  try:
   root=LH.fragment_fromstring(raw,create_parent='div')
   for bad in root.xpath('.//script|.//style|.//form|.//input|.//button|.//*[contains(@class,"mtoolbar") or contains(@class,"fontsize") or contains(@class,"page-header")]'):bad.drop_tree()
   for el in root.iter():
    if el.tag=='h1':el.tag='h2'
    for att in list(el.attrib):
     if att.startswith('on') or att in ['style','class','id','width','height']:el.attrib.pop(att,None)
    if el.tag=='a':
     href=urllib.parse.urljoin(u,el.get('href',''))
     if href.startswith(('javascript:','data:')):el.attrib.pop('href',None)
     else:el.set('href',source_map.get(href,href));el.set('rel','noopener')
    if el.tag=='img':
     if 'acc.tccn.edu.tw' in el.get('src',''):
      el.tag='p';el.text='Historical image unavailable from the original host; consult the original publication.';el.attrib.clear();continue
     src=urllib.parse.urljoin(u,el.get('src',''));el.set('src',source_image(src));el.set('loading','lazy');el.set('alt',el.get('alt') or title)
    if el.tag=='iframe':el.set('src',urllib.parse.urljoin(u,el.get('src','')));el.set('loading','lazy');el.set('title',title)
   content=LH.tostring(root,encoding='unicode',method='html')
  except Exception:content='<p>'+h(p.get('text',''))+'</p>'
  if re.search(r',r1.php',u):
   n=next((n for n in NEWS if n['url']==u),None)
   if n:content='<p>'+h(n['summary'])+'</p>'+('<img src="'+h(n['image'])+'" alt="'+h(n['title'])+'">' if n['image'] else '')+a(n['path'],'Open the redesigned story '+icon(),'text-link')
 else:
  # Keep the original-language text, tables, linked media and documents available in the source collection.
  blocks=p.get('blocks',[]);rowtext={' '.join(row) for t in p.get('tables',[]) for row in t};seen=set()
  for b in blocks:
   b=b.strip()
   if not b or b in seen or b in rowtext or any(n in b for n in noise) or b==title:continue
   seen.add(b);content+='<p>'+h(b)+'</p>'
  content+=tables(p.get('tables',[]))+doclist(p.get('documents',[]))+seed_extra(p)
  for im in p.get('images',[]):
   src=im.get('url','')
   if im.get('local_asset') and not src:src=source_image(im['local_asset'])
   if im.get('local_asset'):
    local=Path(im['local_asset']);local=local if local.is_absolute() else (R/'official-zh'/local)
    if local.exists():
     target=D/'assets/source-images'/local.name;target.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(local,target);src=str(target.relative_to(D))
   elif src:src=source_image(src)
   if src:content+='<a href="'+h(src)+'" target="_blank" rel="noopener"><img src="'+h(src)+'" alt="'+h(im.get('alt') or title)+'" loading="lazy"></a>'
  useful=[l for l in p.get('links',[]) if l.get('url','').startswith(('http','https')) and l['url'] not in SOURCES and not re.search(r'\.(pdf|docx?|pptx?|xlsx?)($|\?)',l['url'],re.I)]
  if useful:content+='<h2>Linked resources</h2>'+doclist(useful)
 body=crumbs('Source collection',title)+hero(h(title),'Original department materials, presented in their publication language.','Department source collection')+'<section class="wrap section" style="padding-top:0">'+('<div class="note-box">Historical resource: some information reflects the former TCUST identity or an earlier academic year. Refer to current admission-year documents for current requirements.</div>' if archival else '')+'<div class="source-body">'+content+'</div>'+note(u,'Read the original publication')+'</section>'
 save(source_path(u),title,body,'Historical source' if archival else 'Source collection',p.get('text','') if p in E else ' '.join(p.get('blocks',[])))
# Sources and content review: finite coverage is explicit.
body=crumbs('About','Content coverage')+hero('Sources you can trace.','A transparent directory of the official pages and resources used in this student redesign.','Content coverage')+'<section class="wrap section" style="padding-top:0"><div class="migration-grid"><article><b>'+str(len(SOURCES))+'</b><small>Captured official source pages</small></article><article><b>'+str(len(F))+'</b><small>Faculty and staff profiles</small></article><article><b>'+str(len(DOCS))+'</b><small>Original document resource links</small></article></div><div class="note-box">Coverage includes the major English and Chinese department menus and their discovered content pages. Linked university services, social media, original documents, and external sites remain external. News summaries retain links to the original announcements; event posters are preserved. This is a documented migration of the captured sources, not a claim that every historical or external page has been replicated.</div><details class="faq"><summary>Source differences and unavailable material</summary><div class="prose"><p>The English introduction’s history infographics contain dates that conflict with the university academic record. The redesigned history follows the university academic record (2000, 2004, 2013, 2023) and the 2024 merger announcement; original infographics remain available in the source collection.</p><p>One linked English news article returned HTTP 404: <a href="https://mdm.tcu.edu.tw/p/406-1021-64534,r1.php?Lang=en">original URL</a>. Its full content could not be migrated.</p><p>Three images from a legacy gallery host could not be retrieved and are identified as unavailable in the source collection. Some published faculty external-profile links appear to point to a different person; curated profiles use the original department profile and CV resources, while the source collection retains the published record.</p><p>Publication dates were not exposed for several announcements. No publication dates have been inferred from crawl dates or award years.</p><p>International materials dated 2019 and the 2022 seminar are labelled historical. Faculty contact details are kept with their source because listing and profile pages can differ.</p></div></details><div data-filter-scope style="margin-top:35px"><input class="filter-input" data-filter-input aria-label="Search source directory" placeholder="Find an original source…"><div class="resource-list">'
for u,p in SOURCES.items():body+='<a data-filter-item class="resource-link" href="'+source_path(u)+'"><div><b>'+h(p.get('title','Department resource'))+'</b><small>'+h(u)+'</small></div><span class="type">Read ↗</span></a>'
body+='</div><p class="empty" hidden>No sources match this search.</p></div></section>'
save('content-review.html','Sources & content coverage',body,'About','Migration audit source original references history conflicts archives')
SEARCH.extend({'url':d['url'],'title':d['label'],'category':'Original document','text':d.get('context','')} for d in DOCS)
(D/'assets/search-index.json').write_text(json.dumps(SEARCH,ensure_ascii=False))
(ROOT/'route-manifest.json').write_text(json.dumps({'pages':SEARCH,'sources':source_map,'documents':DOCS,'events_count':len(EVENTS),'redirects':RETIRED},ensure_ascii=False,indent=2))
from quiet_ui import quiet_document
(D/'404.html').write_text(quiet_document(cache_assets(head('Page not found').replace('</head>','<link rel="stylesheet" href="assets/quiet-ui.css"><link rel="stylesheet" href="assets/campus-refinement.css"><link rel="stylesheet" href="assets/edition.css"><script defer src="assets/campus-refinement.js"></script></head>'))+header('404.html')+'<main id="main">'+hero('Let’s find your way.','This page is not available. Use the navigation or search to find the department information you need.','404')+'<section class="wrap section">'+button('index.html','Back to home')+'</section></main>'+footer(),'404.html'))
from localization import build_languages
build_languages(ROOT)
print(json.dumps({'site_pages':len(list(D.glob('*.html'))),'official_sources':len(SOURCES),'faculty':len(F),'documents':len(DOCS),'news':len(NEWS),'calendar_events':len(EVENTS),'image_mapping':len(IM)},indent=2))

# Keep generated HTML free of source-editor trailing spaces.
for generated in D.glob('*.html'):
 generated.write_text('\n'.join(re.sub(r'^[ \t]+',lambda m:m.group().expandtabs(2),line).rstrip(' \t') for line in generated.read_text().split('\n')))

for excluded in (p for p in E if p.get('status')=='excluded'):
 forbidden=[excluded['url'],excluded.get('title',''),sha(excluded['url'])]
 for public in [*D.glob('*.html'),D/'assets/search-index.json']:
  published=public.read_text()
  assert not any(value and value in published for value in forbidden),f'Excluded record in {public.name}'
