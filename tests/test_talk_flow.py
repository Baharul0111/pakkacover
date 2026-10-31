"""Public Talk-path contracts: sequential identity, units, reset and voice facts."""
import pytest
from sqlalchemy import select
from apps.api.app import interview as fsm
from apps.api.app.db import Session,Consent
from tests.conftest import start

@pytest.mark.parametrize('key,utterance,expected',[
 ('height','5 foot 2','157'),('height','five feet two inches','157'),
 ('height','पांच फुट दो इंच','157'),('height','158 cm','158'),
 ('weight','68 kilo','68'),('weight','६८ किलो','68'),('age','बावन साल','52'),
 ('age','52 years','52'),('name','Her name is Sunita','Sunita'),
 ('name','उनका नाम सुनीता है','सुनीता'),('relation','मेरी माँ के लिए','mother'),
 ('sex','महिला','F'),('height','pata nahi','Not sure'),
])
def test_explicit_talk_values_and_code_unit_conversion(key,utterance,expected):
 node=next(n for n in fsm.IDENTITY_NODES+fsm.NODES if n[0]==key)
 assert fsm.direct_value(fsm.node_view(*node),utterance)==expected

@pytest.mark.parametrize('key,utterance',[
 ('height','5 foot 12'),('height','5.2'),('height','short'),('weight','68 or 86 kilo'),
 ('age','52 or 53'),('age','-3'),('age','3.5'),('name','pata nahi'),
])
async def test_ambiguous_identity_or_measurements_ask_again(key,utterance):
 node=next(n for n in fsm.IDENTITY_NODES+fsm.NODES if n[0]==key)
 values,_=await fsm.extract(fsm.node_view(*node),utterance)
 assert values=={}

async def test_reset_then_full_sunita_voice_sequence_to_check(client,monkeypatch):
 from apps.api.app import gateway as gw
 from apps.api.app.media import media
 spoken=''
 async def stt(*args,**kwargs):return spoken
 async def measured(*args,**kwargs):return 2.0
 monkeypatch.setattr(gw,'transcribe',stt);monkeypatch.setattr(media,'call',measured)
 jid,h=await start(client)
 await client.post(f'/api/journeys/{jid}/consent',headers=h,json={'disclosure':True,'alerts':False,'audit':True})
 # Prove a partially filled run is discarded, rather than resumed in the middle.
 await client.post(f'/api/journeys/{jid}/answer',headers=h,json={'text':'Myself'})
 reset=(await client.post(f'/api/journeys/{jid}/reset',headers=h)).json()
 assert reset['disclosure_consented']
 jid=reset['journey_id'];h={'Authorization':'Bearer '+reset['token']}
 fresh=(await client.get(f'/api/journeys/{jid}',headers=h)).json()
 assert fresh['node']['key']=='relation' and fresh['node']['group']==1 and fresh['slots']=={} and fresh['lines']==[] and fresh['member'] is None
 steps=[('relation','Mother'),('attestation','I agree'),('name','Her name is Sunita'),('age','52 years'),('sex','Female'),('height','5 foot 2'),('weight','68 kilo'),('conditions','BP / hypertension'),('since','2019'),('diagnosed','Yes'),('complications','No'),('treatment','Yes'),('medicine','Telma 40 mg'),('dose','1 tablet'),('frequency','Once daily'),('indication','BP / hypertension'),('hospital','None'),('tests','None'),('tobacco','No'),('alcohol','No'),('family_history','No')]
 for key,value in steps:
  data=(await client.get(f'/api/journeys/{jid}',headers=h)).json()
  assert data['node']['key']==key
  assert data['node']['group']==fsm.GROUPS[key] and data['node']['total_groups']==12
  spoken=value
  if key=='attestation':r=await client.post(f'/api/journeys/{jid}/answer',headers=h,json={'text':value})
  else:r=await client.post(f'/api/journeys/{jid}/voice',headers=h,files={'audio':('answer.wav',b'test placeholder','audio/wav')},data={'duration':'2'})
  assert r.status_code==200 and r.json()['accepted'],(key,r.status_code)
  data=(await client.get(f'/api/journeys/{jid}',headers=h)).json()
  if key=='name':assert data['slots']['name']=='Sunita' and data['member'] is None
  if key=='age':assert data['slots']['age']=='52'
 data=(await client.get(f'/api/journeys/{jid}',headers=h)).json()
 assert data['node']['key']=='review' and data['node']['progress']==100 and data['node']['en']=="That's all. Let's check your answers."
 assert data['slots']['height']=='157' and data['slots']['weight']=='68'
 assert len(data['lines'])==20 and all(not line['confirmed'] for line in data['lines'])
 assert all(line['ai_guess'] and line['source'].startswith('voice:') for line in data['lines'])
 assert (await client.post(f'/api/journeys/{jid}/simulate',headers=h,json={})).status_code==409
 async with Session() as s:
  rows=(await s.scalars(select(Consent).where(Consent.journey_id==jid))).all()
  assert {c.purpose:c.granted for c in rows}=={'P1_disclosure':True,'P2_alerts':False,'P3_audit':True,'P1_member_attest':True}

async def test_minor_voice_identity_requires_guardian_and_skips_habits(client):
 jid,h=await start(client)
 await client.post(f'/api/journeys/{jid}/consent',headers=h,json={'disclosure':True})
 for value in ['Child','I agree','Demo child','12']:
  r=await client.post(f'/api/journeys/{jid}/answer',headers=h,json={'text':value});assert r.json()['accepted']
 data=(await client.get(f'/api/journeys/{jid}',headers=h)).json()
 assert data['node']['key']=='guardian'
 for value in ['I am their legal guardian','Female','158','64','None','No medicine','None','None','No']:
  r=await client.post(f'/api/journeys/{jid}/answer',headers=h,json={'text':value});assert r.json()['accepted']
 data=(await client.get(f'/api/journeys/{jid}',headers=h)).json()
 assert data['node']['key']=='review' and 'tobacco' not in data['slots'] and 'alcohol' not in data['slots']
