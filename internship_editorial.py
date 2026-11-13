"""A source-backed internship field journal, within the established BMD site."""
from html import escape as esc
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from lxml import html as LH
from homepage import ambient
from global_learning import render_global

HUB='https://mdm.tcu.edu.tw/p/412-1021-5007.php?Lang=zh-tw'
JAPAN='https://mdm.tcu.edu.tw/p/406-1021-66149,r8.php?Lang=zh-tw'
SELECTION='https://mdm.tcu.edu.tw/p/406-1021-65596,r930.php?Lang=zh-tw'


def render_internships(old_body, content):
    material=json.loads((content/'internship-editorial.json').read_text())
    words=material['copy']
    def t(key):return esc(words[key])
    def photo(key,cls='',priority=False):
        p=material['photos'][key]
        return f'''<figure class="intern-photo {cls}"><button type="button" data-gallery-open data-gallery-caption="{esc(p['caption'])}" aria-label="View photo: {esc(p['caption'])}"><img src="{p['path']}" alt="{esc(p['alt'])}" width="{p['width']}" height="{p['height']}" {'fetchpriority="high"' if priority else 'loading="lazy"'} decoding="async"><span class="intern-photo-view">{t('view_photo')}</span></button><figcaption>{esc(p['caption'])}</figcaption></figure>'''
    original=LH.fragment_fromstring(old_body,create_parent='div')
    scope=original.xpath('.//*[@data-filter-scope]')[0]
    # Keep every original file URL and the existing filtering/pagination behavior.
    # Replace format-only labels with the document's actual official title.
    titles=material['document_titles']
    previous=''
    for link in scope.xpath('.//a[@data-filter-item]'):
        name=unquote(urlsplit(link.get('href')).path).split('/')[-1]
        label=link.xpath('.//b')[0]
        small=link.xpath('.//small')
        context=small[0].text_content() if small else ''
        title=titles.get(name)
        if not title:
            clean=re.sub(r'【(?:docx?|pdf)】|\b(?:docx?|pdf)\b','',context,flags=re.I).strip()
            if re.search(r'[\u4e00-\u9fff]',clean):title=clean
            else:title=previous
        if title:label.text=title;previous=title
        if small:small[0].text=''
    resource_scope=LH.tostring(scope,encoding='unicode',method='html')
    intro=f'''<section class="wrap intern-cover intern-case-cover" aria-labelledby="tokyo-case-title"><div class="intern-cover-copy"><div class="kicker">{t('case_eyebrow')}</div><h2 id="tokyo-case-title">{t('case_title')}</h2><p>{t('case_intro')}</p><nav class="intern-index" aria-label="On this page"><a href="#tokyo-work">{t('nav_work')}</a><a href="#intern-service">{t('nav_service')}</a></nav><div class="intern-place-mark"><span>{t('featured')}</span><b>{t('tokyo')}</b><small>{t('host_year')}</small></div></div><div class="intern-cover-image">{photo('cohort','intern-cover-photo')}<div class="intern-photo-tab" aria-hidden="true">TOKYO <span>2026</span></div></div></section>'''
    rhythm=f'''<section class="intern-rhythm motion-region" data-ambient-surface aria-labelledby="intern-day-heading">{ambient('breeze')}<div class="wrap intern-rhythm-inner"><div><div class="kicker">{t('day_label')}</div><h2 id="intern-day-heading">{t('day_title')}</h2></div><div class="intern-hours"><time datetime="09:00">09:00</time><div class="intern-day-line" aria-hidden="true"><span></span><i></i><i></i><i></i></div><time datetime="17:00">17:00</time></div><p>{t('day_body')}</p></div><button type="button" class="ambient-control" aria-pressed="false" aria-label="Pause background motion">Pause background motion</button></section>'''
    tabs='';panels=''
    for i,w in enumerate(material['work']):
        ident=w['id'];num=f'{i+1:02d}'
        tabs+=f'''<button type="button" role="tab" id="intern-tab-{ident}" aria-controls="intern-panel-{ident}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}" data-intern-tab="{ident}"><span>{num}</span><b>{esc(w['label'])}</b></button>'''
        picture='<div class="intern-tab-photo">'+photo(w['photo_key'])+'</div>'
        anchor=' id="intern-service"' if ident=='community' else ''
        source=f'<a class="intern-link" href="{JAPAN}" target="_blank" rel="noopener">{t("service_source")}</a>' if ident=='community' else ''
        panels+=f'''<article role="tabpanel" tabindex="0" id="intern-panel-{ident}" aria-labelledby="intern-tab-{ident}" class="intern-work-panel"><div class="intern-tab-copy"{anchor}><h3>{esc(w['title'])}</h3><p>{esc(w['body'])}</p>{source}</div>{picture}</article>'''
    work=f'''<section class="wrap intern-work" id="tokyo-work"><div class="intern-section-head"><div><div class="kicker">{t('work_eyebrow')}</div><h2 data-intern-reveal>{t('work_title')}</h2></div><p>{t('work_intro')}</p></div><div class="intern-notebook"><div class="intern-work-tabs" role="tablist" aria-label="{t('work_tabs_label')}" aria-orientation="horizontal">{tabs}</div><div class="intern-work-panels">{panels}</div></div></section>'''
    guide=''
    for i,g in enumerate(material['preparation']):
        guide+=f'''<details class="intern-guide-step" {'open' if i==0 else ''}><summary><span>0{i+1}</span><b>{esc(g['title'])}</b><i aria-hidden="true">+</i></summary><p>{esc(g['body'])}</p></details>'''
    preparation=f'''<section class="intern-preparation" id="intern-preparation"><div class="wrap"><div class="intern-section-head"><div><div class="kicker">{t('prepare_eyebrow')}</div><h2>{t('prepare_title')}</h2></div><p>{t('prepare_intro')}</p></div><div class="intern-prep-grid"><div class="intern-guide">{guide}<a class="intern-link" href="{HUB}" target="_blank" rel="noopener">{t('hub_link')}</a></div><aside class="intern-opportunity"><span>{t('planning_label')}</span><h3>{t('planning_title')}</h3><p>{t('planning_body')}</p><a class="intern-link" href="https://mdm.tcu.edu.tw/p/412-1021-62.php?Lang=zh-tw" target="_blank" rel="noopener">{t('exchange_collection')}</a><a class="intern-contact" href="contact.html">{t('planning_contact')}</a></aside></div><details class="intern-resources" id="intern-documents"><summary><span><b>{t('documents_title')}</b><small>{t('documents_intro')}</small></span><i aria-hidden="true">+</i></summary><div class="intern-documents-body">{resource_scope}</div></details></div></section>'''
    end=f'''<div class="wrap intern-end"><a href="student-life.html">{t('life_link')}</a><a href="#global-opportunities">{t('all_pathways')}</a><details><summary>{t('sources_label')}</summary><p>{t('sources_body')}</p><a href="{HUB}" target="_blank" rel="noopener">{t('hub_link')}</a><a href="{JAPAN}" target="_blank" rel="noopener">{t('service_source')}</a><a href="https://mdm.tcu.edu.tw/var/file/21/1021/img/622653375.pdf" target="_blank" rel="noopener">{t('policy_link')}</a><a href="https://mdm.tcu.edu.tw/var/file/21/1021/img/485747469.pdf" target="_blank" rel="noopener">{t('guidelines_link')}</a></details></div>'''
    gallery='''<dialog class="photo-dialog" id="photo-dialog" aria-labelledby="photo-caption"><button class="photo-close icon-btn" aria-label="Close photo">×</button><img id="photo-full" src="assets/internships/tokyo-cohort.webp" alt=""><div class="photo-dialog-footer"><button class="photo-previous" aria-label="Previous photo">←</button><p id="photo-caption"></p><button class="photo-next" aria-label="Next photo">→</button></div></dialog>'''
    preview=material.get('summary_photo',material['photos']['cohort'])
    notes=f'''<details class="intern-extra-notes"><summary class="wrap"><span>{t('extra_notes')}</span><span aria-hidden="true">+</span></summary><div class="intern-extra-content">{work}</div></details>'''
    story=f'''<details class="intern-japan-story" id="japan-field-journal"><summary class="wrap intern-story-summary"><div><div class="kicker">{t('story_eyebrow')}</div><h2>{t('story_title')}</h2><p>{t('story_intro')}</p><span class="intern-story-action"><span class="story-closed-label">{t('story_open')}</span><span class="story-open-label">{t('story_close')}</span><i aria-hidden="true">+</i></span></div><img class="intern-story-preview" src="{preview['path']}" alt="{esc(preview['alt'])}" width="{preview['width']}" height="{preview['height']}" loading="lazy" decoding="async"></summary><div class="intern-story-content">{intro+rhythm+notes}</div></details>'''
    return '<div class="bmd-internships">'+render_global(content)+story+preparation+end+'</div>'+gallery
