"""Selected, checked dates and an accessible calendar before JavaScript loads."""
from datetime import datetime,date,timedelta
from zoneinfo import ZoneInfo
from lxml import html as LH
import json

def hydrate_calendar(root,content_root):
    calendars=root.xpath('.//*[@id="calendar"]')
    if not calendars:return
    data=json.loads((content_root/'academic-events.json').read_text());events=data['events'];config=data['range']
    today=datetime.now(ZoneInfo(config['timeZone'])).date();first=date.fromisoformat(config['start']);last=date.fromisoformat(config['end'])
    showing=min(max(today,first),last);month=date(showing.year,showing.month,1)
    title=month.strftime('%B %Y')
    for key in ['calendar-month','event-list-title']:root.get_element_by_id(key).text=title
    root.get_element_by_id('calendar-data').text=json.dumps(events,ensure_ascii=False).replace('</','<'+chr(92)+'/')
    script=LH.Element('script',{'type':'application/json','id':'calendar-config'});script.text=json.dumps(config);calendars[0].addnext(script)
    days=root.get_element_by_id('calendar-days');days.clear();days.set('class','days');days.set('id','calendar-days')
    start=month-timedelta(days=month.weekday())
    for i in range(42):
        current=start+timedelta(days=i);key=current.isoformat();has=any(e['start']<=key<=e['end'] for e in events)
        button=LH.Element('button',{'type':'button','class':'day'+(' event' if has else '')+(' outside' if current.month!=month.month else ''),'aria-pressed':'false','aria-label':current.strftime('%A, %B ')+str(current.day)+', '+str(current.year)+(', event scheduled' if has else '')});button.text=str(current.day)
        if current.month!=month.month:button.set('disabled','')
        if current==today:button.set('aria-current','date');button.set('class',button.get('class')+' today')
        days.append(button)
    for key,disabled in [('cal-previous',month<=first),('cal-next',month.year==last.year and month.month==last.month)]:
        control=root.get_element_by_id(key)
        if disabled:control.set('disabled','')
        else:control.attrib.pop('disabled',None)
    next_month=date(month.year+(month.month==12),month.month%12+1,1);end=next_month-timedelta(days=1)
    listing=root.get_element_by_id('calendar-events');listing.clear();listing.set('id','calendar-events');listing.set('aria-live','polite')
    chosen=[e for e in events if e['start']<=end.isoformat() and e['end']>=month.isoformat()]
    completed=[e for e in chosen if e['end']<today.isoformat()]
    upcoming=sorted([e for e in chosen if e not in completed],key=lambda e:e['start'])
    completed_list=LH.Element('details',{'class':'calendar-completed'})
    summary=LH.Element('summary');summary.text='Completed dates';completed_list.append(summary)
    for event in upcoming+completed:
        state='completed' if event['end']<today.isoformat() else 'upcoming' if event['start']>today.isoformat() else 'ongoing'
        article=LH.Element('article',{'class':'event-card','data-event-state':state})
        badge=LH.Element('span',{'class':'event-state'});badge.text={'completed':'Completed','upcoming':'Upcoming','ongoing':'In progress'}[state]
        article.extend([badge,LH.Element('br')])
        small=LH.Element('small');small.text=event['start']+(' — '+event['end'] if event['end']!=event['start'] else '')
        heading=LH.Element('h3');heading.text=event['title'];description=LH.Element('p');description.text=event['description'];article.extend([small,heading,description]);(completed_list if state=='completed' else listing).append(article)
    if completed:listing.append(completed_list)
    if not chosen:
        message=LH.Element('p',{'class':'empty'});message.text='No selected dates listed this month. Consult the full university calendar.';listing.append(message)
    status=LH.Element('p',{'class':'calendar-status','id':'calendar-status'});status.text='Selected dates from the 2026–2027 calendar · Taiwan time. '
    updates=LH.Element('a',{'href':data['official_updates'],'target':'_blank','rel':'noopener'});updates.text='University calendar updates ↗';status.append(updates);calendars[0].append(status)
