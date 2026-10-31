from datetime import date
from io import BytesIO
import pytest
from pypdf import PdfReader
from apps.api.app.sample_policy import make_policy
from apps.api.app.engine.rules import plans
from apps.api.app.audit import deterministic_fields,compare,FieldValue,verify
from tests.conftest import start,interview
from apps.api.app.config import get

CONTEXT={'member':{'age':52,'sex':'F'},'selection':{'plan_id':'care_supreme_ic','d0':'2026-10-31','receipt':'2026-11-02'},'conditions':['hypertension']}
@pytest.mark.parametrize('variant,key',[('clean',None),('m1_ped_addon_missing','instant_cover'),('m2_declared_condition_missing','declared'),('m3_dob_wrong','age')])
def test_g6_generated_policy_mismatches_and_clean(variant,key):
 data=make_policy(plans()['care_supreme_ic'],CONTEXT['member'],CONTEXT['conditions'],date(2026,10,31),variant)
 pages=[p.extract_text() for p in PdfReader(BytesIO(data)).pages]
 fields=deterministic_fields(pages);assert len(fields)==11
 result=compare(fields,CONTEXT)
 assert [f['key'] for f in result['flags']]==([] if key is None else [key])
 assert all(verify(field,pages) for field in fields.values())

def test_fabricated_quote_and_unaligned_value_are_rejected():
 f=FieldValue(key='age',found=True,value='55',page=1,quote='Member Age: 52')
 assert not verify(f,['Member Age: 52'])
 f=FieldValue(key='age',found=True,value='52',page=1,quote='Member Age: 52')
 assert not verify(f,['No age exists on this page'])

def test_unverified_fields_are_manual_not_silent_matches():
 result=compare({},CONTEXT)
 assert len(result['flags'])==10 and all(f['status']=='check_manually' for f in result['flags'])

async def test_audit_requires_save_purpose_and_owner_and_returns_no_pdf(client):
 j,h=await start(client);body=await interview(client,j,h)
 for l in body['lines']:await client.post(f'/v1/lines/{l["id"]}/confirm',headers=h,json={'version':l['version']})
 await client.post(f'/v1/journeys/{j}/select',headers=h,json={'plan_id':'care_supreme_ic','d0':'2026-10-31','receipt':'2026-11-02'})
 assert (await client.post(f'/v1/journeys/{j}/audit',headers=h,data={'variant':'clean'})).status_code==409
 await client.post(f'/v1/journeys/{j}/save',headers=h,json={'passphrase':get('DEMO_LOGIN_PASSPHRASE')})
 r=await client.post(f'/v1/journeys/{j}/audit',headers=h,data={'variant':'m1_ped_addon_missing'})
 assert r.status_code==200,r.text
 assert [f['key'] for f in r.json()['flags']]==['instant_cover']
 assert r.json()['free_look_last_day']=='2026-12-01'
 assert 'pdf' not in r.json()
 other,ho=await start(client)
 assert (await client.post(f'/v1/journeys/{j}/audit',headers=ho,data={'variant':'clean'})).status_code==404
 from apps.api.app.media import media
 media.close()
