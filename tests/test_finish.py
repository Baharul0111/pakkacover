from sqlalchemy import select
from apps.api.app.db import Session,AuditRun
from tests.conftest import start
from tests.test_payments import paid_journey

FIELDS={'uin':'CHIHLIP25047V022425','inception':'2026-10-31','sum_insured':'500000','age':'52','sex':'F','declared':'hypertension','instant_cover':'Yes','ped_months':'36','initial_days':'30','specific_months':'24'}
async def audited(client,flagged=False):
 jid,h=await paid_journey(client)
 fields={**FIELDS,'instant_cover':'No' if flagged else 'Yes'}
 r=await client.post(f'/api/journeys/{jid}/audit/manual',headers=h,json={'fields':fields,'checked':True})
 assert r.status_code==200
 return jid,h,r.json()

async def test_clean_review_finishes_persists_and_is_idempotent(client):
 jid,h,audit=await audited(client)
 r=await client.post(f'/api/journeys/{jid}/finish',headers=h,json={'audit_id':audit['audit_id'],'acknowledged':True})
 assert r.status_code==200
 result=r.json();assert result['status']=='completed' and result['flag_count']==0
 assert result['policy_accepted'] is False and result['payment_status']=='NOT_PAID'
 assert result['free_look_last_day']=='2026-11-29'
 assert (await client.get(f'/api/journeys/{jid}',headers=h)).json()['completion']==result
 repeat=await client.post(f'/api/journeys/{jid}/finish',headers=h,json={'audit_id':audit['audit_id'],'acknowledged':True})
 assert repeat.json()==result

async def test_flagged_review_needs_ack_keeps_flags_and_is_owner_scoped(client):
 jid,h,audit=await audited(client,True)
 body={'audit_id':audit['audit_id'],'acknowledged':True}
 other,ho=await start(client)
 assert (await client.post(f'/api/journeys/{jid}/finish',headers=ho,json=body)).status_code==404
 assert (await client.get(f'/api/journeys/{jid}/audit/latest',headers=ho)).status_code==404
 assert (await client.post(f'/api/journeys/{other}/finish',headers=ho,json=body)).status_code==409
 assert (await client.post(f'/api/journeys/{jid}/finish',headers=h,json={**body,'acknowledged':False})).status_code==422
 result=(await client.post(f'/api/journeys/{jid}/finish',headers=h,json=body)).json()
 assert result['status']=='completed_with_follow_up' and result['flag_count']==1
 assert not result['issues_resolved'] and not result['policy_accepted']
 assert result['flags'][0]['key']=='instant_cover'
 latest=(await client.get(f'/api/journeys/{jid}/audit/latest',headers=h)).json()
 assert latest['flags']==audit['flags'] and latest['audit_id']==audit['audit_id'] and 'context_fingerprint' not in latest
 fresh=(await client.post(f'/api/journeys/{jid}/reset',headers=h)).json()
 assert (await client.get(f'/api/journeys/{fresh["journey_id"]}',headers={'Authorization':'Bearer '+fresh['token']})).json()['completion'] is None

async def test_changed_context_and_superseded_audit_cannot_be_finished(client):
 jid,h,audit=await audited(client)
 await client.post(f'/api/journeys/{jid}/select',headers=h,json={'plan_id':'care_supreme_ic','d0':'2026-10-31','receipt':'2026-11-02'})
 r=await client.post(f'/api/journeys/{jid}/finish',headers=h,json={'audit_id':audit['audit_id'],'acknowledged':True})
 assert r.status_code==409
 newer=(await client.post(f'/api/journeys/{jid}/audit/manual',headers=h,json={'fields':FIELDS,'checked':True})).json()
 assert newer['audit_id']!=audit['audit_id']
 assert (await client.post(f'/api/journeys/{jid}/finish',headers=h,json={'audit_id':audit['audit_id'],'acknowledged':True})).status_code==409
 assert (await client.post(f'/api/journeys/{jid}/finish',headers=h,json={'audit_id':newer['audit_id'],'acknowledged':True})).status_code==200

async def test_existing_owner_audit_from_before_finish_feature_is_supported(client):
 jid,h,audit=await audited(client,True)
 async with Session() as s:
  record=await s.get(AuditRun,audit['audit_id']);record.payload={key:value for key,value in record.payload.items() if key!='context_fingerprint'};await s.commit()
 r=await client.post(f'/api/journeys/{jid}/finish',headers=h,json={'audit_id':audit['audit_id'],'acknowledged':True})
 assert r.status_code==200 and r.json()['flag_count']==1
