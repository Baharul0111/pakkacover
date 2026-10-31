#!/usr/bin/env python3
"""Run browser QA with secrets only in the child environment, never stdout or argv."""
import os,subprocess,sys,time,asyncio,base64
import httpx
from pathlib import Path
from dotenv import dotenv_values
ROOT=Path(__file__).resolve().parents[1]
env={**os.environ,**{k:v for k,v in dotenv_values(ROOT/'.env').items() if v is not None}}
if '--live-voice' in sys.argv:
 sys.path.insert(0,str(ROOT))
 from apps.api.app import gateway as gw
 from apps.api.app.db import engine
 async def make_audio():
  audio,_=await gw.speak('मेरी माँ को बीपी है। डॉक्टर ने बताया है।','hi')
  await engine.dispose();return audio
 env['PCC_E2E_AUDIO_B64']=base64.b64encode(asyncio.run(make_audio())).decode()
base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000'
for _ in range(40):
 try:
  if httpx.get(base+'/health',timeout=2).status_code==200:break
 except httpx.HTTPError:pass
 time.sleep(.5)
raise SystemExit(subprocess.call(['node',str(ROOT/'apps/web/e2e.mjs'),*sys.argv[1:]],cwd=ROOT,env=env))
