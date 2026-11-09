"""A denser, photo-led refinement of the existing campus design."""
from lxml import html as LH
from lxml.etree import SubElement
from homepage import ambient


def select(root, cls):
    return root.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," '+cls+' ")]')


def node(markup):
    return LH.fromstring(markup)


def campus_edge():
    # An abstract campus edge, not a diagram of a particular university building.
    return '''<div class="campus-edge" aria-hidden="true"><svg viewBox="0 0 1200 180" preserveAspectRatio="xMidYMax slice" focusable="false"><path class="edge-land" d="M0 165 95 110 177 148 298 57 393 130 475 86 580 141 689 57 792 136 911 92 1034 147 1132 100 1200 131V180H0Z"/><g class="edge-buildings"><path d="M46 180v-52h65v52m20 0V99h77v81m31 0v-69h85v69m31 0V75h67v105m18 0v-64h122v64m31 0V92h83v88m29 0v-58h77v58m28 0V66h84v114m23 0v-76h98v76m31 0V91h71v89m25 0v-54h83v54"/><path d="M53 145h51m-51 15h51m37-43h56m-56 17h56m-56 17h56m51-22h68m-68 18h68m48-52h48m-48 18h48m-48 18h48m47 4h102m-102 18h102m49-42h64m-64 18h64m-64 18h64m48-7h59m-59 19h59m49-77h65m-65 18h65m-65 18h65m-65 18h65m44-23h79m-79 18h79m50-33h51m-51 19h51m-51 19h51m44-9h65"/></g><path class="edge-ground" d="M0 179h1200"/></svg></div>'''


def video_section():
    return '''<section class="campus-film-section" aria-labelledby="film-heading"><div class="wrap film-heading"><div><div class="kicker">Hualien, Taiwan</div><h2 id="film-heading">A closer look at Tzu Chi.</h2></div><p>Campus life, in motion.<br><span>TCU Office of Global Affairs</span></p></div><div class="campus-video" data-campus-video><button type="button" class="film-poster" data-film-play aria-label="Play Why Should You Study at Tzu Chi University in Taiwan?"><img src="assets/photos/campus-film-poster.webp" width="1280" height="720" alt="Preview of the Tzu Chi University film" loading="lazy" decoding="async"><span class="film-play-label"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 11 7-11 7Z"/></svg><span>Play film</span></span></button></div><div class="wrap film-credit"><span>Why Should You Study at Tzu Chi University in Taiwan?</span><a href="https://www.youtube.com/watch?v=8ODH3C1lykA" target="_blank" rel="noopener">Watch on YouTube</a></div></section>'''


def ambient_control():
    return node('<button type="button" class="ambient-control" aria-pressed="false" aria-label="Pause background motion">Pause background motion</button>')


def refine_campus(path, body):
    root = LH.fragment_fromstring(body, create_parent='div')
    if path == 'index.html':
        agenda = select(root, 'home-agenda')[0]
        agenda.addprevious(node(video_section()))
        final = select(root, 'home-final-shell')[0]
        final.insert(0, node(campus_edge()))
        final.append(ambient_control())
        life=select(root,'editorial-motion')[0]
        life.insert(0,node(ambient('breeze')))
        # The existing final text included an orphaned sentence fragment.
        for p in final.xpath('.//p'):
            if 'ways to contact the department.' in ''.join(p.itertext()):
                for child in list(p):p.remove(child)
                p.text='Application information and department contacts.'
    if path == 'careers.html':
        hero = select(root, 'page-hero')[0]
        hero.set('class', hero.get('class')+' with-photo career-cover')
        hero.append(node('''<figure class="career-photo photo-zoom"><div class="photo-crop"><img src="assets/photos/career-collaboration.webp" alt="Colleagues discussing work around a shared desk" width="1400" height="933" loading="lazy" decoding="async"></div><figcaption>Workplace collaboration · Illustrative photo<br><a href="https://unsplash.com/photos/QckxruozjRg" target="_blank" rel="noopener">Annie Spratt / Unsplash</a></figcaption></figure>'''))
        lead=select(root,'lead')[0]
        lead.append(node('''<figure class="career-detail photo-zoom"><div class="photo-crop"><img src="assets/photos/career-hospitality.webp" alt="A chef at work in a restaurant kitchen" width="1200" height="800" loading="lazy" decoding="async"></div><figcaption>Hospitality & service · Illustrative photo<br><a href="https://unsplash.com/photos/chef-working-in-a-busy-restaurant-kitchen-ilTlHqGFNQc" target="_blank" rel="noopener">Flavio Mori / Unsplash</a></figcaption></figure>'''))
        # These source cells describe independent examples, rather than tabular data.
        # Preserve each example in a compact, open list beside the photograph.
        table=root.xpath('.//table')[0]
        roles=LH.Element('div',{'class':'career-roles'})
        for cell in table.xpath('.//td'):
            lines=[line.strip() for line in cell.text_content().splitlines() if line.strip()]
            if not lines:continue
            article=SubElement(roles,'article');heading=SubElement(article,'h3');heading.text=lines[0].replace('Accouting','Accounting')
            if len(lines)>1:
                paragraph=SubElement(article,'p');paragraph.text=' · '.join(lines[1:])
        table.getparent().getparent().replace(table.getparent(),roles)
    if path in {'introduction.html','admissions.html','careers.html','international.html'}:
        heroes=select(root,'page-hero')
        if heroes:
            heroes[0].set('class',heroes[0].get('class')+' campus-illustrated')
            heroes[0].append(node(campus_edge()))
            heroes[0].append(ambient_control())
    # Apply the same green breeze to existing content, without adding more copy.
    band_targets={'introduction.html':'intro-story','admissions.html':'faq'}
    if path in band_targets:
        targets=select(root,band_targets[path])
        if targets:
            target=targets[0];parent=target.getparent();index=parent.index(target)
            band=node('<div class="campus-breeze-band motion-region" data-ambient-surface></div>')
            parent.remove(target);parent.insert(index,band)
            band.append(node(ambient('breeze')));band.append(target);band.append(ambient_control())
    if path == 'content-review.html':
        for p in root.xpath('.//p'):
            if 'One legacy notice containing account-access instructions' in ''.join(p.itertext()):
                p.getparent().remove(p)
    # Photograph surfaces get the same small hover movement across the site.
    for cls in ['interior-photo','project-photo']:
        for el in select(root,cls):
            el.set('class',el.get('class')+' photo-zoom')
    return ''.join(LH.tostring(child,encoding='unicode',method='html') for child in root)
