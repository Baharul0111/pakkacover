#!/usr/bin/env python3
"""Bounded, secret-free preflight for the authorized Supabase deployment."""
import asyncio,json,socket,sys
from pathlib import Path
from dotenv import dotenv_values
from sqlalchemy.engine import make_url
import asyncpg
ROOT=Path(__file__).resolve().parents[1]
async def check():
 values=dotenv_values(ROOT/'.env');raw=values.get('DATABASE_URL_REMOTE') or values.get('DATABASE_URL')
 result={'ready':False,'reason':'missing_remote_database'}
 if raw:
  try:
   u=make_url(raw)
   if u.host in ('localhost','127.0.0.1','::1'):
    result['reason']='local_database_only'
   else:
    async with asyncio.timeout(18):
     await asyncio.get_running_loop().getaddrinfo(u.host,6543)
     connection=await asyncpg.connect(host=u.host,port=6543,user=u.username,password=u.password,database=u.database,ssl='require',statement_cache_size=0,timeout=12)
     try:
      assert await connection.fetchval('SELECT 1')==1
      result={'ready':True,'reason':'remote_transaction_pooler_verified','port':6543}
     finally:await connection.close()
  except socket.gaierror:result['reason']='remote_dns_failed'
  except TimeoutError:result['reason']='remote_connection_timeout'
  except Exception as e:result['reason']='remote_connection_failed:'+type(e).__name__
 target=ROOT/'.run/hosted-db-check.json';target.parent.mkdir(exist_ok=True);target.write_text(json.dumps(result,indent=2))
 print(json.dumps(result));return 0 if result['ready'] else 1
if __name__=='__main__':raise SystemExit(asyncio.run(check()))
