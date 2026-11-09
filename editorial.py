"""Editorial finish: clear labels, specific captions, and quieter decoration."""
from lxml import html as LH
from html import escape
import json

TITLES={
    'introduction':'Business Management<br><em>at Tzu Chi University.</em>',
    'vision':'Vision &amp; Mission',
    'history':'Department history',
    'academics':'Learning directions',
    'curriculum':'Curriculum by entry year',
    'requirements':'Certificate requirements',
    'faculty':'Faculty &amp; staff',
    'student-life':'Student life at BMD',
    'exchange':'International learning',
    'outcomes':'Student projects',
    'international':'International students',
    'careers':'Career pathways',
    'admissions':'Study at BMD',
    'news':'News &amp; announcements',
    'events':'Academic calendar',
    'resources':'Documents &amp; forms',
    'regulations':'Department regulations',
    'internships':'Internship resources',
    'contact':'Contact the department',
}
HEADINGS={
    'Knowledge. Character. Connection.':'How we learn',
    'A practical next step.':'Certificate points',
    'Learn confidently.':'Department policies',
    'Prepare. Participate. Reflect.':'Before your internship',
    'Connect across cultures.':'Learning across cultures',
    'Create. Collaborate. Contribute.':'Learning through projects',
    'Different interests. Different paths.':'Where graduates can work',
    'Following the next chapter.':'Graduate destinations',
    'Curious about Business Management?':'Applying to the department',
    'A few useful starting points.':'Questions about applying',
    'We’re here to help.':'Department office',
    'Learn with purpose':'Classroom and practice',
    'Grow with others':'Working with others',
    'Lead with responsibility':'Responsible decisions',
    'Make something meaningful':'Student projects',
    'Explore a wider world':'International experiences',
    'Prepare for what’s next':'Internships and careers',
}
ICONS={
    'admissions':'<path d="m3 8 9-5 9 5-9 5-9-5Zm4 3v6c3 3 7 3 10 0v-6m4-3v8"/>',
    'curriculum':'<path d="M12 5C8 2 4 3 2 4v15c3-1 6-1 10 2m0-16c4-3 8-2 10-1v15c-3-1-6-1-10 2V5Z"/>',
    'faculty':'<circle cx="9" cy="7" r="3"/><path d="M2 21v-3a7 7 0 0 1 14 0v3m1-17a3 3 0 0 1 0 6m3 11v-4a5 5 0 0 0-3-4"/>',
    'internships':'<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4M3 12c6 4 12 4 18 0m-9 0v4"/>',
    'exchange':'<circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="4" ry="10"/><path d="M2 12h20M4 6h16M4 18h16"/>',
    'outcomes':'<rect x="3" y="4" width="18" height="14" rx="1"/><path d="M8 22h8m-4-4v4M7 14V9m5 5V7m5 7v-3"/>',
    'operations':'<rect x="2" y="2" width="7" height="7" rx="1"/><rect x="15" y="15" width="7" height="7" rx="1"/><path d="M9 5h10v10M5 9v10h10"/>',
    'smart':'<rect x="2" y="3" width="20" height="15" rx="2"/><path d="M8 22h8m-4-4v4M6 13l4-4 4 2 4-5"/>',
    'sustainable':'<path d="M4 20C0 8 10 3 21 3c0 13-7 20-17 17Zm0 0L18 6m-9 9V8m5 4h5"/>',
    'culinary':'<path d="M6 2v7m-3-7v5a3 3 0 0 0 6 0V2M6 10v12M19 2c-4 2-5 6-5 10h5m0-10v20"/>',
}
def svg(name):return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ICONS[name]+'</svg>'
def select(root,cls):return root.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," '+cls+' ")]')
def replace_contents(el,markup):
    for child in list(el):el.remove(child)
    el.text=None
    fragment=LH.fragment_fromstring(markup,create_parent='div');el.text=fragment.text
    for child in list(fragment):el.append(child)
def set_first(root,selector,markup):
    elements=select(root,selector)
    if elements:replace_contents(elements[0],markup)
def remove(root,cls):
    for el in select(root,cls):el.getparent().remove(el)
def polish(path,body):
    key=path.removesuffix('.html');root=LH.fragment_fromstring(body,create_parent='div')
    if key in TITLES:
        heading=root.xpath('.//h1')
        if heading:replace_contents(heading[0],TITLES[key])
        crumbs=select(root,'crumbs')
        if crumbs:
            spans=crumbs[0].xpath('./span')
            label={'introduction':'Introduction','admissions':'Admissions'}.get(key,LH.fromstring('<span>'+TITLES[key]+'</span>').text_content())
            if spans:spans[-1].text=label
        heroes=select(root,'page-hero')
        if heroes:
            # Breadcrumb and page title already identify the subject.
            remove(heroes[0],'kicker')
    if key in TITLES:
        for heading in root.xpath('.//h2|.//h3'):
            text=' '.join(' '.join(heading.itertext()).split())
            if text in HEADINGS:replace_contents(heading,escape(HEADINGS[text]))
    for cls in ['life-spark','life-note','ambient-seed','history-art-label','history-art-note','purpose-orbit','purpose-foot','value-symbol','photo-corner']:
        remove(root,cls)
    if key=='index':
        copies=[
            ['Business<br><em>with purpose.</em>','Study business management in Hualien.<br>Learn through courses, projects, and community.'],
            ['On campus.<br><em>In Hualien.</em>','Get to know our campus<br>and the people in our department.'],
            ['Ideas into<br><em>practice.</em>','Student projects, café operations,<br>and learning with others.'],
        ]
        replace_contents(root.get_element_by_id('campus-title'),copies[0][0]);replace_contents(root.get_element_by_id('campus-description'),copies[0][1])
        data=LH.Element('script',{'type':'application/json','id':'campus-copy'});data.text=json.dumps(copies).replace('</','<'+chr(92)+'/');root.append(data)
        quick=select(root,'quick-card');labels=[('Admissions','Application information and contacts.','admissions'),('Courses','Course lists and curriculum maps.','curriculum'),('Faculty & staff','Teaching, research, and department support.','faculty'),('Internships','Forms and preparation resources.','internships'),('International learning','Exchange and overseas experiences.','exchange'),('Student projects','See what our students have worked on.','outcomes')]
        for card,(title,description,symbol) in zip(quick,labels):
            replace_contents(card.xpath('.//h2')[0],escape(title));replace_contents(card.xpath('.//p')[0],escape(description));set_first(card,'quick-symbol',svg(symbol))
            for small in card.xpath('.//small'):small.getparent().remove(small)
        select(root,'quick-top')[0].xpath('./span')[0].text='Useful links'
        memory=select(root,'hero-memory')[0];memory.xpath('.//b')[0].clear();memory.xpath('.//b')[0].text='The student café';memory.xpath('.//div/span')[0].text='Life at BMD'
        location=select(root,'campus-location')[0]
        for span in location.xpath('./span'):location.remove(span)
        set_first(root,'stories-heading','<div><div class="kicker">From the department</div><h2>News &amp; student achievements</h2></div>'+LH.tostring(select(root,'stories-heading-right')[0],encoding='unicode',method='html'))
        caption=select(root,'carousel-caption')[0];caption.xpath('./span')[0].text='Activities, announcements, and work by our students.'
        set_first(root,'carousel-count','More stories →')
        set_first(root,'life-text','<div class="kicker">Student life</div><h2>Projects, people,<br><em>and campus life.</em></h2><p>Students learn together through café operations, workshops, and cross-cultural activities. See what life in the department looks like.</p>'+LH.tostring(select(root,'life-routes')[0],encoding='unicode',method='html')+LH.tostring(select(root,'motion-toggle')[0],encoding='unicode',method='html'))
        for fig,caption_text in zip(select(root,'life-collage')[0].xpath('.//figcaption'),['International learning','Student design workshop']):fig.text=caption_text
        for el in select(root,'life-routes')[0].xpath('./a/span'):
            if el.text=='A wider world':el.text='International learning'
        directions=select(root,'pathways-heading')[0];directions.xpath('.//h2')[0].clear();replace_contents(directions.xpath('.//h2')[0],'Four learning directions');directions.xpath('.//p')[0].text='Explore the department’s teaching areas and find the courses listed for your entry year.';directions.xpath('.//*[contains(@class,"kicker")]')[0].text='Academics'
        for card,symbol in zip(select(root,'pathway-card'),['operations','smart','sustainable','culinary']):
            set_first(card,'pathway-symbol',svg(symbol));remove(card,'pathway-number')
        agenda=select(root,'agenda-heading')[0];replace_contents(agenda.xpath('.//h2')[0],'Academic calendar');agenda.xpath('.//*[contains(@class,"kicker")]')[0].text='2026–2027';replace_contents(agenda.xpath('.//p')[0],'Choose a date to see the listed events.<br>The full calendar is available below.')
        final=select(root,'home-final')[0];replace_contents(final.xpath('.//h2')[0],'Interested in BMD?');final.xpath('.//*[contains(@class,"kicker")]')[0].text='Admissions';replace_contents(final.xpath('.//p')[0],'Find application information and<br>ways to contact the department.')
        for anchor in root.xpath('.//a'):
            if anchor.text and anchor.text.strip()=='Explore your possibilities':anchor.text='Explore the program'
    elif key=='vision':
        for cls,title in [('purpose-vision','Our vision'),('purpose-mission','Our mission')]:
            card=select(root,cls)[0];replace_contents(card.xpath('./h2')[0],title);card.xpath('./p')[0].set('class','purpose-statement')
            remove(card,'purpose-top')
        for index in select(root,'purpose-values')[0].xpath('.//b'):
            parent=index.getparent();parent.text=(parent.text or '')+(index.tail or '');parent.remove(index)
    elif key=='history':
        select(root,'history-toolbar')[0].xpath('./span')[0].text='Select a year'
    elif key=='faculty':
        set_first(root,'directory-note','<span>Department office</span><p>Looking for a department contact?</p><a href="mailto:ss62@gms.tcu.edu.tw">ss62@gms.tcu.edu.tw</a><small>+886-3-857-2677 ext. 31682</small><a href="contact.html" class="directory-office-link">Contact details ↗</a>')
    elif key=='introduction':
        remove(root,'intro-photo-tag')
        for f in select(root,'feature'):remove(f,'num')
    elif key=='student-life':
        for caption,copy in zip(root.xpath('.//figcaption'),['Student café project','Design workshop','Student kayaking activity']):caption.text=copy
        labels=['View projects','International learning','Internship resources']
        for anchor,copy in zip(root.xpath('.//*[contains(@class,"feature-grid")]//a'),labels):
            anchor.text=copy+' '
        for f in select(root,'feature'):remove(f,'num')
    elif key=='academics':
        set_first(root,'academic-jump','Choose a learning direction <span>↓</span>')
        set_first(root,'program-visual','<img id="program-photo" src="assets/photos/cafe-project.webp" alt="Students from the department’s Indonesian cohort presenting a project"><span><b id="program-number">01</b> Learning in practice</span>')
        for panel in select(root,'learning-panel'):
            for kicker in select(panel,'kicker'):kicker.text='Learning directions'
    return ''.join(LH.tostring(child,encoding='unicode',method='html') for child in root)
