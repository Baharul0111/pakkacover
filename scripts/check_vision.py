#!/usr/bin/env python3
"""Live synthetic OCR smoke; real user strips remain a separate golden-set gate."""
import asyncio,json,sys
from pathlib import Path
from io import BytesIO
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from apps.api.app import gateway as gw
from apps.api.app.medicine import read_strip
from apps.api.app.media import media
from apps.api.app.db import engine
async def run():
 await gw.discover_models();report={}
 try:
  for name in ['printed','blank']:
   img=Image.new('RGB',(1000,500),'white')
   if name=='printed':
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',48)
    ImageDraw.Draw(img).multiline_text((40,50),'TELMA 40\nTelmisartan Tablets IP\nEach tablet contains:\nTelmisartan 40 mg',font=font,fill='black',spacing=20)
   buffer=BytesIO();img.save(buffer,format='JPEG')
   try:
    result=await read_strip(buffer.getvalue())
    ok=(result['status']=='agree' and all(r['generic']=='Telmisartan' for r in result['candidates'])) if name=='printed' else not result['candidates']
    report[name]={'passed':ok,'status':result['status'],'candidate_count':len(result['candidates']),'requires_buyer_indication':result['must_ask_indication']}
   except Exception as e:report[name]={'passed':False,'error_type':type(e).__name__}
 finally:media.close();await engine.dispose()
 (ROOT/'evals/results/vision-smoke.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':asyncio.run(run())
