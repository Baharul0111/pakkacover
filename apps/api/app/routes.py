from __future__ import annotations
import asyncio,hashlib,hmac,secrets
from datetime import date,timedelta
from fastapi import APIRouter,Depends,HTTPException,Header,UploadFile,File,Form,Response
from pydantic import BaseModel,Field,ConfigDict
from sqlalchemy import select,delete
from apps.api.app.config import get,fernet
from apps.api.app.db import Session,Journey,AuthToken,Consent,Line,AdvisorRequest,now,Idempotency
from apps.api.app.repo import principal,owned
from apps.api.app import gateway as gw,interview as fsm
from apps.api.app.engine.rules import plans,simulate,promise
router=APIRouter(prefix='/v1')
class Body(BaseModel):model_config=ConfigDict(extra='forbid')
class SessionIn(Body):lang:str='hi'
class ConsentIn(Body):
 disclosure:bool
 alerts:bool=False
 audit:bool=False
class MemberIn(Body):
 age:int=Field(ge=0,le=120)
 sex:str=Field(pattern='^(F|M|Other)$')
 relation:str=Field(min_length=1,max_length=32)
 attested:bool
 guardian:bool=False
class AnswerIn(Body):text:str=Field(min_length=1,max_length=1000)
class LoginIn(Body):passphrase:str=Field(min_length=1,max_length=256)
class SelectIn(Body):
 plan_id:str
 d0:date
 receipt:date
class ScenarioIn(Body):
 d0:date=date(2026,10,31)
 illness:int=Field(default=200000,ge=0,le=10000000)
 accident:int=Field(default=100000,ge=0,le=10000000)
 cataract:int=Field(default=60000,ge=0,le=10000000)
class ConfirmIn(Body):version:int=Field(ge=1)

def check_passphrase(value):
 if not value or not hmac.compare_digest(value,get('DEMO_LOGIN_PASSPHRASE')):raise HTTPException(403,'Incorrect demo passphrase')
async def require_consented(j,purpose='P1_disclosure'):
 async with Session() as s:
  consent=await s.scalar(select(Consent).where(Consent.journey_id==j,Consent.purpose==purpose,Consent.granted.is_(True)))
 if not consent:raise HTTPException(409,'Please give the relevant consent first')
async def view(j,lines):
 payload=j.payload or {}
 return {'id':j.id,'lang':j.lang,'saved':j.saved,'member':payload.get('member'),'node':fsm.next_node(payload),'slots':payload.get('slots',{}),'lines':[{'id':l.id,'version':l.version,'confirmed':l.confirmed,**l.payload} for l in lines],'selection':payload.get('selection'),'medicine':payload.get('medicine_proposal')}
@router.post('/session')
async def create_session(body:SessionIn):
 if not (await gw.flags())['new_sessions']:raise HTTPException(503,'Demo intake is paused')
 token=secrets.token_urlsafe(32)
 async with Session() as s:
  j=Journey(lang='hi' if body.lang=='hi' else 'en',payload={'slots':{}});s.add(j);await s.flush()
  s.add(AuthToken(token_hash=hashlib.sha256(token.encode()).hexdigest(),journey_id=j.id,expires_at=now()+timedelta(hours=24)));await s.commit()
 return {'token':token,'journey_id':j.id}
@router.get('/journeys/{jid}')
async def get_journey(jid:str,owner=Depends(principal)):
 async with Session() as s:
  j=await owned(s,Journey,jid,owner);lines=(await s.scalars(select(Line).where(Line.journey_id==owner).order_by(Line.id))).all()
 return await view(j,lines)
@router.post('/journeys/{jid}/consent')
async def consent(jid:str,body:ConsentIn,owner=Depends(principal)):
 if not body.disclosure:raise HTTPException(422,'Disclosure consent is required to proceed')
 async with Session() as s:
  await owned(s,Journey,jid,owner)
  for purpose,granted in [('P1_disclosure',body.disclosure),('P2_alerts',body.alerts),('P3_audit',body.audit)]:
   s.add(Consent(journey_id=owner,purpose=purpose,granted=granted))
  await s.commit()
 return {'status':'recorded'}
@router.post('/journeys/{jid}/member')
async def member(jid:str,body:MemberIn,owner=Depends(principal)):
 await require_consented(owner)
 if not body.attested or (body.age<18 and not body.guardian):raise HTTPException(422,'Member agreement / guardian attestation is required')
 async with Session() as s:
  j=await owned(s,Journey,jid,owner,True)
  if j.payload.get('member'):raise HTTPException(409,'Member already exists; start a fresh demo for another family')
  j.payload={**j.payload,'member':body.model_dump()}
  s.add(Consent(journey_id=owner,purpose='P1_member_attest',granted=True));await s.commit()
 return await get_journey(jid,owner)

async def answer_core(jid,body,owner,idempotency):
 await require_consented(owner)
 # Keep external I/O outside the DB transaction; version/node is rechecked afterwards.
 async with Session() as s:
  j=await owned(s,Journey,jid,owner)
  if idempotency:
   old=await s.get(Idempotency,owner+':'+idempotency)
   if old:return old.payload
  node=fsm.next_node(j.payload)
  if node['key'] in ('member','review'):raise HTTPException(409,'Finish the member form or review the lines')
 try:
  async with asyncio.timeout(8):vals,source=await fsm.extract(node,body.text)
 except TimeoutError:vals,source={},'deadline'
 async with Session() as s:
  j=await owned(s,Journey,jid,owner,True)
  if fsm.next_node(j.payload)['key']!=node['key']:raise HTTPException(409,'Question changed; refresh your session')
  if vals:
   j.payload={**j.payload,'slots':{**j.payload.get('slots',{}),**vals}}
   for k,v in vals.items():
    existing=await s.scalar(select(Line).where(Line.journey_id==owner,Line.slot==k))
    if existing:
     existing.payload=fsm.line_payload(k,v,j.payload['member'],source);existing.confirmed=False;existing.version+=1
    else:s.add(Line(journey_id=owner,slot=k,payload=fsm.line_payload(k,v,j.payload['member'],source)))
  result={'accepted':bool(vals),'source':source,'node':fsm.next_node(j.payload),'fallback':None if vals else 'Please tap an answer or type the details again.'}
  if idempotency:s.add(Idempotency(key=owner+':'+idempotency,journey_id=owner,payload=result))
  await s.commit()
 return result
@router.post('/journeys/{jid}/answer')
async def answer(jid:str,body:AnswerIn,owner=Depends(principal),idempotency_key:str|None=Header(default=None,max_length=50)):
 return await answer_core(jid,body,owner,idempotency_key)
@router.post('/journeys/{jid}/voice')
async def voice(jid:str,owner=Depends(principal),audio:UploadFile=File(...),duration:float=Form(...),idempotency_key:str|None=Header(default=None,max_length=50)):
 await require_consented(owner)
 async with Session() as s:
  await owned(s,Journey,jid,owner)
  if idempotency_key:
   previous=await s.get(Idempotency,owner+':voice:'+idempotency_key)
   if previous:return previous.payload
 if not 0<duration<=25:raise HTTPException(422,'Record for at most 25 seconds')
 mime=(audio.content_type or '').split(';')[0]
 if mime not in ('audio/webm','audio/ogg','audio/mp4','audio/wav','audio/x-m4a'):raise HTTPException(415,'Unsupported audio format')
 data=await audio.read(1024*1024+1);await audio.close()
 if len(data)>1024*1024:raise HTTPException(413,'Audio is too large')
 try:
  async with asyncio.timeout(12):
   transcript=await gw.transcribe(data,mime,duration)
   if not transcript:raise gw.Unavailable('empty_transcript')
   result=await answer_core(jid,AnswerIn(text=transcript),owner,None)
   result['transcript']=transcript
 except (gw.Unavailable,TimeoutError):result={'accepted':False,'fallback':'Voice unavailable. Tap an answer or type; your progress is safe.'}
 finally:del data
 if idempotency_key:
  async with Session() as s:
   s.add(Idempotency(key=owner+':voice:'+idempotency_key,journey_id=owner,payload=result));await s.commit()
 return result
class TTSIn(Body):
 node:str|None=None
 line_id:str|None=None
@router.post('/journeys/{jid}/speak')
async def speak(jid:str,body:TTSIn,owner=Depends(principal)):
 async with Session() as s:
  j=await owned(s,Journey,jid,owner)
  if body.line_id:
   l=await owned(s,Line,body.line_id,owner);text=l.payload['text_hi' if j.lang=='hi' else 'text_en']
  else:
   node=fsm.next_node(j.payload)
   text=node['hi' if j.lang=='hi' else 'en']
 try:
  data,mime=await gw.speak(text,j.lang);return Response(data,media_type=mime,headers={'Cache-Control':'no-store'})
 except gw.Unavailable:return Response(status_code=204)
@router.post('/lines/{lid}/confirm')
async def confirm(lid:str,body:ConfirmIn,owner=Depends(principal)):
 async with Session() as s:
  line=await owned(s,Line,lid,owner,True)
  if line.version!=body.version:raise HTTPException(409,'This line changed; review it again')
  line.confirmed=True;await s.commit()
 return {'confirmed':True}
@router.post('/lines/{lid}/reopen')
async def reopen(lid:str,owner=Depends(principal)):
 async with Session() as s:
  line=await owned(s,Line,lid,owner,True);line.confirmed=False;line.version+=1
  j=await owned(s,Journey,owner,owner,True)
  slots=dict(j.payload.get('slots',{}));slots.pop(line.slot,None)
  j.payload={**j.payload,'slots':slots,'selection':None}
  # The next answer updates this same card and preserves the version check.
  await s.commit()
 return {'status':'reopened'}
async def confirmed_context(owner):
 async with Session() as s:
  j=await owned(s,Journey,owner,owner)
  lines=(await s.scalars(select(Line).where(Line.journey_id==owner))).all()
 if fsm.next_node(j.payload)['key']!='review' or not lines or any(not l.confirmed for l in lines):raise HTTPException(409,'Confirm every declaration line individually first')
 return j,lines
@router.post('/journeys/{jid}/simulate')
async def simulation(jid:str,body:ScenarioIn,owner=Depends(principal)):
 if jid!=owner:raise HTTPException(404,'Not found')
 j,lines=await confirmed_context(owner)
 return simulate(body.d0,fsm.confirmed_conditions(lines),j.payload['member']['age'],body.model_dump(exclude={'d0'}))
@router.post('/journeys/{jid}/select')
async def select_plan(jid:str,body:SelectIn,owner=Depends(principal)):
 if jid!=owner:raise HTTPException(404,'Not found')
 j,lines=await confirmed_context(owner)
 if body.plan_id not in plans():raise HTTPException(422,'Unknown sample plan')
 async with Session() as s:
  j=await owned(s,Journey,jid,owner,True);j.payload={**j.payload,'selection':body.model_dump(mode='json')};await s.commit()
 return await card(jid,owner)
@router.get('/journeys/{jid}/card')
async def card(jid:str,owner=Depends(principal)):
 if jid!=owner:raise HTTPException(404,'Not found')
 j,lines=await confirmed_context(owner);selection=j.payload.get('selection')
 if not selection:raise HTTPException(409,'Choose a sample plan first')
 plan=plans()[selection['plan_id']]
 rows=promise(plan,date.fromisoformat(selection['d0']),date.fromisoformat(selection['receipt']),fsm.confirmed_conditions(lines))
 return {'plan_id':plan.plan_id,'product_name':plan.product_name,'sample_notice':plan.sample_notice,'rows':rows,'exclusions':plan.exclusions,'exclusion_clause':plan.exclusion_clause,'upcoming':sorted(rows,key=lambda r:r['fact'].value)}
@router.post('/journeys/{jid}/save')
async def save(jid:str,body:LoginIn,owner=Depends(principal)):
 check_passphrase(body.passphrase)
 async with Session() as s:
  j=await owned(s,Journey,jid,owner);j.saved=True;await s.commit()
 return {'saved':True,'message':'Saved for this demo session. Keep this browser tab.'}
@router.post('/journeys/{jid}/advisor')
async def advisor(jid:str,owner=Depends(principal)):
 async with Session() as s:
  j=await owned(s,Journey,jid,owner)
  req=AdvisorRequest(journey_id=owner,payload={'member':j.payload.get('member'),'slots':j.payload.get('slots',{}),'selection':j.payload.get('selection')});s.add(req);await s.commit()
 return {'request_id':req.id,'label':'Pilot callback within 24 h','message':'Callback request recorded for the demo operator; no licensed advisor partner is connected in this hackathon demo.'}
@router.get('/switches')
async def switches():return await gw.flags()
class SwitchIn(Body):
 changes:dict[str,bool]
@router.post('/switches')
async def change_switches(body:SwitchIn,x_demo_passphrase:str=Header(default='')):
 check_passphrase(x_demo_passphrase);await gw.set_flags(body.changes);return await gw.flags()
@router.get('/usage')
async def usage(x_demo_passphrase:str=Header(default='')):
 check_passphrase(x_demo_passphrase);return await gw.usage_status()
