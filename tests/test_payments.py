import json
from decimal import Decimal
import httpx,pytest
from paytmchecksum import PaytmChecksum
from fastapi import HTTPException
from apps.api.app import payments as pay
from tests.conftest import start,interview
from apps.api.app.config import get
DUMMY_KEY='1234567890abcdef'

def test_checksum_round_trip_and_tamper():
 body={'mid':'DUMMY_MID','orderId':'PC_TEST','txnAmount':{'value':'1.00','currency':'INR'}}
 envelope=json.loads(pay.signed_payload(body,DUMMY_KEY))
 assert pay.valid_signature(body,DUMMY_KEY,envelope['head']['signature'])
 assert not pay.valid_signature({**body,'orderId':'TAMPERED'},DUMMY_KEY,envelope['head']['signature'])

def test_callback_checksum_and_amount_are_checked():
 adapter=pay.StagingAdapter('DUMMY_MID',DUMMY_KEY)
 form={'MID':'DUMMY_MID','ORDERID':'PC_TEST','TXNAMOUNT':'1.00','STATUS':'TXN_SUCCESS'}
 signed={**form,'CHECKSUMHASH':PaytmChecksum.generateSignature(form,DUMMY_KEY)}
 assert adapter.verify_callback(signed)
 assert not adapter.verify_callback({**signed,'TXNAMOUNT':'100.00'})
 assert not adapter.verify_callback({**signed,'MID':'OTHER_MID'})
 assert not adapter.verify_callback({**signed,'CHECKSUMHASH':'bad'})
@pytest.mark.parametrize('host',['https://secure.paytmpayments.com','http://securestage.paytmpayments.com','https://securestage.paytmpayments.com.evil.test','https://securestage.paytmpayments.com@evil.test','https://evil.test'])
def test_production_or_lookalike_hosts_rejected_without_network(host):
 with pytest.raises(ValueError):pay.StagingAdapter('DUMMY_MID',DUMMY_KEY,host)

async def test_staging_signed_init_and_s2s_status(monkeypatch):
 seen=[]
 def respond(request):
  assert request.url.host=='securestage.paytmpayments.com'
  envelope=json.loads(request.content);body=envelope['body'];assert pay.valid_signature(body,DUMMY_KEY,envelope['head']['signature']);seen.append(str(request.url))
  if request.url.path.endswith('initiateTransaction'):
   assert body['txnAmount']=={'value':'1.00','currency':'INR'}
   assert body['callbackUrl']=='https://demo.example.test/v1/pay/callback'
   result={'resultInfo':{'resultStatus':'S'},'txnToken':'DUMMY_TXN_TOKEN'}
  else:result={'resultInfo':{'resultStatus':'TXN_SUCCESS'},'mid':'DUMMY_MID','orderId':'PC_TEST','txnAmount':'1.00','currency':'INR'}
  payload=json.loads(pay.signed_payload(result,DUMMY_KEY));return httpx.Response(200,json=payload)
 monkeypatch.setattr(pay,'client',lambda _:httpx.AsyncClient(transport=httpx.MockTransport(respond)))
 adapter=pay.StagingAdapter('DUMMY_MID',DUMMY_KEY,public_url='https://demo.example.test')
 assert (await adapter.initiate('PC_TEST','OWNER'))['txn_token']=='DUMMY_TXN_TOKEN'
 assert await adapter.status('PC_TEST')=={'status':'TXN_SUCCESS','verified':True}
 assert len(seen)==2

async def test_s2s_success_cannot_bypass_amount_or_order_check(monkeypatch):
 async def wrong(*args,**kwargs):return {'resultInfo':{'resultStatus':'TXN_SUCCESS'},'mid':'DUMMY_MID','orderId':'PC_TEST','txnAmount':'2.00'}
 adapter=pay.StagingAdapter('DUMMY_MID',DUMMY_KEY);monkeypatch.setattr(adapter,'call',wrong)
 with pytest.raises(HTTPException):await adapter.status('PC_TEST')

async def test_simulation_stays_labelled_and_owner_scoped(client,monkeypatch):
 monkeypatch.setattr(pay,'ADAPTER',pay.SimulatedAdapter())
 j,h=await start(client);body=await interview(client,j,h)
 for l in body['lines']:await client.post(f'/v1/lines/{l["id"]}/confirm',headers=h,json={'version':l['version']})
 await client.post(f'/v1/journeys/{j}/select',headers=h,json={'plan_id':'care_supreme_ic','d0':'2026-10-31','receipt':'2026-10-31'})
 await client.post(f'/v1/journeys/{j}/save',headers=h,json={'passphrase':get('DEMO_LOGIN_PASSPHRASE')})
 r=await client.post(f'/v1/journeys/{j}/pay/initiate',headers=h);assert r.status_code==200
 order=r.json();assert order['mode']=='simulated' and order['banner']==pay.SIMULATED_BANNER
 other,ho=await start(client)
 assert (await client.post(f'/v1/journeys/{other}/pay/{order["order_id"]}/status',headers=ho)).status_code==404
 r=await client.post(f'/v1/journeys/{j}/pay/{order["order_id"]}/simulate',headers=h)
 assert r.json()['status']=='SIMULATED_SUCCESS' and not r.json()['verified']
 assert (await client.post('/v1/pay/callback',data={'STATUS':'TXN_SUCCESS'})).status_code==400
