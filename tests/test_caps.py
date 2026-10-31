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
