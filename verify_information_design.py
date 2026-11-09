"""Guard the new reading aid against the retained official points and names."""
from collections import Counter
from datetime import datetime
from pathlib import Path
import json
import shutil
import subprocess
from lxml import html as LH

ROOT=Path(__file__).parent
D=ROOT/'dist'
source=next(p for p in json.loads((ROOT/'content/official-en/pages.json').read_text(encoding='utf-8')) if p.get('key')=='c32918c65d8f')
expected=[]
for row in source['tables'][0][1:]:
    expected.extend((name.strip(),row[-1].replace('點','')) for name in row[-2].split('\n') if name.strip())
expected.extend((row[1],row[2].replace('點','')) for row in source['tables'][1][1:])
errors=[]
for prefix in ('','zh-'):
    tree=LH.parse(str(D/(prefix+'requirements.html')))
    rows=tree.xpath('//tr[@data-certificate-en]')
    actual=[]
    for row in rows:
        cells=row.xpath('./td')
        original=cells[0].xpath('./b' if prefix else './small')[0].text
        points=cells[2].text_content().strip()
        actual.append((original,points))
        if not row.get('data-certificate-en'):errors.append('Missing English certificate alias')
    if Counter(actual)!=Counter(expected):errors.append(prefix+'Certificate names or points differ from the publication')
    if len(tree.xpath('//details[@id="original-certificate-tables"]//table'))!=2:errors.append(prefix+'Missing original certificate tables')
    if not tree.xpath('//input[@id="certificate-search"][@type="search"]'):errors.append(prefix+'Missing certificate search')
    admissions=LH.parse(str(D/(prefix+'admissions.html')))
    if not admissions.xpath('//*[@id="international-applicants"]//a[@href="https://oga.tcu.edu.tw/international-student/"]'):errors.append(prefix+'Missing international application gateway')
    if admissions.xpath('//a[@href="#department-resources"]') and not admissions.xpath('//*[@id="department-resources"]'):errors.append(prefix+'Broken department resources anchor')
    events=LH.parse(str(D/(prefix+'events.html')))
    if len(events.xpath('//*[@data-event-state]'))<1:errors.append(prefix+'Calendar status fallback missing')

# Boundary cases: Taiwan midnight, same-day and multi-day events, completed range.
node=shutil.which('node')
if not node:
    errors.append('Node is required for calendar boundary checks')
else:
    code="""const assert=require('node:assert/strict');const api=require('./dist/assets/calendar-date.js');
assert.deepEqual(api.parts(new Date('2026-11-07T15:59:59Z')),{year:2026,month:11,day:7});
assert.deepEqual(api.parts(new Date('2026-11-07T16:00:00Z')),{year:2026,month:11,day:8});
const e={start:'2026-11-09',end:'2026-11-15'};
for(const [day,expected] of [['2026-11-08','upcoming'],['2026-11-09','ongoing'],['2026-11-15','ongoing'],['2026-11-16','completed']])assert.equal(api.eventState(e,day),expected);
assert.equal(api.eventState({start:'2026-11-08',end:'2026-11-08'},'2026-11-08'),'ongoing');
console.log('Taiwan date and calendar state boundaries passed');"""
    result=subprocess.run([node,'-e',code],cwd=ROOT,capture_output=True,text=True)
    if result.returncode:errors.append(result.stderr)

report={'certificate_records_per_language':len(expected),'languages':2,'calendar_boundary_cases':7,'errors':errors}
(ROOT/'information-design-check-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
