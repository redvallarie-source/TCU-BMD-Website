"""The shared gateway to placements, summer study, and academic exchange."""
from html import escape as esc
import json


def render_global(content):
    data=json.loads((content/'global-learning.json').read_text())
    words=data['copy']
    def t(key):return esc(words[key])
    def photo(key,extra='',priority=False):
        p=data['photos'][key]
        return f'''<figure class="intern-photo {extra}"><button type="button" data-gallery-open data-gallery-caption="{esc(p['caption'])}" aria-label="View photo: {esc(p['caption'])}"><img src="{p['path']}" alt="{esc(p['alt'])}" width="{p['width']}" height="{p['height']}" {'fetchpriority="high"' if priority else 'loading="lazy"'} decoding="async"><span class="intern-photo-view">{t('view_photo')}</span></button><figcaption>{esc(p['caption'])}</figcaption></figure>'''
    cover=f'''<section class="wrap intern-cover beyond-cover" aria-labelledby="intern-title"><div class="intern-cover-copy"><div class="kicker">{t('eyebrow')}</div><h1 id="intern-title">{t('title_first')}<span>{t('title_second')}</span></h1><p>{t('intro')}</p><nav class="intern-index" aria-label="On this page"><a href="#global-opportunities">{t('nav_programmes')}</a><a href="#intern-preparation">{t('nav_prepare')}</a><a href="#japan-field-journal">{t('nav_story')}</a></nav><div class="beyond-cover-note"><span>{t('note_first')}</span><span>{t('note_second')}</span></div></div><div class="beyond-cover-photos">{photo('uk','beyond-cover-main',True)}{photo('malaysia','beyond-cover-side')}</div></section>'''
    filters=''.join(f'''<button type="button" class="filter {'active' if i==0 else ''}" data-filter="{category}" aria-pressed="{str(i==0).lower()}">{esc(label)}</button>''' for i,(category,label) in enumerate(data['filters']))
    entries=''
    for i,p in enumerate(data['programmes']):
        links=''.join(f'''<a href="{esc(link['url'])}" class="intern-link" {'target="_blank" rel="noopener"' if link['url'].startswith('https:') else ''}>{esc(link['label'])}</a>''' for link in p['links'])
        entries+=f'''<article class="beyond-programme" data-filter-item data-category="{p['type']}" data-programme="{p['id']}"><div class="beyond-programme-place"><span class="beyond-programme-number">0{i+1}</span><div><h3>{esc(p['place'])}</h3><span>{esc(p['kind'])}</span></div></div><div class="beyond-programme-copy"><h4>{esc(p['title'])}</h4><p>{esc(p['body'])}</p></div><div class="beyond-programme-source"><span>{esc(p['status'])}</span>{links}</div></article>'''
    programmes=f'''<section class="wrap beyond-programmes" id="global-opportunities" aria-labelledby="beyond-programmes-title" data-filter-scope><div class="intern-section-head"><div><div class="kicker">{t('programmes_eyebrow')}</div><h2 id="beyond-programmes-title">{t('programmes_title')}</h2></div><p>{t('programmes_intro')}</p></div><div class="filters beyond-filters" aria-label="{t('filter_label')}">{filters}</div><div class="beyond-programme-list">{entries}</div><p class="beyond-archive-note">{t('availability')}</p><p class="empty" hidden>{t('empty')}</p></section>'''
    return cover+programmes
