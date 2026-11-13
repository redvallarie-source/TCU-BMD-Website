"""A concise, image-led edition of the existing BMD pages."""
from pathlib import Path
from html import escape as esc
import json
from lxml import html as LH
from PIL import Image


def select(root,cls):
    return root.xpath('.//*[contains(concat(" ",normalize-space(@class)," "),$value)]',value=' '+cls+' ')


def node(markup):return LH.fromstring(markup)


def contents(el,text):
    for child in list(el):el.remove(child)
    el.text=text


def drop(el):
    if el.getparent() is not None:el.getparent().remove(el)


def compact(path,body,content):
    root=LH.fragment_fromstring(body,create_parent='div')
    data=json.loads((content/'compact-editorial.json').read_text())
    campus=json.loads((content/'japan-photo-selection.json').read_text(encoding='utf-8'))['additional_campus_photos']
    page=path.removesuffix('.html')
    stories=[]
    originals=path.startswith(('source-','faculty-','news-'))
    if not originals:
        for crumb in select(root,'crumbs'):drop(crumb)
        for hero in select(root,'page-hero'):
            leads=hero.xpath('./div[1]/p')
            for p in leads:
                if page in data['leads'] and data['leads'][page]:contents(p,data['leads'][page])
                else:drop(p)
    # Shorten only curated interface copy. Published source bodies stay intact.
    for el in root.xpath('.//p|.//h1|.//h2|.//h3'):
        if el.xpath('ancestor::*[contains(concat(" ",@class," ")," source-body ")]'):continue
        value=' '.join(el.text_content().split())
        if value in data['replacements']:contents(el,data['replacements'][value])
    def rewrite(value):
        if isinstance(value,str):return data['replacements'].get(' '.join(value.split()),value)
        if isinstance(value,list):return [rewrite(v) for v in value]
        if isinstance(value,dict):return {k:rewrite(v) for k,v in value.items()}
        return value
    for script in root.xpath('.//script[@type="application/json"][@id="life-project-data"]'):
        script.text=json.dumps(rewrite(json.loads(script.text)),ensure_ascii=False).replace('</','<\\/')

    photo_records={p['relative_file']:p for p in json.loads((content.parent/'dist/assets/photos/source-manifest.json').read_text())}
    def picture(src,caption=None,alt=None):
        record=photo_records.get(src,{})
        dimensions=Image.open(content.parent/'dist'/src).size
        p={'src':src,'alt':alt or record.get('caption') or caption or 'Department photograph','caption':caption or record.get('caption') or 'Department photo archive','width':dimensions[0],'height':dimensions[1]}
        p.update(data.get('photo_credits',{}).get(src,{}))
        return p
    def owner_cover(slot):
        p=campus[slot]
        frame=select(root,'interior-photo')[0]
        image=frame.xpath('./img')[0]
        image.set('src',p['path']);image.set('alt',p['alt'])
        image.set('width',str(p['width']));image.set('height',str(p['height']))
        for caption in select(frame,'editorial-caption'):contents(caption,p['caption'])
    def tile(story,href,cls=''):
        p=story['images'][0]
        credit='<span class="edition-illustrative">Illustrative photo</span>' if p.get('credit') else ''
        return f'''<a class="edition-tile {cls}" href="{esc(href)}" data-story-open="{story['id']}" aria-label="View details: {esc(story['title'])}"><span class="edition-tile-media"><img src="{p['src']}" alt="{esc(p['alt'])}" width="{p['width']}" height="{p['height']}" loading="lazy" decoding="async">{credit}<span class="edition-tile-wash"><span>View details</span></span></span><span class="edition-tile-label">{esc(story.get('label',''))}</span><h3>{esc(story['title'])}</h3></a>'''

    if page=='index':
        descriptions=root.xpath('.//*[@id="campus-description"]')
        if descriptions:contents(descriptions[0],'Hualien, Taiwan')
        quick=select(root,'quick-card')
        for card in quick[:4]:
            for p in card.xpath('.//p'):drop(p)
        for card in quick[4:]:drop(card)
        if len(quick)>3:contents(quick[3].xpath('.//h2')[0],'Beyond Campus')
        for cls in ['quick-top','carousel-caption']:
            for el in select(root,cls):drop(el)
        for el in select(root,'quick-launch'):el.attrib.pop('data-carousel',None)
        for el in select(root,'quick-track'):el.set('aria-label','Department quick links')
        for cls in ['life-text','pathways-heading','agenda-heading','film-heading','home-final']:
            for el in select(root,cls):
                for p in el.xpath('./p|./div/p'):drop(p)
        for el in select(root,'life-routes'):
            links=el.xpath('./a')
            if len(links)>2:drop(links[1])
        heading=select(root,'pathways-heading')[0].xpath('.//h2')[0];contents(heading,'Fields of study')
        old=select(root,'pathways-grid')[0]
        for child in list(old):old.remove(child)
        for i,s in enumerate(data['learning_stories']):
            story=dict(s);story['images']=[picture(**p) for p in s['images']]
            stories.append(story);old.append(node(tile(story,f'academics.html#learning-tab-{i}','pathway-card edition-learning')))
        for el in select(root,'stories-heading'):
            for h in el.xpath('.//h2'):contents(h,'News')
        for p in root.xpath('.//*[contains(concat(" ",@class," ")," story-slide ")]/p'):drop(p)
        for el in select(root,'calendar'):
            for p in el.xpath('./p'):
                if not p.xpath('.//a'):drop(p)
        for el in select(root,'home-final'):
            for k in select(el,'kicker'):drop(k)

    if page=='introduction':
        owner_cover('intro-group')
        for el in select(root,'kicker'):drop(el)
        prose=select(root,'intro-story')[0]
        for p in prose.xpath('.//p')[1:]:drop(p)
        if prose.xpath('.//p'):contents(prose.xpath('.//p')[0],data['intro_body'])
        grids=select(root,'editorial-principles')
        if grids:
            grid=grids[0];grid.set('class','edition-intro-grid')
            for child in list(grid):grid.remove(child)
            for s in data['intro_stories']:
                story=dict(s);story['images']=[picture(**p) for p in s['images']]
                stories.append(story);grid.append(node(tile(story,story['links'][0]['href'])))

    if page=='student-life':
        for el in select(root,'life-learning'):
            for p in el.xpath('./div/p'):drop(p)
            for k in select(el,'kicker'):drop(k)
        for el in select(root,'life-project-section'):
            for k in select(el,'kicker'):drop(k)
        for el in select(root,'life-abroad-copy'):
            for p in el.xpath('./p'):drop(p)
        examples=select(root,'life-volunteer-examples')
        for el in examples:
            details=LH.Element('details',{'class':'edition-volunteer-details'})
            summary=LH.Element('summary');summary.text='Volunteer roles';details.append(summary)
            for child in list(el):
                if child.tag!='h3':details.append(child)
            el.getparent().replace(el,details)

    if page=='internships':
        for el in select(root,'beyond-cover'):
            for p in el.xpath('./div/p'):drop(p)
        for el in select(root,'beyond-cover-note'):drop(el)
        for el in select(root,'beyond-programmes'):
            for p in el.xpath('./div[contains(@class,"intern-section-head")]/p'):drop(p)
        programme_data=json.loads((content/'global-learning.json').read_text())
        card_info=data['programme_images']
        listing=select(root,'beyond-programme-list')[0]
        listing.set('class','beyond-programme-list edition-programme-grid')
        for child in list(listing):listing.remove(child)
        for p in programme_data['programmes']:
            ident=p['id'];meta=card_info[ident]
            pics=[picture(**v) for v in meta['images']]
            story={'id':'programme-'+ident,'label':p['place']+' · '+p['kind'],'title':p['title'],'body':p['body'],'images':pics,'links':[{'href':v['url'],'label':v['label']} for v in p['links']]}
            stories.append(story)
            source=next(v for v in p['links'] if v['url'].startswith('https://'))
            article=node(f'''<article class="beyond-programme edition-programme-card" data-programme="{ident}" data-filter-item data-category="{p['type']}">{tile(story,source['url'])}<div class="edition-card-foot"><span>{esc(meta['status'])}</span><a href="{esc(source['url'])}" target="_blank" rel="noopener">Official source</a></div></article>''')
            listing.append(article)
        preparation=select(root,'intern-preparation')[0]
        resources=select(preparation,'intern-resources')[0]
        summary=resources.xpath('./summary')[0]
        count=len(resources.xpath('.//a[@data-filter-item]'))
        for child in list(summary):summary.remove(child)
        summary.append(node('<h2>Internship forms</h2>'));summary.append(node(f'<span class="edition-file-count">{count} files</span>'));summary.append(node('<i aria-hidden="true">+</i>'))
        for child in list(preparation):preparation.remove(child)
        wrapper=LH.Element('div',{'class':'wrap edition-form-shelf'});wrapper.append(resources)
        wrapper.append(node('<div class="edition-form-links"><a href="https://mdm.tcu.edu.tw/p/412-1021-5007.php?Lang=zh-tw" target="_blank" rel="noopener">Official internship resources</a><a href="contact.html">Contact the department</a></div>'))
        preparation.append(wrapper)
        for el in select(root,'intern-takeaway'):drop(el)
        for el in select(root,'intern-notebook-photo'):
            for p in el.xpath('./p'):drop(p)

    if page=='faculty':
        for el in select(root,'directory-count'):
            for b in el.xpath('./b'):b.tail=' members'
        for el in select(root,'directory-note'):
            for p in el.xpath('./p'):drop(p)
    if page=='academics':
        owner_cover('learning-computers')
        p=campus['class-operations'];image=root.xpath('.//*[@id="program-photo"]')[0]
        image.set('src',p['path']);image.set('alt',p['alt'])
        image.set('width',str(p['width']));image.set('height',str(p['height']))
        visual=select(root,'program-visual')[0];overlay=visual.xpath('./span')[0]
        number=overlay.xpath('./b')[0];number.tail=None
        caption=LH.Element('span',{'id':'program-photo-caption'});caption.text=p['caption'];overlay.append(caption)
        for el in select(root,'academic-jump'):drop(el)
        for panel in select(root,'learning-panel'):
            for el in select(panel,'kicker'):drop(el)
        for article in select(root,'feature'):
            heading=article.xpath('./h3');links=article.xpath('./a[@href]')
            if not heading or not links:continue
            link=LH.Element('a',{'href':links[0].get('href')});link.text=heading[0].text_content()
            contents(heading[0],'');heading[0].append(link)
            for el in article.xpath('./p|./a'):drop(el)
        for note in select(root,'source-note'):
            for a in note.xpath('.//a'):contents(a,'Official learning directions')
    if page=='news':
        for el in select(root,'news-card'):
            for p in el.xpath('./p'):drop(p)
    if page=='regulations':
        for el in select(root,'lead'):
            for p in el.xpath('./p'):drop(p)
    if page=='careers':
        for el in select(root,'career-roles'):
            seen={}
            for article in list(el):
                title=article.xpath('./h3')[0].text_content()
                paragraphs=article.xpath('./p')
                if title in seen:
                    for p in paragraphs:seen[title].append(p)
                    drop(article);continue
                details=LH.Element('details',{'class':'edition-career-examples'})
                summary=LH.Element('summary');summary.text='Published examples';details.append(summary)
                for p in paragraphs:details.append(p)
                article.append(details);seen[title]=details
        for figure in select(root,'career-photo'):
            crops=select(figure,'photo-crop')
            if crops:
                story=dict(data['career_story']);story['images']=[picture(**p) for p in story['images']];stories.append(story)
                crops[0].tag='a';crops[0].set('href',story['links'][0]['href']);crops[0].set('data-story-open',story['id']);crops[0].set('aria-label','View details: '+story['title'])

    # No repeated boilerplate in the public footer or around original profiles.
    if path.startswith('faculty-'):
        for a in root.xpath('.//a'):
            if 'Official faculty profile' in a.text_content():contents(a,'Official faculty profile')
    if stories:
        payload=LH.Element('script',{'type':'application/json','id':'editorial-story-data'})
        payload.text=json.dumps(stories,ensure_ascii=False).replace('</','<\\/')
        root.append(payload)
        root.append(node('''<dialog class="edition-story-dialog" id="edition-story-dialog" aria-labelledby="edition-story-title"><button type="button" class="edition-story-close" aria-label="Close story">×</button><div class="edition-story-heading"><span id="edition-story-label"></span><h2 id="edition-story-title"></h2><p id="edition-story-body"></p></div><div id="edition-story-images" class="edition-story-images"></div><div id="edition-story-links" class="edition-story-links"></div></dialog>'''))
    return ''.join(LH.tostring(c,encoding='unicode',method='html') for c in root)
