from sqlalchemy import select,func
from apps.api.app import payments as pay
from apps.api.app.db import Session,Usage,Payment,Notification
from tests.conftest import start,interview
from apps.api.app.config import get

async def paid_journey(client):
 j,h=await start(client);body=await interview(client,j,h)
 for l in body['lines']:assert (await client.post(f'/api/lines/{l["id"]}/confirm',headers=h,json={'version':l['version']})).status_code==200
 assert (await client.post(f'/api/journeys/{j}/select',headers=h,json={'plan_id':'care_supreme_ic','d0':'2026-10-31','receipt':'2026-10-31'})).status_code==200
 assert (await client.post(f'/api/journeys/{j}/save',headers=h,json={'passphrase':get('DEMO_LOGIN_PASSPHRASE')})).status_code==200
 return j,h

async def test_demo_payment_owner_scope_idempotency_and_notification(client):
 assert pay.ADAPTER.mode=='demo'
 j,h=await paid_journey(client)
 order=(await client.post(f'/api/journeys/{j}/pay/initiate',headers=h)).json()
 assert order['mode']=='demo' and order['label']=='Demo' and order['amount']=='1.00'
 other,ho=await start(client)
 url=f'/api/journeys/{j}/pay/{order["order_id"]}/complete'
 assert (await client.post(url,headers=ho,json={'method':'UPI'})).status_code==404
 assert (await client.post(url,headers=h,json={'method':'Cash'})).status_code==422
 r=await client.post(url,headers=h,json={'method':'Wallet'});assert r.status_code==200,r.text
 result=r.json();assert result['status']=='PAID' and not result['verified'] and result['paid_at']
 again=(await client.post(url,headers=h,json={'method':'Card'})).json()
 assert again['paid_at']==result['paid_at'] and again['notification']['id']==result['notification']['id']
 notices=(await client.get(f'/api/journeys/{j}/notifications',headers=h)).json()
 assert len(notices)==1 and notices[0]['body'].startswith('₹1 paid') and notices[0]['mode']=='demo'
 assert (await client.get(f'/api/journeys/{j}/notifications',headers=ho)).status_code==404
 await client.post(f'/api/journeys/{j}/notifications/read',headers=h)
 assert (await client.get(f'/api/journeys/{j}/notifications',headers=h)).json()[0]['read']

async def test_reset_revokes_old_token_and_retains_spend(client):
 j,h=await paid_journey(client)
 async with Session() as s:before=await s.scalar(select(func.count()).select_from(Usage))
 other,ho=await start(client)
 assert (await client.post(f'/api/journeys/{j}/reset',headers=ho)).status_code==404
 r=await client.post(f'/api/journeys/{j}/reset',headers=h);assert r.status_code==200
 fresh=r.json();newh={'Authorization':'Bearer '+fresh['token']}
 assert (await client.get(f'/api/journeys/{j}',headers=h)).status_code==401
 data=(await client.get(f'/api/journeys/{fresh["journey_id"]}',headers=newh)).json()
 assert data['member'] is None and data['lines']==[] and data['selection'] is None
 assert (await client.get(f'/api/journeys/{fresh["journey_id"]}/notifications',headers=newh)).json()==[]
 async with Session() as s:assert await s.scalar(select(func.count()).select_from(Usage))==before

async def test_calendar_is_code_generated_and_has_no_health_details(client):
 j,h=await paid_journey(client)
 r=await client.get(f'/api/journeys/{j}/calendar',headers=h);assert r.status_code==200,r.text
 assert 'BEGIN:VCALENDAR' in r.text and r.text.count('BEGIN:VEVENT')==7
 assert '20261129' in r.text and 'hypertension' not in r.text and 'Telma' not in r.text
