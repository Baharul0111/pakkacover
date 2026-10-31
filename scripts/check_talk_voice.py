#!/usr/bin/env python3
"""Live synthetic identity/measurement voice probe; no audio/transcripts on disk."""
import asyncio,json,sys,time
from pathlib import Path
import httpx
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from apps.api.app import gateway as gw
from apps.api.app.db import engine
async def main():
 began=time.monotonic();report={'synthetic':True,'steps':[]};base='http://127.0.0.1:8000'
 async with httpx.AsyncClient(timeout=25) as c:
  fresh=(await c.post(base+'/api/session',json={'lang':'hi'})).json();jid=fresh['journey_id'];headers={'Authorization':'Bearer '+fresh['token']};root=base+'/api/journeys/'+jid
  await c.post(root+'/consent',headers=headers,json={'disclosure':True,'alerts':True,'audit':True})
  for key,utterance,expected in [('relation','मेरी माँ','mother'),('attestation',None,'I agree'),('name','सुनीता','सुनीता'),('age','उनकी उम्र बावन साल है','52'),('sex','महिला','F'),('height','पाँच फुट दो इंच','157'),('weight','अड़सठ किलो','68')]:
   view=(await c.get(root,headers=headers)).json()
   if view['node']['key']!=key:report['steps'].append({'key':key,'passed':False,'reason':'unexpected_node'});break
   spoken_question=await c.post(root+'/speak',headers=headers,json={})
   if utterance is None:
    response=await c.post(root+'/answer',headers=headers,json={'text':'I agree'})
   else:
    audio,mime=await gw.speak(utterance,'hi')
    response=await c.post(root+'/voice',headers=headers,files={'audio':('synthetic.wav',audio,'audio/wav')},data={'duration':'6'})
    del audio
   view=(await c.get(root,headers=headers)).json();actual=view['slots'].get(key)
   # One replay is the same explicit answer; never substitute a guessed value.
   attempts=1
   correct=actual in ('सुनीता','Sunita','सुनिता') if key=='name' else actual==expected
   if utterance is not None and (not response.json().get('accepted') or not correct) and view['node']['key']==key:
    attempts=2;audio,mime=await gw.speak(utterance,'hi')
    response=await c.post(root+'/voice',headers=headers,files={'audio':('synthetic.wav',audio,'audio/wav')},data={'duration':'6'})
    del audio
    view=(await c.get(root,headers=headers)).json();actual=view['slots'].get(key)
   correct=actual in ('सुनीता','Sunita','सुनिता') if key=='name' else actual==expected
   report['steps'].append({'key':key,'question_audio':spoken_question.status_code==200 and bool(spoken_question.content),'attempts':attempts,'accepted':response.status_code==200 and response.json().get('accepted',False),'preserved':correct,'passed':bool(correct and response.status_code==200 and response.json().get('accepted'))})
   if not correct:break
  report['passed']=len(report['steps'])==7 and all(row['passed'] and row.get('question_audio') for row in report['steps'])
  # Discard only this probe journey. It has no saved policy/payment data.
  await c.post(root+'/reset',headers=headers)
 await engine.dispose();report['seconds']=round(time.monotonic()-began,2)
 (ROOT/'evals/results/talk-voice.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':asyncio.run(main())
