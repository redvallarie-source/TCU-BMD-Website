"""Consolidate student-life routes while keeping old bookmarks useful."""
from lxml import html as LH
from urllib.parse import urlsplit, urlunsplit

RETIRED={
    'exchange.html':'internships.html#global-opportunities',
    'outcomes.html':'student-life.html#life-projects',
    'international.html':'admissions.html',
}


def reconcile_links(markup):
    doc=LH.document_fromstring(markup)
    for link in doc.xpath('//a[@href]'):
        if link.xpath('ancestor::*[contains(concat(" ",@class," ")," source-body ")]'):continue
        parts=urlsplit(link.get('href'))
        if not parts.scheme and not parts.netloc and parts.path in RETIRED:
            replacement=urlsplit(RETIRED[parts.path])
            link.set('href',urlunsplit(('', '', replacement.path,parts.query,replacement.fragment)))
    return '<!doctype html>\n'+LH.tostring(doc,encoding='unicode',method='html')
