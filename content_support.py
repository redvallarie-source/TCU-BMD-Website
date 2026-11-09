"""Targeted information and document improvements from the content review."""
from lxml import html as LH
from urllib.parse import urlsplit
import hashlib,json,re
from calendar_data import hydrate_calendar

def select(root,cls):return root.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," '+cls+' ")]')
def node(markup):return LH.fromstring(markup)
def normalize_document(record):
    out=dict(record);filename=urlsplit(out.get('url','')).path.rsplit('/',1)[-1]
    presentations={
        '836002241.pptx':('Department presentation — Chinese (2026)','PPTX · Publisher-listed size: 55.8 MB'),
        '190825241.pptx':('Department presentation — English (2026)','PPTX · Publisher-listed size: 36.3 MB'),
        '596109525.pptx':('Tourism and culinary training — Vietnam cohort (English)','PPTX · Publisher-listed size: 9.62 MB'),
        '578588702.pdf':('Department admissions resource (PDF)','Original filename: 578588702.pdf'),
    }
    if filename in presentations:
        out['source_label']=out.get('label',out.get('text',''));out['label'],out['context']=presentations[filename]
    return out

def support(path,body,content_root,archive_paths=()):
    key=path.removesuffix('.html');root=LH.fragment_fromstring(body,create_parent='div')
    hydrate_calendar(root,content_root)
    if key=='curriculum':
        for card in select(root,'cohort-card'):
            resources=select(card,'resource-link');summary=card.xpath('./summary/span/small')[0];year=card.get('data-category');ce=int(year)+1911
            summary.text=f'{ce} entry · '+(f'{len(resources)} original document'+('s' if len(resources)!=1 else '') if resources else 'Files not listed')
            if not resources:
                content=select(card,'cohort-body')[0]
                for empty in select(content,'resource-list'):empty.getparent().remove(empty)
                content.insert(0,node('<div class="availability-note"><h3>Documents currently unavailable here</h3><p>Files for this entry year are not available in this document list. Contact the department or check the original course page for the curriculum that applies to your cohort.</p><a class="text-link" href="contact.html">Contact the department ↗</a></div>'))
    elif key=='careers':
        tables=root.xpath('.//table')[-2:]
        groups=[('Business Management','Department of Business Management · One year after graduation'),('International Service Industry Management','Bachelor’s programme · One year after graduation')]
        for table,(title,desc) in zip(tables,groups):
            first=table.xpath('./tr[1]/*|./tbody/tr[1]/*')
            for cell,label in zip(first,['Academic year','Graduates','Graduates with reported status','Employment, further study or military service']):cell.text=label
            for cell in table.xpath('.//td'):
                if cell.text:cell.text=cell.text.replace('※36名外籍生','(source note: 36 international students)').replace('※8名外籍生','(source note: 8 international students)')
            wrap=table.getparent();parent=wrap.getparent();index=parent.index(wrap)
            group=LH.Element('section',{'class':'graduate-group'});h=LH.Element('h3');h.text=title;p=LH.Element('p');p.text=desc;group.extend([h,p]);parent.insert(index,group);group.append(wrap)
    elif key=='vision':
        notes=select(root,'source-note')
        if notes:
            link=notes[0].xpath('.//a')[0];link.text='Read the official educational goals ↗'
            notes[0].text='These summaries are adapted from the department’s published educational goals. '
            notes[0].set('class','source-note interpretation-note')
    elif key=='news':
        scope=root.xpath('.//*[@data-filter-scope]')[0];scope.set('data-filter-default','published')
        for button in scope.xpath('.//*[@data-filter="all"]'):button.set('data-filter','published');button.text='News & achievements'
    elif key=='exchange':
        z=json.loads((content_root/'official-zh/manifest.json').read_text())['pages'];source=next(p for p in z if p.get('category')=='international_exchange' and p.get('depth')==0)
        url=source['url'];local='source-'+hashlib.sha1(url.encode()).hexdigest()[:12]+'.html'
        stories=[
            ('Summer learning · United Kingdom','Nottingham Trent University','A department video shares students’ summer learning experience at Nottingham Trent University.','https://mdm.tcu.edu.tw/var/file/21/1021/img/1532/838246904.mp4','Watch the department video'),
            ('Internship · Malaysia','ViTrox','Students share their internship experience at ViTrox in a video published by the department.','https://mdm.tcu.edu.tw/var/file/21/1021/img/1532/126739396.mp4','Watch the department video'),
            ('Visiting scholar · On campus','Branding and communication','A visiting scholar from Hamburg’s Brand Academy shared branding and communication practice with students on campus.',local,'Read the department account'),
        ]
        section=LH.Element('section',{'class':'wrap published-experiences'});h=LH.Element('h2');h.text='Published department experiences';p=LH.Element('p');p.text='Examples documented by the department. These are experience reports, rather than current application announcements.';section.extend([h,p]);grid=LH.Element('div',{'class':'experience-grid'})
        for tag,title,description,href,label in stories:
            article=LH.Element('article',{'class':'experience-card'});small=LH.Element('span');small.text=tag;heading=LH.Element('h3');heading.text=title;copy=LH.Element('p');copy.text=description;link=LH.Element('a',{'href':href,'class':'text-link'});link.text=label+' ↗'
            if href.startswith('https:'):link.set('target','_blank');link.set('rel','noopener')
            article.extend([small,heading,copy,link]);grid.append(article)
        section.append(grid);heroes=select(root,'page-hero');heroes[0].addnext(section)
        for old in list(select(root,'feature-grid')):
            if 'Overseas learning experiences' in old.text_content():old.getparent().remove(old)
        leads=select(root,'lead')
        if leads:
            heading=leads[0].xpath('./h2')
            if heading:
                for child in list(heading[0]):heading[0].remove(child)
                heading[0].text='Original department resources'
            paragraphs=leads[0].xpath('./p')
            if paragraphs:paragraphs[0].text='Browse the source collection for the full set of published videos and international-learning information.'
    elif key=='content-review':
        faqs=select(root,'faq')
        if faqs:
            faqs[0].append(node('<p class="publication-exclusion-note">One legacy notice containing account-access instructions is intentionally excluded from the published pages and search index.</p>'))
    if path in archive_paths:
        note=node('<div class="wrap archive-context"><strong>Historical department archive</strong><p>This notice may refer to an earlier department name or system. It is retained as historical material, rather than current student guidance.</p></div>');hero=select(root,'page-hero')
        if hero:hero[0].addnext(note)
    preview_count=0
    cache_file=content_root/'document-previews.json';preview_cache=json.loads(cache_file.read_text()) if cache_file.exists() else {}
    if not key.startswith('source-'):
        for resource in list(select(root,'resource-link')):
            href=resource.get('href','')
            if resource.tag!='a' or not urlsplit(href).path.lower().endswith('.pdf'):continue
            preview_src=href if href.startswith('assets/') else preview_cache.get(href,{}).get('asset')
            if not preview_src:continue
            wrapper=LH.Element('div',{'class':'resource-entry'})
            for attr in ['data-filter-item','data-category']:
                if attr in resource.attrib:wrapper.set(attr,resource.attrib.pop(attr))
            parent=resource.getparent();parent.replace(resource,wrapper);wrapper.append(resource)
            title=' '.join(resource.xpath('.//b')[0].itertext()) if resource.xpath('.//b') else 'Department document'
            button=LH.Element('button',{'class':'document-preview-open','type':'button','data-pdf-url':href,'data-preview-src':preview_src,'data-pdf-title':title,'aria-label':'Preview PDF: '+title});button.text='Preview';wrapper.append(button);preview_count+=1
    if preview_count:
        root.append(node('<dialog id="document-preview" class="document-dialog" aria-labelledby="document-preview-title"><div class="document-dialog-head"><div><span>PDF preview</span><h2 id="document-preview-title">Department document</h2></div><button type="button" class="document-preview-close icon-btn" aria-label="Close document preview">×</button></div><p class="document-preview-help">Preview of the saved published PDF. Use the original link below to open the source document.</p><iframe id="document-preview-frame" title="Document preview" src="about:blank" referrerpolicy="no-referrer"></iframe><div class="document-dialog-foot"><a class="text-link" id="document-preview-original" href="#" target="_blank" rel="noopener">Open original PDF ↗</a></div></dialog>'))
    return ''.join(LH.tostring(child,encoding='unicode',method='html') for child in root)
