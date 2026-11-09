"""Verified Chinese names and current listing additions, separate from retained sources."""
import copy
import json
import re
from lxml import html as LH


def verified(content):
    return json.loads((content/'faculty-verified.json').read_text())


def update_roster(original, content):
    records=copy.deepcopy(original)
    authority=verified(content)
    for person in authority['people']:
        match=next((f for f in records if re.sub(r'^Dr\.\s*','',f['name']).split(',')[0]==person['name_en']),None)
        if match is None and person.get('new_record'):
            records.append(copy.deepcopy(person['new_record']));continue
        if match and person.get('role_en_override'):
            match['name']='Dr. '+person['name_en']+', '+person['role_en_override']
    chinese={p['name_en']:p['name_zh'] for p in authority['people']}
    order={name:i for i,name in enumerate(authority.get('listing_order_zh',chinese.values()))}
    records.sort(key=lambda f:order[chinese[re.sub(r'^Dr\.\s*','',f['name']).split(',')[0]]])
    return records


def refine_people(path, body, content):
    if path!='faculty.html':return body
    root=LH.fragment_fromstring(body,create_parent='div')
    names={p['name_en']:p['name_zh'] for p in verified(content)['people']}
    for card in root.xpath('.//*[contains(concat(" ",@class," ")," person ")]'):
        heading=card.xpath('.//h3')[0].text_content().strip()
        assert heading in names, 'Unverified faculty identity: '+heading
        card.set('data-search-alias',heading+' '+names[heading])
    for link in root.xpath('.//a[contains(@href,"412-1021-4505")]'):
        link.set('href',verified(content)['source_url'])
    return ''.join(LH.tostring(el,encoding='unicode',method='html') for el in root)
