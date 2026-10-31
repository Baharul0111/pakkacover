#!/usr/bin/env python3
"""Authorized 14:30 IST read-only payment-key check; never prints credentials."""
import argparse,json,time,os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import dotenv_values
import httpx
ROOT=Path(__file__).resolve().parents[1]
def check():
 values=dotenv_values(ROOT/'.env')
 desired='staging' if values.get('PAYTM_MID') and values.get('PAYTM_MERCHANT_KEY') else 'simulated'
 try:active=httpx.get('http://127.0.0.1:8000/ready',timeout=5).json().get('payment_mode','unavailable')
 except Exception:active='not_running'
 return {'checked_at':datetime.now(ZoneInfo('Asia/Kolkata')).isoformat(),'keys_complete':desired=='staging','configured_mode':desired,'running_mode':active,'restart_needed':active not in (desired,'not_running')}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--at-1430',action='store_true');a=p.parse_args()
 if a.at_1430:
  target=datetime(2026,10,31,14,30,tzinfo=ZoneInfo('Asia/Kolkata'))
  while (remaining:=(target-datetime.now(ZoneInfo('Asia/Kolkata'))).total_seconds())>0:time.sleep(min(remaining,30))
 result=check();state=ROOT/'.run';state.mkdir(exist_ok=True)
 path=state/('payment-preflight-1430.json' if a.at_1430 else 'payment-preflight-now.json');path.write_text(json.dumps(result,indent=2)+'\n');path.chmod(0o600)
 print(json.dumps(result))
