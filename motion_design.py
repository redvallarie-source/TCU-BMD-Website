"""Focused motion direction, applied after the existing editorial content pass."""
from html import escape
from lxml import html as LH
import json

MOTION_PAGES = {'index.html', 'introduction.html', 'academics.html', 'student-life.html',
                'outcomes.html', 'exchange.html', 'admissions.html'}


def select(root, cls):
    return root.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," '+cls+' ")]')


def node(markup):
    return LH.fromstring(markup)


def replace(element, markup):
    for child in list(element):
        element.remove(child)
    fragment = LH.fragment_fromstring(markup, create_parent='div')
    element.text = fragment.text
    for child in list(fragment):
        element.append(child)


def hero(media):
    has_film = bool(media.get('hero'))
    picture = media.get('poster', 'assets/campus-main-building.webp')
    film = ''
    if has_film:
        film = f'''<video id="campus-film" class="campus-film" muted playsinline loop preload="none" poster="{escape(picture)}" data-film-src="{escape(media['hero'])}" data-film-small="{escape(media.get('hero_small', media['hero']))}" aria-hidden="true" disablepictureinpicture></video>'''
    photos = [
        ('assets/campus-main-building.webp', 'Tzu Chi University campus', 'Campus architecture'),
        ('assets/campus-mountain-building.webp', 'Tzu Chi University with the mountains of Hualien', 'Hualien, Taiwan'),
        ('assets/photos/student-community.webp', 'Students and faculty in a department group photograph', 'The BMD community'),
    ]
    options = ([('film', 'Film', 'Show campus film')] if has_film else [])
    options += [(str(i), f'0{i+1}', 'Show photo: '+p[2]) for i, p in enumerate(photos)]
    credit = media.get('source_page', 'https://www.tcu.edu.tw/')
    label = media.get('credit', 'Tzu Chi University')
    return f'''<section class="dynamic-hero cinema-hero" aria-label="Business Management at Tzu Chi University">
<div class="hero-photos" aria-hidden="true">{''.join('<img class="campus-slide'+(' active' if i==0 else '')+'" src="'+p[0]+'" alt="" decoding="async"'+(' fetchpriority="high"' if i==0 else ' loading="lazy"')+'>' for i,p in enumerate(photos))}</div>
{film}<div class="campus-shade"></div>
<div class="wrap dynamic-hero-content"><div class="hero-title-block"><div class="hero-eyebrow">TZU CHI UNIVERSITY <span aria-hidden="true"></span> BUSINESS MANAGEMENT</div>
<h1 id="campus-title">Business<br><em>with purpose.</em></h1><p id="campus-description">Practical learning. Human perspective.<br>Here in Hualien.</p>
<div class="campus-actions"><a class="button light" href="academics.html">Learning directions <span aria-hidden="true">↗</span></a><a class="campus-secondary" href="introduction.html">About BMD <span aria-hidden="true">↗</span></a></div></div>
<a class="hero-scroll" href="#from-bmd"><span>From BMD</span><span aria-hidden="true">↓</span></a></div>
<div class="hero-bottom-line"><div class="wrap hero-bottom-inner"><div class="film-caption"><span id="campus-scene">{'Campus film' if has_film else 'Campus architecture'}</span><a id="campus-credit" href="{escape(credit)}" target="_blank" rel="noopener" data-initial-href="{escape(credit)}" data-initial-label="{escape(label)}">{escape(label)} ↗</a></div>
<div class="campus-controls"><button class="campus-pause" type="button" aria-label="Pause hero motion" aria-pressed="false"><span aria-hidden="true">Ⅱ</span></button><div class="campus-dots" aria-label="Choose hero media">{''.join('<button type="button" data-hero-mode="'+v+'" aria-label="'+alt+'" aria-pressed="'+str(i==0).lower()+'"'+(' class="selected"' if i==0 else '')+'>'+label+'</button>' for i,(v,label,alt) in enumerate(options))}</div><button class="campus-prev" type="button" aria-label="Previous hero view">←</button><button class="campus-next" type="button" aria-label="Next hero view">→</button></div></div></div><span class="sr-only" id="campus-announcement" aria-live="polite"></span></section>'''


def life():
    scenes = [
        ('assets/photos/design-workshop.webp', 'Students sharing ideas in a design-thinking workshop', 'Design-thinking workshop · Department archive', 'practice.'),
        ('assets/photos/design-thinking.webp', 'Students and a visiting educator at a workshop', 'Workshop with a visiting educator · Department archive', 'projects.'),
        ('assets/photos/kayaking.webp', 'Local and international students kayaking at Liyu Lake', 'Liyu Lake, Hualien · Student activity', 'action.'),
    ]
    return '''<section class="home-life motion-region editorial-motion" aria-labelledby="life-heading"><div class="wrap life-layout"><div class="life-text"><div class="kicker">Learning in practice</div>
<h2 id="life-heading" class="kinetic-heading"><span data-reveal-line>Ideas into</span><span class="sr-only">practice, projects, and action.</span><span class="word-window" aria-hidden="true"><span class="word-track">'''+''.join('<span>'+s[3]+'</span>' for s in scenes)+'''</span></span></h2>
<p>Student projects. Design workshops.<br>Learning with others.</p><div class="life-routes"><a href="student-life.html"><span>Student life</span><b aria-hidden="true">↗</b></a><a href="outcomes.html"><span>Student work</span><b aria-hidden="true">↗</b></a><a href="exchange.html"><span>International learning</span><b aria-hidden="true">↗</b></a></div>
<div class="life-motion-controls"><div class="life-steps" aria-label="Choose a student-life scene">'''+''.join('<button type="button" data-life-step="'+str(i)+'" aria-label="Show scene: '+s[3].rstrip('.')+'" aria-pressed="'+str(i==0).lower()+'">0'+str(i+1)+'</button>' for i,s in enumerate(scenes))+'''</div><button class="motion-toggle" type="button" aria-pressed="false" aria-label="Pause section animation"><span class="motion-state" aria-hidden="true">Ⅱ</span><span class="motion-label">Motion on</span></button></div></div>
<figure class="life-stage" data-photo-drift><div class="life-photo-window">'''+''.join('<img class="life-scene'+(' active' if i==0 else '')+'" data-life-scene="'+str(i)+'" src="'+s[0]+'" alt="'+s[1]+'" loading="lazy" decoding="async" width="'+'960'+'" height="'+('542' if i==2 else '719')+'"'+(' aria-hidden="true"' if i else '')+'>' for i,s in enumerate(scenes))+'''</div><figcaption id="life-scene-caption">'''+scenes[0][2]+'''</figcaption><script type="application/json" id="life-scene-data">'''+json.dumps([s[2] for s in scenes])+'''</script></figure></div></section>'''


def apply_motion(path, body, content_root):
    if path not in MOTION_PAGES:
        return body
    root = LH.fragment_fromstring(body, create_parent='div')
    if path == 'index.html':
        config = content_root/'motion-media.json'
        media = json.loads(config.read_text()) if config.exists() else {}
        old = select(root, 'dynamic-hero')[0]
        old.getparent().replace(old, node(hero(media)))
        for script in root.xpath('.//script[@id="campus-copy"]'):
            script.getparent().remove(script)
        old = select(root, 'home-life')[0]
        old.getparent().replace(old, node(life()))
        stories = select(root, 'home-stories')[0]
        stories.set('id', 'from-bmd')
        stories.xpath('.//h2')[0].text = 'News & achievements'
        for el in select(root, 'carousel-caption')[0].xpath('./span[1]'):
            el.text = 'From the department'
        quick=select(root, 'quick-card')
        if quick:quick[-1].xpath('.//p')[0].text='Presentations and student-made projects.'
        select(root, 'pathways-heading')[0].xpath('./p')[0].text = 'Four teaching areas. Find the curriculum for your entry year.'
        select(root, 'agenda-heading')[0].xpath('./div[2]/p')[0].text = 'Selected university dates, in Taiwan time.'
        select(root, 'home-final')[0].xpath('./div[2]/p')[0].text = 'Application information and department contacts.'
        for cls in ['pathways-heading', 'agenda-heading', 'home-final']:
            for heading in select(root, cls)[0].xpath('.//h2'):
                heading.set('data-editorial-reveal', '')
        for el in select(root, 'ambient-layer'):
            # One quiet moving region remains at the close of the page.
            el.set('class', el.get('class')+' restrained-ambient')
    else:
        heroes = select(root, 'page-hero')
        if heroes:
            concise = {
                'student-life.html': 'Student presentations, a design workshop, a day at Liyu Lake.',
                'exchange.html': 'Overseas study, internships, and visiting educators. Experiences from the department’s records.',
                'admissions.html': 'Department presentations, application information, and contacts.',
            }
            if path in concise:
                paragraphs=heroes[0].xpath('./div[1]/p')
                if paragraphs:paragraphs[0].text=concise[path]
            for heading in heroes[0].xpath('.//h1'):
                heading.set('data-editorial-reveal', '')
            for photo in select(heroes[0], 'interior-photo'):
                photo.set('data-photo-drift', '')
        if path == 'student-life.html':
            for caption in root.xpath('.//figcaption[h2]'):
                caption.set('data-editorial-reveal', '')
        if path == 'introduction.html':
            for heading in select(root, 'intro-story')[0].xpath('.//h2'):
                heading.set('data-editorial-reveal', '')
        if path == 'outcomes.html':
            for photo in select(root, 'project-photo'):
                photo.set('data-photo-drift', '')
    return ''.join(LH.tostring(child, encoding='unicode', method='html') for child in root)
