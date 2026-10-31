"""Local configuration. Secret values are never part of logs or API responses."""
import os,secrets
from pathlib import Path
from dotenv import dotenv_values,set_key
from cryptography.fernet import Fernet,MultiFernet
ROOT=Path(__file__).resolve().parents[3]
ENV=ROOT/'.env'
SERVERLESS=bool(os.environ.get('VERCEL'))
def bootstrap():
 if SERVERLESS:return
 if not ENV.exists():ENV.touch(mode=0o600)
 values=dotenv_values(ENV)
 for name,factory in [('FERNET_KEYS',lambda:Fernet.generate_key().decode()),('PEPPER',lambda:secrets.token_urlsafe(32)),('DEMO_LOGIN_PASSPHRASE',lambda:secrets.token_urlsafe(18))]:
  if not values.get(name):set_key(str(ENV),name,factory(),quote_mode='always')
 ENV.chmod(0o600)
bootstrap()
def values():
 # Local demo credentials belong to this checkout, not the parent agent shell.
 # Hosted runtimes have no .env and receive their explicit production settings.
 if SERVERLESS:return dict(os.environ)
 return {**os.environ,**dotenv_values(ENV),**{k:v for k,v in os.environ.items() if k.startswith('PCC_')}}
def get(key,default=''):return values().get(key) or default
def fernet():return MultiFernet([Fernet(k.strip().encode()) for k in get('FERNET_KEYS').split(',')])
def payment_mode():return 'demo'
