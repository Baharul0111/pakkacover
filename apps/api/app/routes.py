from __future__ import annotations
import asyncio,hashlib,hmac,secrets
from datetime import date,timedelta
from fastapi import APIRouter,Depends,HTTPException,Header,UploadFile,File,Form,Response,Request
from pydantic import BaseModel,Field,ConfigDict
from sqlalchemy import select,delete
from apps.api.app.config import get,fernet
from apps.api.app.db import Session,Journey,AuthToken,Consent,Line,AdvisorRequest,now,Idempotency
from apps.api.app.repo import principal,owned
from apps.api.app import gateway as gw,interview as fsm
from apps.api.app.engine.rules import plans,simulate,promise
router=APIRouter(prefix='/api')
class Body(BaseModel):model_config=ConfigDict(extra='forbid')
class SessionIn(Body):lang:str='hi'
class ConsentIn(Body):
 disclosure:bool
 alerts:bool=False
 audit:bool=False
class MemberIn(Body):
 name:str=Field(default="",max_length=80)
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
  identity=f'{body.name or "Member 1"} · {body.age} · {body.sex}'
  s.add(Line(journey_id=owner,slot='member',payload={'key':'member','value':identity,'text_en':'Name, age and sex: '+identity,'text_hi':'नाम, उम्र और लिंग: '+identity,'ai_guess':False,'source':'manual'}))
  s.add(Consent(journey_id=owner,purpose='P1_member_attest',granted=True));await s.commit()
 return await get_journey(jid,owner)

async def answer_core(jid,body,owner,idempotency,input_source='typed'):
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
  if input_source=='voice':source='voice:'+source
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
   from apps.api.app.media import media
   measured=await media.call('audio',data)
   transcript=await gw.transcribe(data,mime,measured)
   if not transcript:raise gw.Unavailable('empty_transcript')
   result=await answer_core(jid,AnswerIn(text=transcript),owner,None,'voice')
   result['transcript']=transcript
 except (gw.Unavailable,ValueError,TimeoutError):result={'accepted':False,'fallback':'Voice unavailable. Tap an answer or type; your progress is safe.'}
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
  if line.slot=='member':
   await s.execute(delete(Line).where(Line.journey_id==owner))
   j.payload={'slots':{}};await s.commit();return {'status':'reopened','node':'member'}
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

@router.post('/journeys/{jid}/photo')
async def photo(jid:str,owner=Depends(principal),image:UploadFile=File(...),idempotency_key:str|None=Header(default=None,max_length=50)):
 from apps.api.app.medicine import read_strip
 await require_consented(owner)
 async with Session() as s:
  j=await owned(s,Journey,jid,owner)
  if idempotency_key:
   prior=await s.get(Idempotency,owner+':photo:'+idempotency_key)
   if prior:return prior.payload
  if fsm.next_node(j.payload)['key']!='medicine':raise HTTPException(409,'Photo capture belongs to the medicine question')
 data=await image.read(5*1024*1024+1);await image.close()
 if len(data)>5*1024*1024:raise HTTPException(413,'Photo is too large')
 try:
  async with asyncio.timeout(25):result=await read_strip(data)
 except (gw.Unavailable,ValueError,TimeoutError):result={'status':'manual','candidates':[],'readings':[],'must_ask_indication':True,'message':'Could not read this photo. Please type the printed name and strength.'}
 finally:del data
 async with Session() as s:
  j=await owned(s,Journey,jid,owner,True);j.payload={**j.payload,'medicine_proposal':result}
  if idempotency_key:s.add(Idempotency(key=owner+':photo:'+idempotency_key,journey_id=owner,payload=result))
  await s.commit()
 return result
class MedicineChoice(Body):candidate:int=Field(ge=0,le=1)
@router.post('/journeys/{jid}/medicine/choose')
async def medicine_choose(jid:str,body:MedicineChoice,owner=Depends(principal)):
 async with Session() as s:
  j=await owned(s,Journey,jid,owner,True)
  proposal=j.payload.get('medicine_proposal',{});candidates=proposal.get('candidates',[])
  if body.candidate>=len(candidates):raise HTTPException(422,'Choose a printed reading or type it yourself')
  chosen=candidates[body.candidate];value=f'{chosen["generic"]} {chosen["strength"]}'.strip()
  slots={**j.payload.get('slots',{}),'medicine':value};slots.pop('indication',None)
  j.payload={**j.payload,'slots':slots,'medicine_proposal':None,'selection':None}
  line=await s.scalar(select(Line).where(Line.journey_id==owner,Line.slot=='medicine'))
  payload=fsm.line_payload('medicine',value,j.payload['member'],'two_readers_buyer_choice')
  if line:line.payload=payload;line.confirmed=False;line.version+=1
  else:s.add(Line(journey_id=owner,slot='medicine',payload=payload))
  await s.commit()
 return {'accepted':True,'node':fsm.next_node(j.payload),'condition_choices':['BP / hypertension','Heart','Kidney','I do not know']}

class LanguageIn(Body):lang:str=Field(pattern='^(hi|en)$')
@router.post('/journeys/{jid}/language')
async def language(jid:str,body:LanguageIn,owner=Depends(principal)):
 async with Session() as s:
  j=await owned(s,Journey,jid,owner);j.lang=body.lang;await s.commit()
 return {'lang':body.lang}

@router.post('/journeys/{jid}/audit')
async def audit_policy(jid:str,owner=Depends(principal),policy:UploadFile|None=File(default=None),variant:str|None=Form(default=None)):
 from apps.api.app.audit import audit_pdf
 from apps.api.app.sample_policy import make_policy,VARIANTS
 from apps.api.app.db import AuditRun
 if jid!=owner:raise HTTPException(404,'Not found')
 await require_consented(owner,'P3_audit')
 j,lines=await confirmed_context(owner)
 if not j.saved:raise HTTPException(409,'Save with the demo passphrase before checking a policy')
 selection=j.payload.get('selection')
 if not selection:raise HTTPException(409,'Choose a sample plan first')
 context={'member':j.payload['member'],'selection':selection,'conditions':fsm.confirmed_conditions(lines)}
 if policy:
  data=await policy.read(10*1024*1024+1);await policy.close()
  if len(data)>10*1024*1024:raise HTTPException(413,'PDF is too large')
  if not data.startswith(b'%PDF-'):raise HTTPException(415,'Please choose a PDF')
  generated=False
 else:
  if variant not in VARIANTS:raise HTTPException(422,'Choose a valid sample variant')
  data=make_policy(plans()[selection['plan_id']],context['member'],context['conditions'],date.fromisoformat(selection['d0']),variant);generated=True
 digest=hashlib.sha256(data).hexdigest()
 try:result=await audit_pdf(data,context,generated)
 except (ValueError,TimeoutError):
  result={'flags':[{'key':'document','status':'check_manually','title':'Please check this PDF manually','title_hi':'कृपया यह पीडीएफ खुद जाँचें','expected_quote':'Your confirmed declaration and Promise Card','actual_quote':'The PDF could not be safely read.','impact':'Use a text PDF or ask the advisor to compare the fields.','impact_hi':'टेक्स्ट वाली पीडीएफ दें या सलाहकार से क्षेत्रों की तुलना करवाएं।'}],'matches':[],'verified_field_count':0,'extraction_mode':'manual_required','extracted':{}}
 finally:del data
 result['free_look_last_day']=(date.fromisoformat(selection['receipt'])+timedelta(days=plans()[selection['plan_id']].free_look.value-1)).isoformat()
 async with Session() as s:
  record=AuditRun(journey_id=owner,pdf_sha=digest,payload=result);s.add(record);await s.commit()
 return result

def payment_view(row):
 return {'mode':row.mode,'order_id':row.order_id,'amount':'1.00','status':row.status,'verified':False,'paid_at':row.paid_at.isoformat() if row.paid_at else None,'label':'Demo'}
def notification_view(row):
 return {'id':row.id,'order_id':row.order_id,'title':'Paytm','body':f'₹1 paid for your health cover · Order {row.order_id}','created_at':row.created_at.isoformat(),'read':row.read,'mode':'demo'}
@router.post('/journeys/{jid}/pay/initiate')
async def pay_initiate(jid:str,owner=Depends(principal)):
 from apps.api.app.payments import ADAPTER
 from apps.api.app.db import Payment,uid
 if jid!=owner:raise HTTPException(404,'Not found')
 if not (await gw.flags())['payments']:raise HTTPException(503,'Demo payments are switched off')
 j,lines=await confirmed_context(owner)
 if not j.saved or not j.payload.get('selection'):raise HTTPException(409,'Save your Promise Card first')
 async with Session() as s:
  row=Payment(journey_id=owner,order_id='PC'+uid(),mode='demo');s.add(row);await s.commit()
 return await ADAPTER.initiate(row.order_id,owner)
async def payment_row(s,order_id,owner):
 from apps.api.app.db import Payment
 row=await s.scalar(select(Payment).where(Payment.order_id==order_id,Payment.journey_id==owner).with_for_update())
 if not row:raise HTTPException(404,'Not found')
 return row
class CompletePaymentIn(Body):
 method:str=Field(pattern='^(UPI|Wallet|Card)$')
@router.post('/journeys/{jid}/pay/{order_id}/complete')
async def complete_payment(jid:str,order_id:str,body:CompletePaymentIn,owner=Depends(principal)):
 from apps.api.app.db import Notification
 if jid!=owner:raise HTTPException(404,'Not found')
 if not (await gw.flags())['payments']:raise HTTPException(503,'Demo payments are switched off')
 async with Session() as s:
  row=await payment_row(s,order_id,owner)
  if row.mode!='demo':raise HTTPException(409,'Start a new demo order')
  if row.status!='PAID':
   row.status='PAID';row.verified=False;row.paid_at=now()
   notice=Notification(journey_id=owner,order_id=order_id);s.add(notice);await s.flush()
  else:notice=await s.scalar(select(Notification).where(Notification.order_id==order_id,Notification.journey_id==owner))
  await s.commit();result=payment_view(row);result['notification']=notification_view(notice)
 return result
@router.post('/journeys/{jid}/pay/{order_id}/status')
async def payment_status(jid:str,order_id:str,owner=Depends(principal)):
 if jid!=owner:raise HTTPException(404,'Not found')
 async with Session() as s:return payment_view(await payment_row(s,order_id,owner))
@router.get('/journeys/{jid}/notifications')
async def notifications(jid:str,owner=Depends(principal)):
 from apps.api.app.db import Notification
 async with Session() as s:
  await owned(s,Journey,jid,owner)
  rows=(await s.scalars(select(Notification).where(Notification.journey_id==owner).order_by(Notification.created_at.desc()))).all()
 return [notification_view(row) for row in rows]
@router.post('/journeys/{jid}/notifications/read')
async def read_notifications(jid:str,owner=Depends(principal)):
 from apps.api.app.db import Notification
 from sqlalchemy import update
 async with Session() as s:
  await owned(s,Journey,jid,owner)
  await s.execute(update(Notification).where(Notification.journey_id==owner).values(read=True));await s.commit()
 return {'read':True}
@router.post('/journeys/{jid}/reset')
async def reset_demo(jid:str,owner=Depends(principal)):
 # Remove only this browser's journey. Provider spend is deliberately retained.
 async with Session() as s:
  old=await owned(s,Journey,jid,owner,True);lang=old.lang
  await s.execute(delete(AuthToken).where(AuthToken.journey_id==owner));await s.delete(old)
  token=secrets.token_urlsafe(32);j=Journey(lang=lang,payload={'slots':{}});s.add(j);await s.flush()
  s.add(AuthToken(token_hash=hashlib.sha256(token.encode()).hexdigest(),journey_id=j.id,expires_at=now()+timedelta(hours=24)));await s.commit()
 return {'token':token,'journey_id':j.id}
@router.get('/journeys/{jid}/calendar')
async def calendar(jid:str,owner=Depends(principal)):
 await require_consented(owner,'P2_alerts');result=await card(jid,owner)
 # Dates come only from the rules engine; no health details enter calendar text.
 lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//PakkaCover//Demo//EN','CALSCALE:GREGORIAN']
 for index,row in enumerate(result['rows']):
  d=date.fromisoformat(row['fact'].value)
  lines+=['BEGIN:VEVENT',f'UID:{jid}-{index}@pakkacover',f'DTSTAMP:{now().strftime("%Y%m%dT%H%M%SZ")}',f'DTSTART;VALUE=DATE:{d.strftime("%Y%m%d")}',f'DTEND;VALUE=DATE:{(d+timedelta(days=1)).strftime("%Y%m%d")}', 'SUMMARY:PakkaCover - review your cover date','END:VEVENT']
 lines+=['END:VCALENDAR']
 return Response('\r\n'.join(lines)+'\r\n',media_type='text/calendar',headers={'Content-Disposition':'attachment; filename="pakkacover-dates.ics"'})

class ManualAuditIn(Body):
 fields:dict[str,str]
 checked:bool
@router.post('/journeys/{jid}/audit/manual')
async def manual_audit(jid:str,body:ManualAuditIn,owner=Depends(principal)):
 from apps.api.app.audit import compare,FieldValue,FIELDS
 from apps.api.app.db import AuditRun
 if jid!=owner:raise HTTPException(404,'Not found')
 await require_consented(owner,'P3_audit');j,lines=await confirmed_context(owner)
 if not j.saved or not j.payload.get('selection'):raise HTTPException(409,'Save your Promise Card first')
 if not body.checked or not body.fields or set(body.fields)-set(FIELDS) or any(not v.strip() or len(v)>500 for v in body.fields.values()):raise HTTPException(422,'Enter policy fields and confirm you checked them')
 context={'member':j.payload['member'],'selection':j.payload['selection'],'conditions':fsm.confirmed_conditions(lines)}
 # Manual inputs are explicitly human-confirmed, never presented as AI/PDF-verified quotes.
 fields={k:FieldValue(key=k,found=True,value=v.strip(),page=0,quote=f'Buyer-checked manual entry — {FIELDS[k]}: {v.strip()}') for k,v in body.fields.items()}
 result=compare(fields,context);result['extraction_mode']='buyer_checked_manual';result['extracted']={k:f.model_dump() for k,f in fields.items()}
 result['free_look_last_day']=(date.fromisoformat(context['selection']['receipt'])+timedelta(days=plans()[context['selection']['plan_id']].free_look.value-1)).isoformat()
 digest=hashlib.sha256(str(body.fields).encode()).hexdigest()
 async with Session() as s:s.add(AuditRun(journey_id=owner,pdf_sha=digest,payload=result));await s.commit()
 return result
