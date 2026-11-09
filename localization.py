"""Build real, linked Traditional Chinese pages from the curated English site.

Original source bodies, personal names and document files retain their published
language. No translation service or browser-side DOM replacement is required.
"""
from pathlib import Path
import copy
import hashlib
import json
import re
from urllib.parse import urlsplit, urlunsplit
from lxml import html as LH


def norm(value):
    return ' '.join(value.split())


def dictionary(root):
    translations = {}
    for line in (root/'content/translations-zh-Hant.txt').read_text().splitlines():
        if line.lstrip().startswith('#') or ' | ' not in line:
            continue
        en, zh = line.split(' | ', 1)
        translations[norm(en)] = zh.strip()
    authority=json.loads((root/'content/faculty-verified.json').read_text())
    translations.update(json.loads((root/'content/internship-editorial.json').read_text())['translations'])
    translations.update(json.loads((root/'content/global-learning.json').read_text())['translations'])
    translations.update(json.loads((root/'content/compact-editorial.json').read_text())['translations'])
    translations.update(json.loads((root/'content/information-design.json').read_text())['translations'])
    translations.update(json.loads((root/'content/japan-photo-selection.json').read_text())['translations'])
    for person in authority['people']:
        translations[person['name_en']]=person['name_zh']
    # Names inside existing translated news headlines use the same official spelling.
    for key,value in list(translations.items()):
        for person in authority['people']:value=value.replace(person['name_en'],person['name_zh'])
        translations[key]=value
    return translations


def translator(translations):
    def translate(value):
        if not value or not value.strip():
            return value
        key = norm(value)
        result = translations.get(key)
        if result is None and key.endswith('.'):
            result=translations.get(key.rstrip('.'))
        if result is None:
            match = re.fullmatch(r'(11[1-5]) curriculum', key)
            if match:
                result = match[1]+'學年度課程'
            match = re.fullmatch(r'(11[1-5]) Admission Courses', key)
            if match:
                result = match[1]+'學年度入學課程'
            match = re.fullmatch(r'(\d{4}) entry · (\d+) original documents?', key)
            if match:
                result = f'{match[1]}年入學・{match[2]}份原始文件'
            if key == '2022 entry · Files not listed':
                result = '2022年入學・未提供文件'
            match = re.fullmatch(r'(\w+) (20\d\d)', key)
            months = ['January','February','March','April','May','June','July','August','September','October','November','December']
            if match and match[1] in months:
                result = f'{match[2]}年{months.index(match[1])+1}月'
            if key.startswith('PDF preview: '):
                result='PDF預覽：'+translate(key[13:])
            if key.startswith('Preview PDF: '):
                result='預覽PDF：'+translate(key[13:])
            if key.startswith('View photo: '):
                result='查看照片：'+translate(key[12:])
            if key.startswith('View details: '):
                result='查看內容：'+translate(key[14:])
            match=re.fullmatch(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), (\w+) (\d+), (20\d\d)(, event scheduled)?',key)
            if match and match[2] in months:
                weekdays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
                result=f'{match[4]}年{months.index(match[2])+1}月{match[3]}日（週'+['一','二','三','四','五','六','日'][weekdays.index(match[1])]+'）'+('，當日有行事' if match[5] else '')
        if result is None:
            return value
        return re.match(r'^\s*',value).group()+result+re.search(r'\s*$',value).group()
    return translate


def zh_route(url, routes):
    parts = urlsplit(url)
    if not parts.scheme and not parts.netloc and parts.path in routes:
        return urlunsplit(('', '', 'zh-'+parts.path, parts.query, parts.fragment))
    return url


def fingerprint(dist, path):
    return path+'?v='+hashlib.sha256((dist/path).read_bytes()).hexdigest()[:12]


def switch_label(element, full, short):
    element.text=None
    for child in list(element):element.remove(child)
    label=LH.Element('span',{'class':'language-full'});label.text=full;element.append(label)
    compact=LH.Element('span',{'class':'language-short','aria-hidden':'true'});compact.text=short;element.append(compact)


def localized_scripts(dist, translations):
    """Wrap translatable UI literals, leaving the original JS as maintained source."""
    scripts={}
    string = re.compile(r"'((?:\\.|[^'\\])*)'|\"((?:\\.|[^\"\\])*)\"")
    for name in ['site','interior','homepage','refinement','campus-motion']:
        source=(dist/f'assets/{name}.js').read_text()
        def replace(match):
            literal=match.group(0)
            try:
                value=json.loads(literal) if literal[0]=='"' else bytes(literal[1:-1],'utf-8').decode('unicode_escape') if '\\' in literal else literal[1:-1]
            except (ValueError,UnicodeDecodeError):
                return literal
            if norm(value) in translations:
                return 'BMDI18n.t('+literal+')'
            return literal
        source=string.sub(replace,source)
        source=source.replace("new Intl.DateTimeFormat('en',",'new Intl.DateTimeFormat(BMDI18n.locale,')
        source=source.replace("fetch('assets/search-index.json')","fetch(BMDI18n.isZh?'assets/search-index-zh.json':'assets/search-index.json')")
        # These pieces are computed after an interaction rather than a static node.
        # Do not leave a misleading café caption on a project-presentation photo.
        source=source.replace('Student café operations as applied management learning','Students from the department’s Indonesian cohort presenting a project')
        target=f'assets/{name}-localized.js'
        (dist/target).write_text(source)
        scripts[f'assets/{name}.js']=target
    return scripts


def data_translate(value, translate):
    if isinstance(value, str):return translate(value)
    if isinstance(value, list):return [data_translate(v,translate) for v in value]
    if isinstance(value, dict):return {k:data_translate(v,translate) for k,v in value.items()}
    return value


def build_languages(root):
    dist=root/'dist'
    translations=dictionary(root)
    translate=translator(translations)
    runtime="""'use strict';
(()=>{
 const words=__WORDS__;
 const isZh=document.documentElement.lang==='zh-Hant';
 function t(value){if(!isZh||typeof value!=='string')return value;const key=value.replace(/\\s+/g,' ').trim(),found=words[key];if(found===undefined)return value;return (value.match(/^\\s*/)||[''])[0]+found+(value.match(/\\s*$/)||[''])[0]}
 window.BMDI18n={t,isZh,locale:isZh?'zh-TW':'en'};
})();
""".replace('__WORDS__',json.dumps(translations,ensure_ascii=False,separators=(',',':')))
    (dist/'assets/i18n.js').write_text(runtime)
    scripts=localized_scripts(dist,translations)
    originals=sorted(p for p in dist.glob('*.html') if not p.name.startswith('zh-'))
    routes={p.name for p in originals}
    chinese_index=[]
    preserved_bodies=0
    for page in originals:
        en=LH.document_fromstring(page.read_text())
        for script in en.xpath('//script[@src]'):
            path=urlsplit(script.get('src')).path
            if path in scripts:script.set('src',fingerprint(dist,scripts[path]))
            elif path=='assets/i18n.js':script.set('src',fingerprint(dist,path))
        # One language switch lives alongside the shared navigation utilities.
        switch=en.xpath('//header//a[contains(concat(" ",@class," ")," language-switch ")]')[0]
        switch.set('href','zh-'+page.name)
        switch.set('class','language-switch')
        switch.set('lang','zh-Hant')
        switch.set('hreflang','zh-Hant')
        switch.set('aria-label','繁體中文 — Read this page in Traditional Chinese')
        for attr in ['target','rel']:switch.attrib.pop(attr,None)
        switch_label(switch,'繁體中文','繁中')
        for existing in en.xpath('//head/link[@rel="alternate"]'):existing.getparent().remove(existing)
        head=en.find('head')
        for lang,href in [('en',page.name),('zh-Hant','zh-'+page.name)]:
            el=LH.Element('link',rel='alternate',hreflang=lang,href=href);head.append(el)
        zh=copy.deepcopy(en)
        zh.set('lang','zh-Hant')
        for text in zh.xpath('//body//text()[not(ancestor::script|ancestor::style|ancestor::svg)]'):
            parent=text.getparent()
            # An official source is kept intact even when its surrounding UI is Chinese.
            check=parent.getparent() if text.is_tail else parent
            if check is not None and (check.get('class')=='source-body' or check.xpath('ancestor::*[contains(concat(" ",normalize-space(@class)," ")," source-body ")]')):
                continue
            value=translate(str(text))
            if text.is_tail:parent.tail=value
            else:parent.text=value
        for el in zh.iter():
            if not isinstance(el.tag,str):continue
            for attr in ['aria-label','alt','title','placeholder','data-gallery-caption','data-pdf-title','data-initial-label']:
                if el.get(attr):el.set(attr,translate(el.get(attr)))
            if el.tag=='a' and el.get('href'):
                el.set('href',zh_route(el.get('href'),routes))
            if el.tag=='link' and el.get('rel')=='canonical':
                el.set('href',zh_route(el.get('href'),routes))
            if el.tag=='meta' and el.get('name')=='bmd-redirect':
                el.set('content',zh_route(el.get('content'),routes))
            if el.tag=='meta' and el.get('http-equiv')=='refresh':
                delay,target=el.get('content').split(';url=',1)
                el.set('content',delay+';url='+zh_route(target,routes))
            if el.tag=='script' and el.get('type')=='application/json' and el.text:
                if el.get('id') in {'calendar-data','life-scene-data','life-project-data','editorial-story-data'}:
                    el.text=json.dumps(data_translate(json.loads(el.text),translate),ensure_ascii=False).replace('</','<\\/')
                    if el.get('id')=='editorial-story-data':
                        stories=json.loads(el.text)
                        for story in stories:
                            for link in story['links']:link['href']=zh_route(link['href'],routes)
                        el.text=json.dumps(stories,ensure_ascii=False).replace('</','<\\/')
        # Chinese readers see the exact published credential name first, with the
        # English reading aid retained as a searchable alias underneath.
        for row in zh.xpath('//tr[@data-certificate-en]'):
            name=row.xpath('./td[1]/b')[0]
            alias=row.xpath('./td[1]/small')[0]
            name.text=alias.text
            alias.text=row.get('data-certificate-en')
            alias.set('lang','en')
        # Direction names span two lines in English; Chinese has its own natural rhythm.
        for h3,name in zip(zh.xpath('//*[contains(concat(" ",@class," ")," pathway-card ")]//h3'),['營運管理','智慧商務','永續創新','餐飲管理']):
            for child in list(h3):h3.remove(child)
            h3.text=name
        # Retain author names and original-language qualifications where no official equivalent exists.
        source_bodies=zh.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," source-body ")]')
        for source in source_bodies:
            notice=LH.Element('p',{'class':'original-language-note'})
            notice.text='以下資料保留官方發布原文；文件與外部連結亦維持原始語言。'
            source.addprevious(notice);preserved_bodies+=1
        if page.name.startswith('faculty-'):
            sheet=zh.xpath('//*[contains(concat(" ",@class," ")," profile-sheet ")]')
            if sheet:
                notice=LH.Element('p',{'class':'original-language-note'})
                notice.text='姓名採系所官方中文名錄；部分學經歷保留官方發布原文。最新資訊請參閱原始系所頁面。'
                sheet[0].addprevious(notice)
                notice.set('class','wrap original-language-note')
        switch=zh.xpath('//a[contains(concat(" ",@class," ")," language-switch ")]')[0]
        switch.set('href',page.name);switch.set('lang','en');switch.set('hreflang','en');switch.set('aria-label','English — Read this page in English');switch_label(switch,'English','EN')
        for a in zh.xpath('//footer//a[starts-with(@href,"https://mdm.tcu.edu.tw/?Lang=")]'):
            a.set('href','https://mdm.tcu.edu.tw/?Lang=zh-tw')
        first=zh.xpath('//main//h1')
        title=norm(first[0].text_content()) if first else translate(en.find('head/title').text)
        zh.find('head/title').text=title+'｜慈濟大學經營管理學系'
        for meta in zh.xpath('//head/meta[@name="description"]'):
            meta.set('content',title+'・慈濟大學經營管理學系。系所資訊、師資、學生作品與學習資源。')
        zh_path='zh-'+page.name
        for doc,target in [(en,page),(zh,dist/zh_path)]:
            target.write_text('<!doctype html>\n'+LH.tostring(doc,encoding='unicode',method='html'),encoding='utf-8')
        main=copy.deepcopy(zh.xpath('//main')[0])
        story_text=' '.join(' '.join(str(v.get(k,'')) for k in ('label','title','body')) for script in main.xpath('.//script[@id="editorial-story-data"]') for v in json.loads(script.text))
        for ignored in main.xpath('.//script|.//dialog|.//svg'):ignored.getparent().remove(ignored)
        aliases=' '.join(main.xpath('.//*[@data-search-alias]/@data-search-alias'))
        if page.name.startswith('faculty-'):aliases+=' '+norm(en.xpath('//main//h1')[0].text_content())
        if not zh.xpath('//meta[@name="bmd-redirect"]'):
            chinese_index.append({'url':zh_path,'title':title,'category':'原始資料' if page.name.startswith('source-') else '系所資訊','text':norm(main.text_content())[:3500]+' '+aliases+' '+story_text})
    original_index=json.loads((dist/'assets/search-index.json').read_text())
    for record in original_index:
        if record['url'].startswith('faculty-'):record['text']+=' '+translate(record['title'])
        if record['url']=='faculty.html':record['text']+=' '+' '.join(p['name_zh'] for p in json.loads((root/'content/faculty-verified.json').read_text())['people'])
    (dist/'assets/search-index.json').write_text(json.dumps(original_index,ensure_ascii=False))
    chinese_index.extend({'url':item['url'],'title':translate(item['title']),'category':'原始文件','text':translate(item.get('text',''))} for item in original_index if item['url'] not in routes)
    (dist/'assets/search-index-zh.json').write_text(json.dumps(chinese_index,ensure_ascii=False))
    report={'english_pages':len(originals),'chinese_pages':len(originals),'translations':len(translations),'chinese_search_records':len(chinese_index),'original_source_bodies_preserved':preserved_bodies,'document_language':'Original official publication language retained'}
    (root/'language-check-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False))
