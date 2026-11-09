"""A restrained editorial pass over the established Green Campus pages.

Photography and descriptions refer only to the retained department publications.
No quotations, dates, programme promises, or student identities are inferred.
"""
from html import escape
from lxml import html as LH
import json


def select(root, cls):
    return root.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," '+cls+' ")]')


def contents(element, markup):
    for child in list(element):
        element.remove(child)
    fragment = LH.fragment_fromstring(markup, create_parent='div')
    element.text = fragment.text
    for child in list(fragment):
        element.append(child)


LEADS = {
    'introduction': 'Business education in Hualien, with practical management skills, teamwork, and professional ethics at its centre.',
    'student-life': 'A project presentation, a design workshop, a day at Liyu Lake. A few scenes from the department’s student-life collection.',
    'exchange': 'Summer study in the UK, an internship in Malaysia, and conversations with visiting educators on campus. Reports from the department’s international-learning collection.',
    'outcomes': 'Café operations, project presentations, and podcast branding: student work published by the department.',
    'international': 'Department introductions, campus-life materials, and resources for international students, with earlier publications identified as historical.',
    'academics': 'Four teaching areas, with course lists and curriculum maps organised by entry year.',
    'curriculum': 'Choose your entry year for the published course list and curriculum map. Each cohort’s requirements belong to its own documents.',
    'admissions': 'Department presentations and application contacts, with current routes and deadlines provided by the university’s admissions service.',
    'careers': 'Published career examples and graduate destinations, with the programme and reporting period shown alongside the data.',
    'events': 'Selected dates from the university’s 2026–2027 academic calendar. Choose a day for its listed events, or open the full calendar.',
    'resources': 'Course documents, internship forms, department policies, and recruitment presentations. Search by title, entry year, or subject.',
    'contact': 'For curriculum, department, and application enquiries, contact the department office in Hualien.',
}


def refine(path, body, content_root):
    key = path.removesuffix('.html')
    root = LH.fragment_fromstring(body, create_parent='div')
    hero = next(iter(select(root, 'page-hero')), None)
    if hero is not None and key in LEADS:
        paragraphs = hero.xpath('./div[1]/p')
        if paragraphs:
            paragraphs[0].text = LEADS[key]

    # Supply natural-size geometry, specific alt text, and visible provenance.
    photos = json.loads((content_root.parent/'dist/assets/photos/source-manifest.json').read_text())
    photo_map = {p['relative_file']: p for p in photos}
    for image in root.xpath('.//img'):
        record = photo_map.get(image.get('src'))
        image.set('decoding', 'async')
        if record:
            image.set('width', str(record['width']))
            image.set('height', str(record['height']))
            image.set('alt', record['caption'])
    if hero is not None:
        frames = select(hero, 'interior-photo')
        if frames:
            frame = frames[0]
            image = frame.xpath('./img')[0]
            record = photo_map.get(image.get('src'))
            if record:
                frame.tag = 'figure'
                caption = LH.Element('figcaption', {'class': 'editorial-caption'})
                caption.text = record['caption']+'. '
                credit = LH.Element('span')
                credit.text = 'Department photo archive'
                caption.append(credit)
                frame.append(caption)

    if key == 'index':
        # Keep every established homepage section, slider and control.
        memory = select(root, 'hero-memory')[0]
        memory.set('href', 'outcomes.html')
        memory.xpath('.//b')[0].text = 'Student projects'
        for index, link in enumerate(select(root, 'pathway-card')):
            link.set('href', f'academics.html#learning-tab-{index}')
        directions = select(root, 'pathways-heading')[0]
        directions.xpath('./p')[0].text = 'Operations, digital business, sustainability, and culinary management. Course lists are published separately for each entry year.'
        select(root, 'life-text')[0].xpath('./p')[0].text = 'The department’s photo archive follows students through café projects, design workshops, and cross-cultural activities. The student-life collection brings these moments together.'
        for link in select(root, 'campus-secondary'):
            contents(link, 'About the department <span>↗</span>')
        for link in root.xpath('.//a[contains(@class,"button")]'):
            if link.get('href') == 'academics.html':
                # Preserve the existing icon.
                link.text = 'Learning directions '
        for link in select(root, 'stories-heading-right')[0].xpath('./a'):
            link.text = 'All department news '

    elif key == 'introduction':
        grid = select(root, 'feature-grid')[0]
        grid.set('class', grid.get('class')+' editorial-principles')
        for index, card in enumerate(select(grid, 'feature')):
            number = LH.Element('span', {'class':'editorial-index','aria-hidden':'true'})
            number.text = f'0{index+1}'
            card.insert(0, number)
        descriptions = [
            'Café operations and student projects give management concepts a practical setting.',
            'Teamwork, creative thinking, and cross-cultural understanding are part of the department’s educational goals.',
            'Humanistic qualities and workplace ethics sit alongside business knowledge in the department’s published goals.',
        ]
        for card, text in zip(select(grid, 'feature'), descriptions):
            card.xpath('./p')[0].text = text
        for label, text in zip(select(root, 'interior-next')[0].xpath('.//span'), ['Vision & mission', 'Department history']):
            label.text = text

    elif key == 'student-life':
        gallery = select(root, 'life-gallery')[0]
        gallery.set('aria-label', 'Scenes from department life')
        scenes = [
            ('01 / In practice', 'Student presentations', 'Students in the department’s Indonesian cohort present work combining marketing ideas, English, and multimedia.'),
            ('02 / Working together', 'Ideas on the wall', 'Students share ideas during a design-thinking workshop.'),
            ('03 / Hualien · Liyu Lake', 'Time on the water', 'Local and international students take part in a kayaking activity at Liyu Lake.'),
        ]
        for figure, (label, title, copy) in zip(gallery.xpath('./figure'), scenes):
            button = figure.xpath('./button')[0]
            button.set('data-gallery-caption', title+' — '+copy)
            button.set('aria-label', 'View photo: '+title)
            contents(figure.xpath('./figcaption')[0], '<span class="editorial-index">'+escape(label)+'</span><h2>'+escape(title)+'</h2><p>'+escape(copy)+'</p>')
        note = LH.Element('p', {'class':'wrap photo-archive-note'})
        note.text = 'Photographs from the department’s published student-life collection. Dates are not supplied for every image.'
        gallery.addnext(note)
        grid = select(root, 'feature-grid')[0]
        grid.set('class', grid.get('class')+' editorial-link-list')
        for br in grid.xpath('.//br'):
            br.getparent().remove(br)
        copies = [
            'Project presentations, café operations, and student-made podcast branding.',
            'Published accounts of overseas study, internships, and visiting educators.',
            'Internship preparation, department forms, and workplace guidance.',
        ]
        for card, copy in zip(select(grid, 'feature'), copies):
            card.xpath('./p')[0].text = copy

    elif key == 'exchange':
        section = select(root, 'published-experiences')[0]
        section.xpath('./h2')[0].text = 'From the department’s records'
        section.xpath('./p')[0].text = 'Summer study, workplace experience, and visiting educators. These published reports describe past experiences; current application details should be confirmed with the department.'
        for index, card in enumerate(select(section, 'experience-card')):
            label = card.xpath('./span')[0]
            label.text = f'0{index+1} / '+label.text

    elif key == 'outcomes':
        grid = select(root, 'feature-grid')[0]
        grid.set('class', grid.get('class')+' project-notes')
        project = select(grid, 'feature')[1]
        photo = LH.Element('figure', {'class':'project-photo'})
        photo.append(LH.fromstring('<img src="assets/photos/cafe-project.webp" width="1200" height="675" alt="Students from the department’s Indonesian cohort presenting a project" loading="lazy" decoding="async">'))
        cap = LH.Element('figcaption', {'class':'editorial-caption'})
        cap.text = 'Student project presentation · Indonesian cohort · Department photo archive'
        photo.append(cap)
        project.insert(0, photo)
        for card in select(grid, 'feature'):
            title = card.xpath('./h3')[0]
            title.tag = 'h2'
        select(grid, 'feature')[1].xpath('./p')[0].text = 'The department publishes project presentations and a podcast-branding collection. The original materials keep the students’ work in its published context.'
        for link in root.xpath('.//a[@href="source-01264718904c.html"]'):
            link.text = 'Podcast branding · 113–2 student collection ↗'
        lead = select(root, 'lead')[0]
        lead.xpath('./p')[0].text = 'Original work and applied-learning materials, as published by the department.'

    elif key == 'academics':
        for card, label in zip(select(root, 'feature'), ['Course documents', 'Certificate points', 'Forms and policies']):
            for number in select(card, 'num'):
                number.getparent().remove(number)
            for link in card.xpath('./a'):
                link.text = label+' '

    elif key == 'resources':
        # Already present in the shortcuts above; keep one clear route.
        for link in select(root, 'tool-row')[0].xpath('./a[@href="regulations.html"]'):
            link.getparent().remove(link)

    elif key == 'careers':
        headings = select(root, 'section-head')
        for heading in headings:
            for kicker in select(heading, 'kicker'):
                kicker.getparent().remove(kicker)

    return ''.join(LH.tostring(child, encoding='unicode', method='html') for child in root)


def navigation(markup, path):
    root = LH.fragment_fromstring(markup, create_parent='div')
    current = path
    if path.startswith('faculty-'):
        current = 'faculty.html'
    elif path.startswith('news-'):
        current = 'news.html'
    for nav in select(root, 'primary-nav'):
        for link in nav.xpath('.//a'):
            if link.get('href') == current:
                if current == path:
                    link.set('aria-current', 'page')
                else:
                    link.set('class', 'current-parent')
                group = link.getparent()
                if group.get('class') == 'dropdown':
                    group.getparent().set('class', 'nav-group current-section')
        if path == 'regulations.html':
            for group in select(nav, 'nav-group'):
                if group.xpath('.//a[@href="resources.html"]'):
                    group.set('class', 'nav-group current-section')
    for link in select(root, 'apply'):
        if path == 'admissions.html':
            link.set('aria-current', 'page')
    return ''.join(LH.tostring(child, encoding='unicode', method='html') for child in root)
