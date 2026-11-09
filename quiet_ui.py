"""Remove repeated UI decoration while retaining content and interaction targets."""
import re
from lxml import html as LH


def has_class(element, name):
    return name in element.get('class', '').split()


def elements(root, name):
    return [el for el in root.iter() if isinstance(el.tag,str) and has_class(el,name)]


def original_material(element):
    return any(has_class(ancestor,'source-body') for ancestor in [element,*element.iterancestors()])


def clean_marker(text):
    if not text or not re.search('[↗↖↘↙→]', text):
        return text
    return re.sub('[↗↖↘↙→]', '', text).rstrip()


def quiet_document(markup, path):
    root=LH.document_fromstring(markup)
    # These elements contain decoration only. No links or controls are removed.
    for cls in ['quick-arrow','quick-symbol','pathway-arrow','pathway-symbol',
                'story-open','portrait-arrow']:
        for el in list(elements(root,cls)):
            if not original_material(el):
                el.drop_tree()

    # Use a literal action for the photo viewer, rather than another diagonal arrow.
    for button in elements(root,'gallery-open'):
        for marker in button.xpath('./span'):
            marker.drop_tree()
        label=LH.Element('span',{'class':'gallery-action','aria-hidden':'true'})
        label.text='View photo'
        button.append(label)

    for link in root.xpath('//a'):
        if original_material(link):
            continue
        for svg in list(link.xpath('.//*[local-name()="svg"]')):
            # Shared link arrows; any actual navigation/search icons live in buttons.
            if has_class(svg,'icon'):
                svg.drop_tree()
        for el in list(link.iterdescendants()):
            if not isinstance(el.tag,str):
                continue
            if not len(el) and re.fullmatch(r'\s*[↗↖↘↙→]\s*',el.text or ''):
                el.drop_tree()
        for el in link.iter():
            if not isinstance(el.tag,str):
                continue
            el.text=clean_marker(el.text)
            if el is not link:
                el.tail=clean_marker(el.tail)

    # Numbers are useful in a timeline or calendar; they do not add meaning here.
    for label in list(elements(root,'editorial-index')):
        if re.fullmatch(r'\s*\d+\s*',label.text or ''):
            label.drop_tree()
        elif label.text:
            label.text=re.sub(r'^\d+\s*/\s*','',label.text)
    for card in elements(root,'experience-card'):
        for label in card.xpath('./span'):
            if label.text:
                label.text=re.sub(r'^\d+\s*/\s*','',label.text)
    for shortcuts in elements(root,'resource-shortcuts'):
        for index in shortcuts.xpath('./a/span'):
            index.drop_tree()
    for section in elements(root,'interior-next'):
        for icon in section.xpath('./a/i'):
            icon.drop_tree()
    for ticket in elements(root,'cohort-ticket'):
        for icon in ticket.xpath('.//i'):
            icon.drop_tree()
        ticket.xpath('./span')[0].text='Entry year'
        ticket.xpath('./small')[0].text='Latest listed cohort'
    for tab in elements(root,'learning-tab'):
        for icon in tab.xpath('./*[local-name()="svg"]'):
            icon.drop_tree()
    for category in elements(root,'story-category'):
        for rule in category.xpath('./i'):
            rule.drop_tree()
    if path=='index.html':
        count=len(elements(root,'story-slide'))
        for label in elements(root,'carousel-count'):
            label.text=f'{count} stories'
    return LH.tostring(root,encoding='unicode',method='html',doctype='<!doctype html>')
