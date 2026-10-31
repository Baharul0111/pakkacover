#!/usr/bin/env python3
"""Synthetic voice-path diagnosis; reports only metadata, not health text or recordings."""
import asyncio,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from apps.api.app import gateway as gw,interview
from apps.api.app.media import media
from apps.api.app.db import engine
async def run():
 await gw.discover_models();out={};start=time.monotonic()
 try:
  audio,_=await gw.speak('मेरी माँ को बीपी है। डॉक्टर ने बताया है।','hi');out['tts_bytes']=len(audio)
  try:measured=await media.call('audio',audio);out['measured_seconds']=round(measured,2)
  except Exception as e:out['media_error']=type(e).__name__+':'+str(e);measured=6
  transcript=await gw.transcribe(audio,'audio/wav',measured);out['transcript_present']=bool(transcript);out['recognized_bp_alias']=interview.canonical_condition(transcript)=='hypertension'
  values,source=await interview.extract({'key':'conditions','en':'Has a doctor told you about any illness?','choices':['BP / hypertension','Diabetes','None','Other / not sure']},transcript)
  out['extracted']=bool(values);out['source']=source;out['correct_condition']=interview.canonical_condition(values.get('conditions',''))=='hypertension'
 except Exception as e:out['error_type']=type(e).__name__;out['error_code']=str(e)
 finally:media.close();await engine.dispose()
 out['seconds']=round(time.monotonic()-start,2);(ROOT/'evals/results/voice-path.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':asyncio.run(run())
