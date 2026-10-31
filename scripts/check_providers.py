#!/usr/bin/env python3
"""Small synthetic provider smoke. Never outputs keys, audio or transcribed text."""
import asyncio,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from apps.api.app import gateway as gw,interview
from apps.api.app.db import engine
async def run():
 report={'models':await gw.discover_models()}
 node={'key':'conditions','en':'Any doctor-diagnosed condition?','choices':[]}
 vals,model=await interview.extract(node,'Meri mummy ko BP hai, doctor ne bataya hai.')
 report['slot_extraction']={'passed':interview.canonical_condition(vals.get('conditions',''))=='hypertension','returned_model':model}
 try:
  audio,mime=await gw.speak('मेरी उम्र बावन साल है।','hi')
  report['tts']={'passed':len(audio)>100,'bytes':len(audio),'mime':mime}
  transcript=await gw.transcribe(audio,'audio/wav',4)
  report['stt']={'passed':'52' in gw.number_tokens(transcript),'model':gw.STT_MODEL}
  del audio,transcript
 except gw.Unavailable as e:report['speech']={'passed':False,'reason':str(e)}
 report['usage']=await gw.usage_status()
 (ROOT/'evals/results/provider-smoke.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
 await engine.dispose()
asyncio.run(run())
