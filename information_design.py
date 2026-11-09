"""Practical reading aids and a more deliberate campus editorial hierarchy.

The certificate guide is derived from the retained publication, never from the
example table in the external evaluation. Published tables remain unchanged.
"""
from html import escape
import json
from lxml import html as LH


def select(root, cls):
    return root.xpath('.//*[contains(concat(" ",normalize-space(@class)," "),$c)]', c=' '+cls+' ')


def node(markup):
    return LH.fromstring(markup)


def replace_text(el, text):
    for child in list(el):
        el.remove(child)
    el.text = text


# Descriptive English translations, not official English credential titles.
# Groups follow the source's domestic table rows, including the two Class C rows.
DOMESTIC = [
    ('Skills test · Class B', ['Retail services', 'Chinese cooking', 'Western cooking', 'Baking', 'Chinese wheat-based food processing']),
    ('Skills test · Class C', ['International trade operations']),
    ('Skills test · Class C', ['Retail services', 'Chinese cooking', 'Western cooking', 'Baking', 'Chinese rice-based food processing', 'Chinese wheat-based food processing']),
    ('Professional', ['TIMS Marketing Analysis', 'TIMS Marketing Decision-Making', 'TIMS Marketing Strategy', 'PMA Project Assistant', 'iPAS Brand Planning', 'iPAS Net-Zero Carbon Planning and Management', 'iPAS Business Intelligence Analysis', 'Financial Planning Professional Competency (Taiwan Academy of Banking and Finance)', 'Financial Markets and Professional Ethics', 'Senior Securities Specialist', 'Real Estate Appraiser', 'Real Estate Broker', 'Land Administration Agent']),
    ('Advanced', ['TIMS Marketing Planning', 'TIMS Internet Marketing', 'TIMS Global Marketing', 'TIMS Tourism Marketing', 'Chain Store Operations Specialist', 'Chain Store Management Specialist', 'E-Business Planner (CRM, MKP, SCM)', 'E-Business Software Applications (CRM, ERP)', 'E-Business Data Analyst (DPA)', 'Internet of Things Applications and Technology (Professional)', 'Business Ethics Certification', 'Introductory Chain Store Operations and Management', 'TBSA Business Planning Competency', 'Meetings and Exhibitions Professional Certification', 'E-Commerce Analyst (ECA)', 'Multimedia Website Analyst (MWA)', 'Internet Marketing Analyst (IMA)', 'Customer Relationship Management Assistant Manager', 'Junior Foreign Exchange Personnel', 'Junior Credit Personnel']),
    ('Basic', ['E-Business Assistant Planner (EBC)', 'Modern Services S5: Innovation, Entrepreneurship and Technology Management', 'Integrated Online and Offline Marketing Management', 'Workplace Ethics Certification', 'Modern Services S6: Cultural and Creative Services Management', 'Finance-related credentials issued by the Taiwan Academy of Banking and Finance, Ministry of Examination, or Securities and Futures Institute', 'Real Estate Salesperson', 'Click up Certification']),
]
INTERNATIONAL = [
    'Microsoft Office Specialist (MOS)', 'Google Ads', 'Adobe ACA', 'Adobe ACP',
    'WBSA Business Planning Professional Certification', 'Google Analytics',
    'Marketing Management (City & Guilds, London)',
    'Customer Relationship Management (City & Guilds, London)',
    'Sustainability and Carbon Management Analyst (TÜV Rheinland Taiwan)',
]


def certificate_records(content):
    pages=json.loads((content/'official-en/pages.json').read_text(encoding='utf-8'))
    source=next(p for p in pages if p.get('key')=='c32918c65d8f')
    records=[]
    for row,(level,names) in zip(source['tables'][0][1:],DOMESTIC,strict=True):
        original=[v.strip() for v in row[-2].split('\n') if v.strip()]
        if len(original)!=len(names):
            raise ValueError('Certificate source group changed; review English reading aid')
        for zh,en in zip(original,names,strict=True):
            records.append(dict(en=en,zh=zh,level=level,points=int(row[-1].replace('點','')),scope='Domestic'))
    for row,en in zip(source['tables'][1][1:],INTERNATIONAL,strict=True):
        records.append(dict(en=en,zh=row[1],level={'基礎':'Basic','專業':'Professional'}[row[0]],points=int(row[2].replace('點','')),scope='International'))
    return records


def certificate_guide(root, content):
    hero=select(root,'page-hero')[0]
    replace_text(hero.xpath('.//h1')[0],'Certificate requirements')
    section=select(root,'split')[0]
    section.set('class','wrap section certificate-overview')
    lead=select(section,'lead')[0]
    for kicker in select(lead,'kicker'):
        kicker.getparent().remove(kicker)
    for h in lead.xpath('./h2'):
        replace_text(h,'Plan your next certificate.')
    lead.append(node('<p class="review-meta">Published rule revised 25 September 2025</p>'))
    original=section.xpath('./div')[1]
    details=node('<details class="certificate-original" id="original-certificate-tables"><summary>Original point tables · Traditional Chinese</summary><div class="certificate-original-body" lang="zh-Hant"></div></details>')
    target=details.xpath('./div')[0]
    for child in list(original):
        target.append(child)
    section.remove(original)
    example=node('''<aside class="certificate-example" aria-labelledby="certificate-example-title"><span class="review-eyebrow">A planning example</span><h2 id="certificate-example-title">20 + 10 = 30</h2><p>Google Ads + Microsoft Office Specialist (MOS)</p><small>Points shown in the published table. Confirm recognition and the rules for your cohort with the department before registering for an exam.</small><a class="text-link" href="contact.html">Ask about your certificate</a></aside>''')
    section.append(example)
    records=certificate_records(content)
    rows=''
    for r in records:
        rows+=f'''<tr data-filter-item data-category="{r['points']}" data-certificate-en="{escape(r['en'])}"><td><b>{escape(r['en'])}</b><small lang="zh-Hant">{escape(r['zh'])}</small></td><td><span>{r['scope']}</span><small>{r['level']}</small></td><td><b>{r['points']}</b></td></tr>'''
    guide=node('''<section class="wrap section certificate-guide" aria-labelledby="certificate-guide-title" data-filter-scope><div class="review-section-heading"><div><span class="review-eyebrow">Find a certificate</span><h2 id="certificate-guide-title">Compare the points.</h2></div><a class="text-link" href="#original-certificate-tables">Read the original tables</a></div><p class="certificate-reading-note">English reading aid for the published domestic and international lists. English names are descriptive translations; the original Chinese tables and department confirmation remain the reference.</p><div class="certificate-tools"><div><label for="certificate-search">Search certificate names</label><input class="filter-input" id="certificate-search" type="search" data-filter-input placeholder="Try Google, TIMS, MOS, or a Chinese name"></div><div class="filters" aria-label="Filter certificates by points"><button class="filter active" data-filter="all" aria-pressed="true">All points</button><button class="filter" data-filter="10" aria-pressed="false">10</button><button class="filter" data-filter="15" aria-pressed="false">15</button><button class="filter" data-filter="20" aria-pressed="false">20</button></div></div><div class="certificate-table-scroll" role="region" aria-label="Certificate point comparison" tabindex="0"><table class="certificate-table"><thead><tr><th scope="col">Certificate</th><th scope="col">List / level</th><th scope="col">Points</th></tr></thead><tbody>'''+rows+'''</tbody></table></div><p class="empty" hidden>No matching certificates. Try another name or point value.</p></section>''')
    section.addnext(guide)
    for row in guide.xpath('.//tr[@data-certificate-en]'):
        alias=row.xpath('./td[1]/small')[0]
        if alias.text==row.get('data-certificate-en'):
            alias.set('hidden','')
    counter=node('<p class="certificate-result-count" aria-live="polite" hidden></p>')
    select(guide,'certificate-tools')[0].addnext(counter)
    archive=node('<section class="wrap section certificate-source-section" aria-label="Published reference"></section>')
    archive.append(details)
    guide.addnext(archive)


def admissions_guide(root):
    section=node('''<section class="wrap section international-guide" id="international-applicants" aria-labelledby="international-guide-title"><div class="international-guide-intro"><span class="review-eyebrow">Coming to Hualien</span><h2 id="international-guide-title">Applying from outside Taiwan?</h2><p>Start with the university’s international admissions guidance, then ask BMD about the programme and language of instruction.</p><a class="button" href="https://oga.tcu.edu.tw/international-student/" target="_blank" rel="noopener">International admissions</a><a class="text-link" href="contact.html">Talk to the department</a></div><ol class="international-steps"><li><span aria-hidden="true">01</span><div><h3>Find your application route</h3><p>Check eligibility, documents, language requirements, and the schedule for your intake.</p><a href="https://oga.tcu.edu.tw/international-student/" target="_blank" rel="noopener">Application guidance</a></div></li><li><span aria-hidden="true">02</span><div><h3>Plan for fees and support</h3><p>Read the university’s scholarship criteria, tuition information, and living-cost guidance.</p><a href="https://oga.tcu.edu.tw/scholarship/" target="_blank" rel="noopener">Scholarships &amp; tuition</a></div></li><li><span aria-hidden="true">03</span><div><h3>Get to know life here</h3><p>Explore language learning and the international student handbook for practical campus information.</p><div class="international-step-links"><a href="https://language.tcu.edu.tw/" target="_blank" rel="noopener">Chinese Language Center</a><a href="https://oga.tcu.edu.tw/" target="_blank" rel="noopener">Global Affairs &amp; student handbook</a><a href="student-life.html">Life at BMD</a></div></div></li></ol></section>''')
    hero=select(root,'page-hero')[0]
    hero.addnext(section)
    hero.xpath('./div')[0].append(node('<nav class="admissions-audience" aria-label="Find admissions information"><a href="#international-applicants">International applicants</a><a href="#department-resources">Department resources</a></nav>'))
    for resource in select(root,'resource-list')[:1]:
        resource.set('id','department-resources')


def refine_information(path, body, content):
    if path not in {'index.html','requirements.html','admissions.html','academics.html','news.html'}:
        return body
    root=LH.fragment_fromstring(body,create_parent='div')
    if path=='index.html':
        # Keep the cinematic opening, but explain what the visitor is looking at.
        for p in root.xpath('.//*[@id="campus-description"]'):
            replace_text(p,'Business Management in Hualien, Taiwan. Learn through projects, teamwork, and service.')
        for i,card in enumerate(select(root,'quick-card')):
            titles=['Admissions','Curriculum','Faculty & staff','Beyond Campus']
            captions=['Application routes & contacts','Courses for your entry year','People & areas of expertise','Placements & international learning']
            replace_text(card.xpath('.//h2')[0],titles[i])
            card.append(node('<p class="quick-description">'+captions[i]+'</p>'))
        for heading in select(root,'stories-heading'):
            title=heading.xpath('.//h2')[0]
            replace_text(title,'From the department')
            title.addprevious(node('<span class="review-eyebrow">BMD bulletin</span>'))
        for heading in select(root,'pathways-heading'):
            title=heading.xpath('.//h2')[0]
            title.addprevious(node('<span class="review-eyebrow">Four ways into business</span>'))
        for heading in select(root,'home-final'):
            heading.xpath('./div')[0].append(node('<p>Get to know the courses, the people, and daily life in Hualien.</p>'))
            heading.xpath('./div')[1].append(node('<a class="text-link" href="admissions.html#international-applicants">Applying from outside Taiwan?</a>'))
    elif path=='requirements.html':
        certificate_guide(root,content)
    elif path=='admissions.html':
        admissions_guide(root)
    elif path=='academics.html':
        for note in select(root,'source-note')[:1]:
            note.addprevious(node('<p class="learning-terminology">Learning-direction labels are short introductions. Refer to your entry-year curriculum for the official module and course names.</p>'))
    if path in {'index.html','news.html'}:
        records=json.loads((content/'official-zh/latest-news.json').read_text(encoding='utf-8'))['items']
        import hashlib
        dates={'news-'+hashlib.sha1(r['url'].encode()).hexdigest()[:12]+'.html':r.get('publication_date') for r in records}
        for card in select(root,'story-slide')+select(root,'news-card'):
            links=card.xpath('.//a[@href]')
            stamp=dates.get(links[0].get('href')) if links else None
            if stamp:
                card.append(node('<time class="news-date" datetime="'+escape(stamp)+'">'+escape(stamp)+'</time>'))
        # Never mistake the date printed on an event poster for its publication date.
        if path=='news.html':
            hero=select(root,'page-hero')[0]
            hero.append(node('<p class="review-meta">Publication dates appear when provided by the source. Event dates remain in the original notices.</p>'))
    return ''.join(LH.tostring(c,encoding='unicode',method='html') for c in root)
