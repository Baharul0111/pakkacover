#!/usr/bin/env python3
"""Compatibility status command. Scheduled gateway/key checks are cancelled."""
import argparse,json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import httpx
ROOT=Path(__file__).resolve().parents[1]
def check():
 try:active=httpx.get('http://127.0.0.1:8000/api/ready',timeout=5).json().get('payment_mode','unavailable')
 except httpx.HTTPError:active='not_running'
 return {'checked_at':datetime.now(ZoneInfo('Asia/Kolkata')).isoformat(),'configured_mode':'demo','running_mode':active,'scheduled_key_check':'cancelled','gateway_calls':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--at-1430',action='store_true',help='Obsolete flag; reports demo status immediately without waiting.');p.parse_args()
 result=check();state=ROOT/'.run';state.mkdir(exist_ok=True);path=state/'payment-demo-status.json';path.write_text(json.dumps(result,indent=2)+'\n');path.chmod(0o600);print(json.dumps(result))
