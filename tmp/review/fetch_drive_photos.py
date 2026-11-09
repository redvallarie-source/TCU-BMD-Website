from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen,Request
from PIL import Image
from io import BytesIO
import json

target=Path(__file__).parent/'drive-sources'
target.mkdir(exist_ok=True)
photos=json.loads((Path(__file__).parent/'drive-selection.json').read_text(encoding='utf-8'))
def fetch(p):
    path=target/(p['slot']+'.jpg')
    if path.exists():
        return {'slot':p['slot'],'path':str(path),'existing':True}
    if p.get('local_source'):
        data=Path(p['local_source']).read_bytes()
        Image.open(BytesIO(data)).verify()
        path.write_bytes(data)
        return {'slot':p['slot'],'path':str(path),'bytes':len(data)}
    url='https://drive.google.com/uc?export=download&id='+p['file_id']
    with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as response:
        data=response.read()
    im=Image.open(BytesIO(data));im.verify()
    path.write_bytes(data)
    return {'slot':p['slot'],'path':str(path),'bytes':len(data)}
with ThreadPoolExecutor(max_workers=3) as pool:
    for result in pool.map(fetch,photos):print(json.dumps(result),flush=True)
