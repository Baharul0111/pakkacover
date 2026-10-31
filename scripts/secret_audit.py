#!/usr/bin/env python3
"""Fail closed on real credential material/private media, never print matched values."""
import argparse,re,subprocess,sys
from pathlib import Path
from dotenv import dotenv_values
ROOT=Path(__file__).resolve().parents[1]
SECRET_NAMES=['ANTHROPIC_API_KEY','OPENAI_API_KEY','SARVAM_API_KEY','FERNET_KEYS','PEPPER','DEMO_LOGIN_PASSPHRASE','PAYTM_MERCHANT_KEY','DATABASE_URL_REMOTE','GH_TOKEN','RENDER_API_KEY','CLOUDFLARE_API_TOKEN']
PATTERNS=[('provider_key',re.compile(rb'\bsk-(?:ant-api\d+-|proj-)?[A-Za-z0-9_-]{24,}')),('github_token',re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})'))]
def check(path,data,values):
 errors=[]
 if path=='.env' or path.startswith(('.env.','secrets/')):errors.append('private_path')
 if path.startswith('evals/golden/') and Path(path).suffix.lower() in ['.m4a','.mp3','.wav','.webm','.jpg','.jpeg','.png','.mp4','.ogg','.webp']:errors.append('private_media')
 if path.startswith('data/plans/src/') and path.endswith('.pdf'):errors.append('private_source_pdf')
 if path.endswith('.dump'):errors.append('database_dump')
 for name,value in values.items():
  if name in SECRET_NAMES and value and len(value)>12 and value.encode() in data:errors.append('env_value:'+name)
 for label,pattern in PATTERNS:
  if pattern.search(data):errors.append(label)
 for match in re.finditer(rb'postgres(?:ql)?(?:\+asyncpg)?://[^\s/:]+:([^\s@]+)@',data):
  password=match.group(1).lower()
  if not any(w in password for w in [b'your',b'password',b'xxxxx',b'dummy',b'<',b'[',b'...']):errors.append('credential_database_url')
 for match in re.finditer(rb'(?:FERNET_KEYS|PEPPER|API_KEY)\s*=\s*[\"\x27]([A-Za-z0-9_\-+/=]{30,})[\"\x27]',data):errors.append('literal_secret_assignment')
 return errors
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--history',action='store_true');a=p.parse_args();values=dotenv_values(ROOT/'.env');issues=[]
 tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
 for name in filter(None,tracked):
  path=ROOT/name
  if path.is_file():
   errors=check(name,path.read_bytes(),values)
   if errors:issues.append((name,sorted(set(errors))))
 if a.history:
  objects=subprocess.check_output(['git','rev-list','--objects','--all'],cwd=ROOT,text=True).splitlines()
  for entry in objects:
   obj,sep,name=entry.partition(' ')
   if not sep:continue
   kind=subprocess.check_output(['git','cat-file','-t',obj],cwd=ROOT,text=True).strip()
   if kind!='blob':continue
   data=subprocess.check_output(['git','cat-file','blob',obj],cwd=ROOT);errors=check(name,data,values)
   if errors:issues.append(('history:'+name,sorted(set(errors))))
 if issues:
  for path,reasons in issues:print(path,','.join(reasons))
  print('FAIL: push aborted; no secret values printed.');sys.exit(1)
 print('PASS: tracked files'+(' and all history' if a.history else '')+' contain no detected credentials or private media.')
