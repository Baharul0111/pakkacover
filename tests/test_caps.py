import asyncio
from datetime import datetime,timezone
from sqlalchemy import delete,select,func
import pytest
from apps.api.app import gateway as gw
from apps.api.app.db import Session,Usage,engine
class FutureClock(datetime):
 @classmethod
 def now(cls,tz=None):return cls(2099,1,1,12,tzinfo=timezone.utc)
async def test_app_cap_serializes_in_flight_spend(monkeypatch):
 monkeypatch.setattr(gw,'datetime',FutureClock)
 async with Session() as s:
  await s.execute(delete(Usage).where(Usage.day=='2099-01-01'))
  s.add(Usage(day='2099-01-01',provider='test',amount=145,model='test',step='test'));await s.commit()
 try:
  out=await asyncio.gather(gw.reserve('openai',4,'test','test'),gw.reserve('openai',4,'test','test'),return_exceptions=True)
  assert sum(isinstance(x,str) for x in out)==1
  assert sum(isinstance(x,gw.Unavailable) for x in out)==1
  async with Session() as s:
   assert await s.scalar(select(func.sum(Usage.amount)).where(Usage.day=='2099-01-01'))==149
 finally:
  async with Session() as s:await s.execute(delete(Usage).where(Usage.day=='2099-01-01'));await s.commit()
  await engine.dispose()
async def test_credit_floor_blocks_voice_before_network(monkeypatch):
 monkeypatch.setattr(gw,'get',lambda key,default='': '20' if key=='SARVAM_BALANCE_INR' else default)
 with pytest.raises(gw.Unavailable,match='speech_credit_floor'):await gw.reserve('sarvam',.1,'test','test')
 await engine.dispose()

async def test_rejected_provider_credit_is_not_charged_or_retried(monkeypatch):
 import httpx,time
 from apps.api.app.interview import Turn
 monkeypatch.setattr(gw,'datetime',FutureClock)
 async def flags():return dict(gw.DEFAULTS)
 monkeypatch.setattr(gw,'flags',flags);monkeypatch.setattr(gw,'pinned',lambda provider,model:model)
 calls=[]
 class Client:
  async def __aenter__(self):return self
  async def __aexit__(self,*args):pass
  async def post(self,*args,**kwargs):
   calls.append(1)
   response=httpx.Response(400,json={'error':{'type':'invalid_request_error','message':'Your credit balance is too low to access the API.'}},request=httpx.Request('POST','https://example.invalid'))
   response.raise_for_status()
 monkeypatch.setattr(gw,'client',lambda *args,**kwargs:Client())
 try:
  for _ in range(2):
   with pytest.raises(gw.Unavailable,match='provider_credit_unavailable'):
    await gw.structured('anthropic','claude-haiku-5-5',Turn,'test','test',step='credit_test')
  assert len(calls)==1 and gw.CREDIT_BLOCKED_UNTIL['anthropic']>time.monotonic()
  async with Session() as s:
   rows=(await s.scalars(select(Usage).where(Usage.day=='2099-01-01',Usage.step=='credit_test'))).all()
   assert len(rows)==1 and rows[0].amount==0 and rows[0].outcome=='provider_credit_unavailable'
 finally:
  gw.CREDIT_BLOCKED_UNTIL.pop('anthropic',None)
  async with Session() as s:await s.execute(delete(Usage).where(Usage.day=='2099-01-01'));await s.commit()
  await engine.dispose()
