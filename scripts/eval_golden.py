#!/usr/bin/env python3
"""Optional owner-media A/B and no-fabrication gates. Never records transcripts or media outputs."""
import argparse,asyncio,csv,hashlib,json,mimetypes,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from apps.api.app import gateway as gw
from apps.api.app.media import media
from apps.api.app.medicine import read_strip
from apps.api.app.db import engine
# Script entities are from setup.md; aliases only grade preservation, never infer a diagnosis.
ALIASES={
'yes':['haan','yes','हाँ','हां'],'no':['nahi','no','नहीं'],'correct':['sahi','correct','सही'],'wrong':['galat','wrong','गलत'],
'unknown':['pata nahi','पता नहीं',"don’t know","do not know"],'bp':['bp','बीपी','बी.पी','blood pressure','रक्तचाप'],'sugar':['sugar','diabetes','शुगर','मधुमेह'],
'drug_telma':['telma','टेल्मा','टेलमा'],'drug_telmisartan':['telmisartan','टेल्मिसार्टन','टेलमिसार्टन'],'drug_metformin':['metformin','मेटफॉर्मिन','मेटफार्मिन'],
'drug_thyronorm':['thyronorm','थायरोनॉर्म','थायरोनर्म'],'drug_amlodipine':['amlodipine','एम्लोडिपिन','एम्लोडिपीन','अम्लोडिपिन'],'drug_atorvastatin':['atorvastatin','एटोरवास्टेटिन','एटोरवास्टैटिन'],
'hernia':['hernia','हर्निया'],'stopped':['band','stopped','बंद'],'heart':['heart','दिल','हृदय']}
EXPECTED={1:['yes'],2:['no'],3:['correct'],4:['wrong'],5:['52'],6:['5'],7:['1'],8:['unknown'],9:['bp','2019','drug_telma','40'],10:['sugar','drug_metformin','500','2'],11:['drug_thyronorm','50'],12:['drug_amlodipine','5','3'],13:['drug_atorvastatin','10'],14:['sugar'],15:['hernia','3'],16:['drug_telmisartan','6','stopped'],17:['bp','2019','drug_telmisartan','40'],18:['52','158','64'],19:['5','no'],20:['heart','60']}
def entity_present(entity,transcript):
 t=gw.normal(transcript)
 words={'once':'1','twice':'2','five':'5','six':'6','sixty':'60','fifty-two':'52'}
 for w,n in words.items():t=re.sub(r'\b'+re.escape(w)+r'\b',n,t)
 if entity.isdigit():return entity in gw.number_tokens(t)
 return any((re.search(r'\b'+re.escape(a)+r'\b',t) if a.isascii() and ' ' not in a else a in t) for a in ALIASES[entity])
def fingerprint(files):
 h=hashlib.sha256()
 for f in files:h.update(f.name.encode());h.update(f.read_bytes())
 return h.hexdigest()
def clean_salt(s):return re.sub(r'\b(tablets?|capsules?|ip|bp|usp)\b','',gw.normal(s)).strip(' ,.-')
async def evaluate(if_new=False):
 clips=sorted(f for f in (ROOT/'evals/golden/stt').glob('*') if f.suffix.lower() in ('.m4a','.mp4','.webm','.wav','.ogg','.mp3'))
 photos=sorted(f for f in (ROOT/'evals/golden/vision').glob('*') if f.suffix.lower() in ('.jpg','.jpeg','.png','.webp'))
 labels=ROOT/'evals/golden/vision/labels.csv';files=clips+photos+([labels] if labels.exists() else [])
 output=ROOT/'evals/results/golden-media.json';fp=fingerprint(files)
 if if_new and output.exists() and json.loads(output.read_text()).get('fingerprint')==fp:print('Golden media unchanged; keeping last measured result.');return
 report={'fingerprint':fp,'clip_count':len(clips),'photo_count':len(photos)}
 if not files:
  report.update(status='not_supplied',stt_pinned='saaras:v4',reason='Owner media absent; v4 default, manual/chip fallbacks retained.')
 else:
  await gw.discover_models()
  if clips:
   variants={}
   for model in ['saaras:v4','saaras:v3']:
    matched=total=passing=0;results=[]
    for clip in clips:
     m=re.search(r'stt-(\d+)',clip.stem)
     expected=EXPECTED.get(int(m.group(1))) if m else None
     if expected is None:results.append({'file':clip.name,'status':'missing_script_label'});continue
     try:
      data=clip.read_bytes();duration=await media.call('audio',data);transcript=await gw.transcribe(data,mimetypes.guess_type(clip.name)[0] or 'audio/mp4',duration,model)
      found=sum(entity_present(e,transcript) for e in expected);matched+=found;total+=len(expected);ok=found==len(expected);passing+=ok
      results.append({'file':clip.name,'passed':ok,'entities_preserved':found,'entity_count':len(expected)})
      del transcript,data
     except Exception as e:total+=len(expected);results.append({'file':clip.name,'passed':False,'error_type':type(e).__name__})
    variants[model]={'slot_accuracy':passing/max(1,len(clips)),'eps':matched/max(1,total),'clips':results}
   winner=max(variants,key=lambda k:(variants[k]['slot_accuracy'],variants[k]['eps'],k=='saaras:v4'))
   pin=ROOT/'models.yaml';cfg=json.loads(pin.read_text());cfg['stt']=winner;cfg['stt_reason']='Owner golden A/B: slot accuracy, then entity preservation.';pin.write_text(json.dumps(cfg,indent=2)+'\n')
   report['speech']={'winner':winner,'variants':variants,'passed':variants[winner]['eps']>=.95 and variants[winner]['slot_accuracy']==1}
  if photos:
   if not labels.exists():report['vision']={'passed':False,'reason':'labels.csv missing; no truth labels assumed'}
   else:
    with labels.open() as f:truth={r['file']:r for r in csv.DictReader(f)}
    results=[]
    for photo in photos:
     label=truth.get(photo.name)
     if not label:results.append({'file':photo.name,'passed':False,'reason':'missing_label'});continue
     try:
      result=await read_strip(photo.read_bytes());candidates=result['candidates'];expected=label['expected']
      if expected in ('null','please_type'):ok=not candidates
      else:ok=result['status']=='agree' and all(clean_salt(c['model_reading']['salt_text'])==clean_salt(label['salt_text']) and re.sub(r'\s','',gw.normal(c['strength']))==re.sub(r'\s','',gw.normal(label['strength'])) for c in candidates)
      results.append({'file':photo.name,'passed':ok,'status':result['status']})
     except Exception as e:results.append({'file':photo.name,'passed':False,'error_type':type(e).__name__})
    report['vision']={'passed':all(r['passed'] for r in results),'photos':results}
  report['status']='passed' if all(v.get('passed',False) for k,v in report.items() if k in ('speech','vision')) else 'needs_attention'
 output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('speech','vision')},indent=2))
 media.close();await engine.dispose()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--if-new',action='store_true');a=p.parse_args();asyncio.run(evaluate(a.if_new))
