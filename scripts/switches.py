#!/usr/bin/env python3
"""Operator kill switches. Passphrase is loaded privately, never passed in argv."""
import argparse,sys
from pathlib import Path
import httpx
from dotenv import dotenv_values
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('changes',nargs='*',help='e.g. voice_in=off voice_out=off');a=p.parse_args()
values=dotenv_values(ROOT/'.env');changes={}
for arg in a.changes:
 key,sep,value=arg.partition('=')
 if not sep or value not in ('on','off'):p.error('Use switch_name=on or switch_name=off')
 changes[key]=value=='on'
with httpx.Client(timeout=8) as c:
 if changes:r=c.post('http://127.0.0.1:8000/api/switches',json={'changes':changes},headers={'X-Demo-Passphrase':values.get('DEMO_LOGIN_PASSPHRASE','')})
 else:r=c.get('http://127.0.0.1:8000/api/switches')
 if not r.is_success:print('Could not update switches; check the local demo is running.',file=sys.stderr);sys.exit(1)
 for k,v in r.json().items():print(f'{k}: {"on" if v else "off"}')
