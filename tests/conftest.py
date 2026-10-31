import pytest_asyncio
import httpx
from apps.api.app.main import app
from apps.api.app.db import engine
@pytest_asyncio.fixture
async def client():
 async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://test') as c:yield c
 await engine.dispose()
async def start(client):
 r=await client.post('/v1/session',json={'lang':'hi'});assert r.status_code==200
 body=r.json();return body['journey_id'],{'Authorization':'Bearer '+body['token']}
async def interview(client,jid,headers):
 assert (await client.post(f'/v1/journeys/{jid}/consent',headers=headers,json={'disclosure':True,'alerts':True,'audit':True})).status_code==200
 assert (await client.post(f'/v1/journeys/{jid}/member',headers=headers,json={'age':52,'sex':'F','relation':'mother','attested':True})).status_code==200
 answers=['158','64','BP / hypertension','2019','Yes','No','Telma 40 mg','BP / hypertension','Once daily','None','None','No','No','No']
 for a in answers:
  r=await client.post(f'/v1/journeys/{jid}/answer',headers=headers,json={'text':a});assert r.status_code==200,r.text
  assert r.json()['accepted'],r.text
 return (await client.get(f'/v1/journeys/{jid}',headers=headers)).json()
