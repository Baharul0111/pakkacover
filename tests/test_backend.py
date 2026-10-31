import pytest
from sqlalchemy import text,select
from apps.api.app.db import Session,Consent
from tests.conftest import start,interview
from apps.api.app.config import get

async def test_g0_session_cannot_read_another_family(client):
 a,ha=await start(client);b,hb=await start(client)
 assert (await client.get(f'/api/journeys/{a}',headers=hb)).status_code==404
 assert (await client.get(f'/api/journeys/{a}')).status_code==401
 assert (await client.post(f'/api/journeys/{a}/advisor',headers=hb)).status_code==404
 assert (await client.post(f'/api/journeys/{a}/save',headers=hb,json={'passphrase':get('DEMO_LOGIN_PASSPHRASE')})).status_code==404

async def test_consent_and_member_attestation_required(client):
 j,h=await start(client)
 assert (await client.post(f'/api/journeys/{j}/member',headers=h,json={'age':52,'sex':'F','relation':'mother','attested':True})).status_code==409
 await client.post(f'/api/journeys/{j}/consent',headers=h,json={'disclosure':True,'alerts':False,'audit':True})
 assert (await client.post(f'/api/journeys/{j}/member',headers=h,json={'age':52,'sex':'F','relation':'mother','attested':False})).status_code==422
 async with Session() as s:
  cons=(await s.scalars(select(Consent).where(Consent.journey_id==j))).all()
  assert len(cons)==3 and len({r.purpose for r in cons})==3

async def test_confirmation_gate_encrypted_health_and_correction(client):
 j,h=await start(client);body=await interview(client,j,h)
 assert body['node']['key']=='review' and len(body['lines'])==17
 r=await client.post(f'/api/journeys/{j}/simulate',headers=h,json={});assert r.status_code==409
 for line in body['lines']:
  r=await client.post(f'/api/lines/{line["id"]}/confirm',headers=h,json={'version':line['version']});assert r.status_code==200
 r=await client.post(f'/api/journeys/{j}/simulate',headers=h,json={})
 assert [x['display_label'] for x in r.json()]==['Plan B','Plan C','Plan A']
 other,ho=await start(client)
 assert (await client.post(f'/api/lines/{body["lines"][0]["id"]}/confirm',headers=ho,json={'version':1})).status_code==404
 async with Session() as s:
  raw=await s.scalar(text('SELECT "payload_E" FROM app.journeys WHERE id=:id'),{'id':j})
  assert isinstance(raw,bytes) and b'hypertension' not in raw and b'Telma' not in raw
 lid=body['lines'][2]['id']
 assert (await client.post(f'/api/lines/{lid}/reopen',headers=h)).status_code==200
 assert (await client.post(f'/api/journeys/{j}/simulate',headers=h,json={})).status_code==409

async def test_minor_habits_are_skipped(client):
 j,h=await start(client)
 await client.post(f'/api/journeys/{j}/consent',headers=h,json={'disclosure':True})
 assert (await client.post(f'/api/journeys/{j}/member',headers=h,json={'age':12,'sex':'F','relation':'child','attested':True})).status_code==422
 assert (await client.post(f'/api/journeys/{j}/member',headers=h,json={'age':12,'sex':'F','relation':'child','attested':True,'guardian':True})).status_code==200
 from apps.api.app.interview import next_node,NODES
 slots={n[0]:'None' for n in NODES if n[0] not in ('tobacco','alcohol')}
 assert next_node({'member':{'age':12},'slots':slots})['key']=='review'

async def test_turn_retry_is_idempotent(client):
 j,h=await start(client)
 await client.post(f'/api/journeys/{j}/consent',headers=h,json={'disclosure':True})
 await client.post(f'/api/journeys/{j}/member',headers=h,json={'age':52,'sex':'F','relation':'self','attested':True})
 hh={**h,'Idempotency-Key':'test-key'}
 a=await client.post(f'/api/journeys/{j}/answer',headers=hh,json={'text':'158'})
 b=await client.post(f'/api/journeys/{j}/answer',headers=hh,json={'text':'158'})
 assert a.json()==b.json()
 lines=(await client.get(f'/api/journeys/{j}',headers=h)).json()['lines']
 assert len([line for line in lines if line['key']=='height'])==1
 assert len([line for line in lines if line['key']=='member'])==1

async def test_switches_require_passphrase(client):
 assert (await client.post('/api/switches',json={'changes':{'voice_in':False}})).status_code==403

async def test_oversize_body_rejected_before_parse(client):
 r=await client.post('/api/session',content=b'X'*100,headers={'Content-Length':str(12*1024*1024)})
 assert r.status_code==413

async def test_voice_values_are_always_marked_for_human_check(client,monkeypatch):
 from apps.api.app import gateway as gw
 from apps.api.app.media import media
 async def stt(*args,**kwargs):return '158'
 async def measured(*args,**kwargs):return 2.0
 monkeypatch.setattr(gw,'transcribe',stt);monkeypatch.setattr(media,'call',measured)
 j,h=await start(client)
 await client.post(f'/api/journeys/{j}/consent',headers=h,json={'disclosure':True})
 await client.post(f'/api/journeys/{j}/member',headers=h,json={'age':52,'sex':'F','relation':'self','attested':True})
 r=await client.post(f'/api/journeys/{j}/voice',headers=h,files={'audio':('test.wav',b'synthetic placeholder','audio/wav')},data={'duration':'2'})
 assert r.status_code==200 and r.json()['accepted']
 line=next(l for l in (await client.get(f'/api/journeys/{j}',headers=h)).json()['lines'] if l['key']=='height')
 assert line['ai_guess'] and not line['confirmed'] and line['source'].startswith('voice:')

async def test_identity_reopen_requires_fresh_member_attestation_and_review(client):
 j,h=await start(client);body=await interview(client,j,h)
 identity=next(line for line in body['lines'] if line['key']=='member')
 for line in body['lines']:
  await client.post(f'/api/lines/{line["id"]}/confirm',headers=h,json={'version':line['version']})
 assert (await client.post(f'/api/lines/{identity["id"]}/reopen',headers=h)).status_code==200
 fresh=(await client.get(f'/api/journeys/{j}',headers=h)).json()
 assert fresh['node']['key']=='relation' and not fresh['member'] and not fresh['lines']
 assert (await client.post(f'/api/journeys/{j}/simulate',headers=h,json={})).status_code==409
 assert (await client.post(f'/api/journeys/{j}/member',headers=h,json={'name':'Corrected demo','age':53,'sex':'F','relation':'mother','attested':False})).status_code==422
 updated=await client.post(f'/api/journeys/{j}/member',headers=h,json={'name':'Corrected demo','age':53,'sex':'F','relation':'mother','attested':True})
 assert updated.status_code==200
 assert updated.json()['lines'][0]['value']=='Corrected demo · 53 · F'
 assert not updated.json()['lines'][0]['confirmed']
