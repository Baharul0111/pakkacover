#!/usr/bin/env python3
"""Run a same-origin local demo and disposable HTTPS tunnel without printing secrets."""
import argparse,json,os,re,signal,subprocess,sys,time,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));os.chdir(ROOT);os.umask(0o077)
from dotenv import dotenv_values,set_key
import httpx
STATE=ROOT/'.run';STATE.mkdir(exist_ok=True);STATE.chmod(0o700)
PYTHON=str(ROOT/'.venv/bin/python')

def stop_one(kind):
 path=STATE/f'{kind}.pid'
 if not path.exists():return
 try:
  pid=int(path.read_text());command=subprocess.check_output(['ps','-p',str(pid),'-o','command='],text=True)
  expected={'api':'uvicorn apps.api.app.main:app','tunnel':'cloudflared tunnel','preflight':'scripts/payment_preflight.py','awake':'caffeinate -i -w'}[kind]
  if expected in command:
   os.kill(pid,signal.SIGTERM)
   for _ in range(20):
    try:os.kill(pid,0)
    except ProcessLookupError:break
    time.sleep(.15)
 except (ProcessLookupError,subprocess.CalledProcessError):pass
 path.unlink(missing_ok=True)

def stop():
 stop_one('preflight');stop_one('awake');stop_one('tunnel');stop_one('api');print('Demo API and tunnel stopped. Local PostgreSQL is retained for restart.')

def command(args):
 result=subprocess.run(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if result.returncode:raise RuntimeError('Setup command failed: '+Path(args[0]).name+' (no secret values printed)')

def ensure_database():
 values=dotenv_values(ROOT/'.env');url=values.get('DATABASE_URL') or ''
 local=not url or '127.0.0.1:55432/pakkacover_demo' in url
 if not local:return
 if not shutil.which('initdb'):command(['brew','install','postgresql@16'])
 bindir=Path(subprocess.check_output(['brew','--prefix','postgresql@16'],text=True).strip())/'bin'
 data=STATE/'postgres'
 if not (data/'PG_VERSION').exists():command([str(bindir/'initdb'),'-D',str(data),'-A','trust','-U','pakkacover','--no-locale','--encoding=UTF8'])
 status=subprocess.run([str(bindir/'pg_ctl'),'-D',str(data),'status'],capture_output=True)
 if status.returncode:
  command([str(bindir/'pg_ctl'),'-D',str(data),'-l',str(STATE/'postgres.log'),'-o','-h 127.0.0.1 -p 55432 -k /tmp','start'])
 exists=subprocess.run([str(bindir/'psql'),'-h','127.0.0.1','-p','55432','-U','pakkacover','-d','postgres','-tAc',"SELECT 1 FROM pg_database WHERE datname='pakkacover_demo'"],capture_output=True,text=True)
 if exists.stdout.strip()!='1':command([str(bindir/'createdb'),'-h','127.0.0.1','-p','55432','-U','pakkacover','pakkacover_demo'])
 if not url:set_key(str(ROOT/'.env'),'DATABASE_URL','postgresql://pakkacover@127.0.0.1:55432/pakkacover_demo',quote_mode='always')

def launch(kind,args):
 log=(STATE/f'{kind}.log').open('w')
 proc=subprocess.Popen(args,cwd=ROOT,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 (STATE/f'{kind}.pid').write_text(str(proc.pid));return proc

def wait_api(port):
 for _ in range(100):
  try:
   r=httpx.get(f'http://127.0.0.1:{port}/ready',timeout=2)
   if r.status_code==200:return r.json()
  except httpx.HTTPError:pass
  time.sleep(.3)
 raise RuntimeError('API did not become ready. See .run/api.log (secret-free startup errors).')

def tunnel(port):
 if not shutil.which('cloudflared'):command(['brew','install','cloudflared'])
 stop_one('tunnel')
 proc=launch('tunnel',['cloudflared','tunnel','--url',f'http://127.0.0.1:{port}','--protocol','http2','--edge-ip-version','4','--no-autoupdate'])
 for _ in range(120):
  log=(STATE/'tunnel.log').read_text(errors='replace')
  match=re.search(r'https://[a-z0-9-]+\.trycloudflare\.com',log)
  if match:
   url=match.group();set_key(str(ROOT/'.env'),'PUBLIC_URL',url,quote_mode='always');(STATE/'public_url').write_text(url);return url
  if proc.poll() is not None:raise RuntimeError('Quick tunnel exited; see .run/tunnel.log. Retry scripts/run_demo --retunnel.')
  time.sleep(.25)
 raise RuntimeError('Quick tunnel did not produce a URL; retry scripts/run_demo --retunnel.')

def main():
 p=argparse.ArgumentParser();p.add_argument('--stop',action='store_true');p.add_argument('--retunnel',action='store_true');p.add_argument('--restart-api',action='store_true');p.add_argument('--no-tunnel',action='store_true');p.add_argument('--no-build',action='store_true');p.add_argument('--status',action='store_true');p.add_argument('--port',type=int,default=8000);a=p.parse_args()
 if a.stop:return stop()
 if a.status:
  status=wait_api(a.port);print(json.dumps({'status':status['status'],'profile':status['profile'],'payment_mode':status['payment_mode'],'url':(STATE/'public_url').read_text() if (STATE/'public_url').exists() else f'http://127.0.0.1:{a.port}'}));return
 if a.restart_api:
  stop_one('awake');stop_one('api')
  proc=launch('api',[PYTHON,'-m','uvicorn','apps.api.app.main:app','--host','0.0.0.0','--port',str(a.port),'--no-access-log'])
  status=wait_api(a.port)
  if shutil.which('caffeinate'):launch('awake',['caffeinate','-i','-w',str(proc.pid)])
  print('API restarted; payment mode: '+status['payment_mode'])
  print('Phone URL unchanged: '+((STATE/'public_url').read_text() if (STATE/'public_url').exists() else f'http://127.0.0.1:{a.port}'))
  return
 if a.retunnel:
  wait_api(a.port);url=tunnel(a.port);print('PakkaCover HTTPS: '+url);return
 stop()
 ensure_database()
 from apps.api.app.config import bootstrap
 bootstrap()
 command([PYTHON,'-m','alembic','upgrade','head'])
 command([PYTHON,'scripts/eval_golden.py','--if-new'])
 if not (ROOT/'apps/web/node_modules').exists():command(['npm','ci','--prefix','apps/web','--no-audit','--no-fund'])
 if not a.no_build or not (ROOT/'apps/web/dist/index.html').exists():command(['npm','run','build','--prefix','apps/web'])
 proc=launch('api',[PYTHON,'-m','uvicorn','apps.api.app.main:app','--host','0.0.0.0','--port',str(a.port),'--no-access-log'])
 try:
  status=wait_api(a.port)
  url=f'http://127.0.0.1:{a.port}' if a.no_tunnel else tunnel(a.port)
  if shutil.which('caffeinate'):launch('awake',['caffeinate','-i','-w',str(proc.pid)])
  print('\nPakkaCover is ready · DEMO ONLY')
  print('Open on your phone: '+url)
  print('Payment mode: '+status['payment_mode'])
  print('Demo passphrase: stored in local .env (never printed).')
  print('Stop: scripts/run_demo --stop')
 except Exception:
  stop_one('api');stop_one('tunnel');raise
if __name__=='__main__':
 try:main()
 except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
