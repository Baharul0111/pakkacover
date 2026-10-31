"""Bounded, schema-only model gateway; no tools, raw input logging, or counting."""
from __future__ import annotations
import asyncio,base64,hashlib,json,re,ssl,unicodedata,time
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import httpx,truststore
from sqlalchemy import select,func,text
from fastapi import HTTPException
from apps.api.app.config import get,ROOT
from apps.api.app.db import Session,ConfigFlag,Usage

DEFAULTS={'voice_in':True,'voice_out':True,'vision_read':True,'llm_phrasing':True,'audit_llm':True,'payments':True,'vendor:openai':True,'vendor:anthropic':True,'vendor:sarvam':True,'new_sessions':True}
KEYTERMS=['BP','sugar','thyroid','Telma','Telmisartan','Amlodipine','Metformin','Thyronorm','Atorvastatin','hypertension','diabetes','kidney','heart']
MODEL_STATUS={}
CREDIT_BLOCKED_UNTIL={}
STT_MODEL=json.loads((ROOT/'models.yaml').read_text()).get('stt','saaras:v4') if (ROOT/'models.yaml').exists() else 'saaras:v4'
class Unavailable(Exception):pass

def client(timeout=8):
 return httpx.AsyncClient(timeout=httpx.Timeout(timeout,connect=min(4,timeout)),verify=truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT),follow_redirects=False)
def normal(text):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',str(text)).translate(str.maketrans('०१२३४५६७८९','0123456789'))).strip().casefold()
WORDS={'bawan':'52','बावन':'52','paanch':'5','पाँच':'5','पांच':'5','ek':'1','एक':'1','do':'2','दो':'2','teen':'3','तीन':'3','chaar':'4','चार':'4','chhe':'6','छह':'6','chaalis':'40','चालीस':'40','pachaas':'50','पचास':'50'}
def number_tokens(t):
 t=normal(t)
 for w,n in WORDS.items():t=re.sub(r'(?<!\w)'+re.escape(w)+r'(?!\w)',n,t)
 return set(re.findall(r'\d+(?:\.\d+)?',t))
def numeric_guard(candidate,source):return number_tokens(candidate)<=number_tokens(source)
def guarded_question(candidate,source,template):return candidate if numeric_guard(candidate,source) else template
async def flags():
 async with Session() as s:
  rows=(await s.scalars(select(ConfigFlag))).all()
 return {**DEFAULTS,**{r.key:r.value for r in rows}}
async def set_flags(changes):
 async with Session() as s:
  for k,v in changes.items():
   if k not in DEFAULTS:raise HTTPException(422,'Unknown switch')
   row=await s.get(ConfigFlag,k)
   if row:row.value=bool(v)
   else:s.add(ConfigFlag(key=k,value=bool(v)))
  await s.commit()
async def reserve(provider,amount,model,step):
 """Conservative reservations serialize cap checks, including in-flight calls."""
 day=datetime.now(ZoneInfo('Asia/Kolkata')).date().isoformat()
 async with Session() as s:
  await s.execute(text('SELECT pg_advisory_xact_lock(793401)'))
  total=await s.scalar(select(func.coalesce(func.sum(Usage.amount),0)))
  today=await s.scalar(select(func.coalesce(func.sum(Usage.amount),0)).where(Usage.day==day))
  sarvam=await s.scalar(select(func.coalesce(func.sum(Usage.amount),0)).where(Usage.provider=='sarvam'))
  sarvam_today=await s.scalar(select(func.coalesce(func.sum(Usage.amount),0)).where(Usage.provider=='sarvam',Usage.day==day))
  if today+amount>150:raise Unavailable('global_daily_cap')
  if provider=='sarvam':
   if sarvam_today+amount>150:raise Unavailable('sarvam_daily_cap')
   if float(get('SARVAM_BALANCE_INR','0'))-sarvam-amount<20:raise Unavailable('speech_credit_floor')
  item=Usage(day=day,provider=provider,amount=amount,model=model,step=step,outcome='reserved');s.add(item);await s.commit();return item.id
async def finish(reservation,returned_model,outcome='ok',unexecuted=False):
 async with Session() as s:
  row=await s.get(Usage,reservation)
  if row:
   row.model=returned_model;row.outcome=outcome
   if unexecuted:row.amount=0
  await s.commit()
async def usage_status():
 day=datetime.now(ZoneInfo('Asia/Kolkata')).date().isoformat()
 async with Session() as s:
  speech=await s.scalar(select(func.coalesce(func.sum(Usage.amount),0)).where(Usage.provider=='sarvam'))
  daily=await s.scalar(select(func.coalesce(func.sum(Usage.amount),0)).where(Usage.day==day))
 return {'daily_estimate_inr':round(float(daily),2),'daily_cap_inr':150,'sarvam_remaining_estimate_inr':round(float(get('SARVAM_BALANCE_INR','0'))-float(speech),2),'sarvam_floor_inr':20}
async def discover_models():
 async def one(provider,url,headers,wanted):
  try:
   async with client(8) as c:
    r=await c.get(url,headers=headers);r.raise_for_status();body=r.json()
   ids=[x['id'] for x in body.get('data',[])]
   selected={w:next((x for x in sorted(ids,reverse=True) if x==w or x.startswith(w+'-')),None) for w in wanted}
   return provider,{'status':'ok','selected':selected}
  except Exception as e:return provider,{'status':'unavailable','error_type':type(e).__name__,'selected':{}}
 pairs=await asyncio.gather(one('openai','https://api.openai.com/v1/models',{'Authorization':'Bearer '+get('OPENAI_API_KEY')},['gpt-6.1-terra','gpt-6-luna','omni-moderation-latest']),one('anthropic','https://api.anthropic.com/v1/models',{'x-api-key':get('ANTHROPIC_API_KEY'),'anthropic-version':'2023-06-01'},['claude-haiku-5-5','claude-sonnet-5-5']))
 MODEL_STATUS.clear();MODEL_STATUS.update(dict(pairs))
 (ROOT/'.run').mkdir(exist_ok=True)
 (ROOT/'.run/model_status.json').write_text(json.dumps(MODEL_STATUS,indent=2))
 return MODEL_STATUS

def pinned(provider,requested):
 model=MODEL_STATUS.get(provider,{}).get('selected',{}).get(requested)
 if not model:raise Unavailable('requested_model_not_discovered')
 return model
async def structured(provider,requested,schema,system,user,*,image=None,timeout=3.5,step='slots'):
 f=await flags()
 if not f.get('vendor:'+provider):raise Unavailable('vendor_disabled')
 if CREDIT_BLOCKED_UNTIL.get(provider,0)>time.monotonic():raise Unavailable('provider_credit_unavailable')
 model=pinned(provider,requested);reservation=await reserve(provider,(3.0 if 'sonnet' in requested else .40) if step=='audit' else (1 if image else .40),model,step)
 try:
  async with client(timeout) as c:
   if provider=='anthropic':
    content=[{'type':'text','text':user}]
    if image:content.insert(0,{'type':'image','source':{'type':'base64','media_type':'image/jpeg','data':base64.b64encode(image).decode()}})
    r=await c.post('https://api.anthropic.com/v1/messages',headers={'x-api-key':get('ANTHROPIC_API_KEY'),'anthropic-version':'2023-06-01'},json={'model':model,'max_tokens':1200,'system':system,'messages':[{'role':'user','content':content}],'output_config':{'format':{'type':'json_schema','schema':schema.model_json_schema()}}})
    r.raise_for_status();body=r.json();raw=''.join(x.get('text','') for x in body.get('content',[]) if x.get('type')=='text')
   else:
    content=[{'type':'input_text','text':user}]
    if image:content.append({'type':'input_image','image_url':'data:image/jpeg;base64,'+base64.b64encode(image).decode()})
    r=await c.post('https://api.openai.com/v1/responses',headers={'Authorization':'Bearer '+get('OPENAI_API_KEY')},json={'model':model,'store':False,'instructions':system,'input':[{'role':'user','content':content}],'max_output_tokens':1800,'reasoning':{'effort':'low'},'text':{'format':{'type':'json_schema','name':schema.__name__,'schema':schema.model_json_schema(),'strict':True}}})
    r.raise_for_status();body=r.json();raw=''.join(c.get('text','') for o in body.get('output',[]) for c in o.get('content',[]) if c.get('type')=='output_text')
   parsed=schema.model_validate_json(raw)
   CREDIT_BLOCKED_UNTIL.pop(provider,None)
   await finish(reservation,body.get('model',model));return parsed,body.get('model',model)
 except Exception as e:
  # A rejected request with insufficient provider credit never executed. Release
  # its reservation, and avoid repeated futile retries against the app's budget.
  credit=False
  if isinstance(e,httpx.HTTPStatusError) and e.response.status_code in (400,402):
   try:
    message=str(e.response.json().get('error',{}).get('message','')).casefold()
    credit='credit balance' in message or 'insufficient credit' in message
   except (ValueError,AttributeError):pass
  if credit:
   CREDIT_BLOCKED_UNTIL[provider]=time.monotonic()+60
   await finish(reservation,model,'provider_credit_unavailable',unexecuted=True)
   raise Unavailable('provider_credit_unavailable') from None
  await finish(reservation,model,type(e).__name__)
  raise Unavailable(type(e).__name__) from None
async def moderate(text_input=None,image=None):
 if not (await flags())['vendor:openai']:raise Unavailable('moderation_disabled')
 model=pinned('openai','omni-moderation-latest');payload=[]
 if text_input:payload.append({'type':'text','text':text_input})
 if image:payload.append({'type':'image_url','image_url':{'url':'data:image/jpeg;base64,'+base64.b64encode(image).decode()}})
 try:
  async with client(3) as c:
   r=await c.post('https://api.openai.com/v1/moderations',headers={'Authorization':'Bearer '+get('OPENAI_API_KEY')},json={'model':model,'input':payload});r.raise_for_status()
  if any(x.get('flagged') for x in r.json().get('results',[])):raise Unavailable('moderated')
 except Exception as e:raise Unavailable(type(e).__name__) from None
async def transcribe(audio,mime,duration,model=None):
 f=await flags()
 if not f['voice_in'] or not f['vendor:sarvam']:raise Unavailable('voice_disabled')
 model=model or STT_MODEL
 reservation=await reserve('sarvam',max(1,duration)*.49/60,model,'stt')
 data={'model':model,'language_code':'unknown'}
 if model=='saaras:v4':data['keyterms']=json.dumps(KEYTERMS)
 else:data['mode']='codemix'
 extension={'audio/webm':'webm','audio/mp4':'m4a','audio/wav':'wav','audio/ogg':'ogg'}.get(mime,'webm')
 try:
  async with client(4) as c:
   r=await c.post('https://api.sarvam.ai/speech-to-text',headers={'api-subscription-key':get('SARVAM_API_KEY')},data=data,files={'file':('clip.'+extension,audio,mime)});r.raise_for_status();body=r.json()
  await finish(reservation,body.get('model',model));return body.get('transcript','')
 except Exception as e:
  await finish(reservation,model,type(e).__name__);raise Unavailable('speech_unavailable') from None
async def speak(text_input,lang):
 f=await flags()
 if not f['voice_out'] or not f['vendor:sarvam']:raise Unavailable('voice_disabled')
 model='bulbul:v4-flash';reservation=await reserve('sarvam',len(text_input)/1000,model,'tts')
 body={'text':text_input,'model':model,'speaker':'aparna_hi_customer' if lang=='hi' else 'simran_enhi_customer','language_code':'hi-IN' if lang=='hi' else 'en-IN','enable_preprocessing':True,'speech_sample_rate':24000,'output_audio_codec':'wav'}
 try:
  async with client(6) as c:
   r=await c.post('https://api.sarvam.ai/text-to-speech/stream',headers={'api-subscription-key':get('SARVAM_API_KEY')},json=body);r.raise_for_status()
  await finish(reservation,model);return r.content,r.headers.get('content-type','audio/wav')
 except Exception as e:
  await finish(reservation,model,type(e).__name__);raise Unavailable('speech_unavailable') from None
