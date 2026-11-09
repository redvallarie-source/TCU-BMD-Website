"""Page-specific presentation for the retained, source-backed interior content."""
from lxml import html as LH
from html import escape
import re

def classes(el,extra):el.set('class',(el.get('class','')+' '+extra).strip())
def select(root,cls):return root.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," '+cls+' ")]')
def node(markup):return LH.fromstring(markup)
def cards(titles):
    return '<div class="interior-next">'+''.join('<a href="'+u+'"><span>'+label+'</span><b>'+title+'</b><i aria-hidden="true">↗</i></a>' for u,label,title in titles)+'</div>'
def page_class(path):
    key=path.removesuffix('.html')
    if key.startswith('faculty-'):key='profile'
    elif key.startswith('source-'):key='reading'
    elif key.startswith('news-'):key='article'
    return 'interior-page page-'+key

def redesign(path,body):
    root=LH.fragment_fromstring(body,create_parent='div')
    hero=next(iter(select(root,'page-hero')),None)
    if hero is not None:
        pics=hero.xpath('./img')
        if pics:
            pic=pics[0];frame=LH.Element('div',{'class':'interior-photo'});hero.replace(pic,frame);frame.append(pic)
            frame.append(node('<span class="photo-corner" aria-hidden="true">BMD · A WIDER PERSPECTIVE <b>↗</b></span>'))
        if path in ['introduction.html','vision.html','history.html']:
            for old in select(root,'page-tabs'):old.getparent().remove(old)
            nav=node('<nav class="wrap section-switcher" aria-label="About the department">'+''.join('<a href="'+p+'"'+(' aria-current="page"' if p==path else '')+'>'+label+'</a>' for p,label in [('introduction.html','Introduction'),('vision.html','Vision & Mission'),('history.html','Our history')])+'</nav>')
            hero.addnext(nav)
    if path=='introduction.html':
        classes(hero,'intro-cover')
        hero.xpath('.//h1')[0].text='Business learning.'
        hero.xpath('.//h1')[0].append(node('<span>Human connection.</span>'))
        frame=select(root,'interior-photo')[0]
        frame.append(node('<div class="intro-photo-tag"><span>THIS IS BMD</span><b>A place to find<br>your possibilities.</b></div>'))
        for s in select(root,'split'):classes(s,'intro-story')
        for i,f in enumerate(select(root,'feature')):
            classes(f,'value-card value-'+str(i));f.insert(0,node('<span class="value-symbol" aria-hidden="true">'+['✳','◎','↗'][i]+'</span>'))
        root.append(node('<div class="wrap">'+cards([('vision.html','OUR PURPOSE','What guides us'),('history.html','OUR JOURNEY','How we got here')])+'</div>'))
    elif path=='vision.html':
        old=select(root,'vision-layout')[0]
        spread=node('''<div class="purpose-spread"><section class="purpose-vision"><div class="purpose-top"><span>01 / VISION</span><i aria-hidden="true">↗</i></div><h2>A better future.<br>A broader<br><em>perspective.</em></h2><p>Advance innovative, globally connected, and socially responsible business education.</p><svg class="purpose-orbit" viewBox="0 0 250 250" aria-hidden="true"><circle cx="125" cy="125" r="100"/><ellipse cx="125" cy="125" rx="55" ry="100" transform="rotate(40 125 125)"/><ellipse cx="125" cy="125" rx="55" ry="100" transform="rotate(-40 125 125)"/><circle cx="125" cy="125" r="25"/></svg></section><section class="purpose-mission"><div class="purpose-top"><span>02 / MISSION</span><i aria-hidden="true">✳</i></div><h2>Professional minds.<br><em>Compassionate hearts.</em></h2><p>Develop skilled business professionals with creativity, teamwork, cross-cultural understanding, and strong ethical values.</p><div class="purpose-values"><span><b>01</b> Creativity</span><span><b>02</b> Teamwork</span><span><b>03</b> Cultural understanding</span><span><b>04</b> Ethical values</span></div><div class="purpose-foot">KNOWLEDGE WITH PURPOSE. LEADERSHIP WITH HEART.</div></section></div>''')
        old.getparent().replace(old,spread)
    elif path=='history.html':
        console=select(root,'archive-layout')[0];classes(console,'history-console')
        console.insert(0,node('<div class="history-toolbar"><span>EXPLORE THE CHAPTERS</span><div><span id="history-position" aria-live="polite">01 / 05</span><button class="history-previous" aria-label="Previous history milestone" disabled>←</button><button class="history-next" aria-label="Next history milestone">→</button></div></div>'))
        panel=select(root,'history-sheet')[0];classes(panel,'history-stage');classes(panel[0],'history-narrative')
        for art in panel.xpath('./svg'):panel.remove(art)
        artwork=[
            '<rect x="75" y="42" width="140" height="176" rx="12"/><path d="M96 42v176m22-132h74m-74 24h74m-74 24h74m-74 24h74m-74 24h74m-48-72v96"/>',
            '<rect x="40" y="50" width="220" height="140" rx="12"/><path d="M45 166h210M150 192v35m-53 0h106m-81-117 21-21m-21 21 21 21m35-42 21 21-21 21"/><circle cx="150" cy="178" r="2"/>',
            '<path d="M58 102h184l-13 108H71L58 102Zm28 0 28-55m100 55-28-55M96 123v60m35-60v60m35-60v60m35-60v60"/><circle cx="235" cy="55" r="23"/><path d="m225 55 7 7 13-14"/>',
            '<circle cx="150" cy="128" r="79"/><ellipse cx="150" cy="128" rx="37" ry="79"/><path d="M73 128h154m-144-38h128m-128 76h128m-70 41v25m-39 0h78"/><path d="m220 39 24 0v24m0-24-45 45"/>',
            '<path d="M41 211h218M59 207V91l91-51 91 51v116M98 205V117h104v88M138 205v-44h26v44M74 102h152M121 126h10m38 0h10m-58 20h10m38 0h10"/><path d="M123 70h54m-27-15v29"/>',
        ]
        visual='<div class="history-visual"><span class="history-art-label">THE STORY KEEPS GROWING</span>'
        for i,art in enumerate(artwork):visual+='<svg viewBox="0 0 300 260" data-history-illustration="'+str(i)+'"'+(' hidden' if i else '')+' aria-hidden="true"><ellipse class="art-shadow" cx="150" cy="226" rx="113" ry="14"/><g>'+art+'</g></svg>'
        visual+='<span class="history-art-note">Rooted in knowledge.<br>Open to possibility.</span></div>'
        panel.append(node(visual))
    elif path=='academics.html':
        for layout in select(root,'learning-layout'):classes(layout,'program-explorer')
        panel=select(root,'learning-panel')[0];panel.insert(0,node('<div class="program-visual"><img id="program-photo" src="assets/photos/cafe-project.webp" alt="Students from the department’s Indonesian cohort presenting a project"><span><b id="program-number">01</b> LEARN IT. PUT IT INTO PRACTICE.</span></div>'))
        hero.append(node('<a class="academic-jump" href="#learning-panel">EXPLORE FOUR DIRECTIONS <span>↓</span></a>'))
    elif path=='curriculum.html':
        scope=root.xpath('.//*[@data-filter-scope]')[0];classes(scope,'cohort-finder')
        cohorts=scope.xpath('./section[@data-filter-item]')
        years=[s.get('data-category') for s in cohorts]
        hero.append(node('<div class="cohort-ticket"><span>FIND YOUR CURRICULUM</span><b>'+max(years)+'</b><small>LATEST LISTED ENTRY YEAR</small><div>Course list <i>↗</i><br>Curriculum map <i>↗</i></div></div>'))
        for i,s in enumerate(cohorts):
            head=select(s,'section-head')[0];title=head.xpath('.//h2')[0].text_content();links=head.xpath('.//a');count=len(select(s,'resource-link'))
            details=LH.Element('details',{'class':'cohort-card','data-filter-item':'','data-category':s.get('data-category')})
            if not i:details.set('open','')
            summary=node('<summary><span class="cohort-year">'+s.get('data-category')+'</span><span><b>'+escape(title)+'</b><small>'+str(int(s.get('data-category'))+1911)+' entry · '+str(count)+' original documents</small></span><i aria-hidden="true">+</i></summary>')
            details.append(summary);content=LH.Element('div',{'class':'cohort-body'})
            for child in list(s):
                if child is not head:content.append(child)
            for link in links:content.append(link)
            details.append(content);scope.replace(s,details)
    elif path=='faculty.html':
        classes(hero,'directory-cover');h1=hero.xpath('.//h1')[0];h1.clear();h1.text='Our people.';h1.append(node('<span>Your possibilities.</span>'))
        total=len(select(root,'person'))
        hero.append(node('<aside class="directory-note"><span>THE BMD COMMUNITY</span><b>'+str(total)+'<i>people</i></b><p>Teaching. Research. Support.<br>Get to know the people behind BMD.</p><a href="contact.html">Department contacts ↗</a><svg viewBox="0 0 220 160" aria-hidden="true"><circle cx="65" cy="65" r="30"/><circle cx="155" cy="65" r="30"/><path d="M20 145c0-43 90-43 90 0m0 0c0-43 90-43 90 0"/></svg></aside>'))
        scope=root.xpath('.//*[@data-filter-scope]')[0];scope.insert(1,node('<p class="directory-count" aria-live="polite"><b id="people-visible">'+str(total)+'</b> people to discover</p>'))
        for person in select(root,'person'):
            image=select(person,'person-image')[0];image.append(node('<span class="portrait-arrow" aria-hidden="true">↗</span>'))
    elif path.startswith('faculty-'):
        for profile in select(root,'profile'):classes(profile,'profile-sheet')
    elif path=='student-life.html':
        classes(hero,'life-cover')
        for grid in select(root,'campus-grid'):
            classes(grid,'life-gallery')
            for i,figure in enumerate(grid.xpath('./figure')):
                image=figure.xpath('./img')[0];button=LH.Element('button',{'class':'gallery-open','data-gallery-open':str(i),'aria-label':'View photo: '+image.get('alt','Student life')});figure.replace(image,button);button.append(image);button.append(node('<span aria-hidden="true">↗</span>'))
        root.append(node('<dialog class="photo-dialog" id="photo-dialog" aria-labelledby="photo-caption"><button class="photo-close icon-btn" aria-label="Close photo">×</button><img id="photo-full" src="assets/photos/cafe-project.webp" alt=""><div class="photo-dialog-footer"><button class="photo-previous" aria-label="Previous photo">←</button><p id="photo-caption"></p><button class="photo-next" aria-label="Next photo">→</button></div></dialog>'))
    elif path in ['resources.html','regulations.html','internships.html']:
        scope=root.xpath('.//*[@data-filter-scope]')[0];scope.set('data-resource-paginate','')
        scope.append(node('<div class="resource-pagination"><span class="resource-count" aria-live="polite"></span><button class="button outline resource-more" type="button">Show more documents <span>↓</span></button></div>'))
        if path=='resources.html':hero.append(node('<div class="resource-shortcuts"><a href="curriculum.html"><span>01</span> Curriculum <i>↗</i></a><a href="internships.html"><span>02</span> Internship forms <i>↗</i></a><a href="regulations.html"><span>03</span> Regulations <i>↗</i></a></div>'))
    elif path=='requirements.html':
        lead=select(root,'lead')[0];lead.insert(0,node('<div class="certificate-target"><span>THE PUBLISHED THRESHOLD</span><b>30<small>certificate points</small></b><i aria-hidden="true">✳</i></div>'))
    elif path=='news.html':
        classes(hero,'newsroom-cover');grid=select(root,'news-grid')[0]
        if len(grid):classes(grid[0],'lead-story')
    elif path=='admissions.html':
        classes(hero,'admissions-cover')
    elif path in ['exchange.html','outcomes.html','international.html']:
        classes(hero,'experience-cover')
    elif path=='events.html':
        hero.append(node('<a class="calendar-pass" href="assets/academic-calendar-2026-2027.pdf" target="_blank" rel="noopener"><span>THE ACADEMIC YEAR</span><b>2026 <i>—</i> 2027</b><small>Download the full calendar ↗</small></a>'))
    for resource in select(root,'resource-link'):
        labels=resource.xpath('./div/b')
        if labels and re.fullmatch(r'\d+\.(?:pdf|docx?|xlsx?|pptx?)',labels[0].text_content().strip(),re.I):
            filename=labels[0].text_content().strip();labels[0].text='Curriculum document' if path=='curriculum.html' else 'Original department document'
            labels[0].addnext(node('<small class="resource-filename">'+escape(filename)+'</small>'))
    return ''.join(LH.tostring(c,encoding='unicode',method='html') for c in root)
