from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path
import asyncio,uuid,logging
from fastapi import FastAPI,Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse,JSONResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.formparsers import MultiPartParser
from sqlalchemy import text
from apps.api.app.config import ROOT,payment_mode,fernet
from apps.api.app.db import Session,engine
from apps.api.app.engine.rules import plans,simulate
from apps.api.app.routes import router
from apps.api.app import gateway as gw

# Uploads stay in memory; the streaming body cap is lower than the spool threshold.
MultiPartParser.spool_max_size=12*1024*1024
for name in ['httpx','httpcore','openai','anthropic','sqlalchemy.engine']:logging.getLogger(name).setLevel(logging.WARNING)
@asynccontextmanager
async def lifespan(app):
 plans()
 async with Session() as s:await s.execute(text('SELECT 1'))
 await gw.discover_models()
 yield
 await engine.dispose()
app=FastAPI(title='PakkaCover · Hackathon Demo',lifespan=lifespan)
app.include_router(router)

class BodyCap:
 def __init__(self,app):self.app=app
 async def __call__(self,scope,receive,send):
  if scope['type']!='http':return await self.app(scope,receive,send)
  headers=dict(scope.get('headers',[]));size=0;chunks=[]
  try:
   length=int(headers.get(b'content-length',b'0'))
  except ValueError:length=12*1024*1024
  if length>11*1024*1024:return await JSONResponse({'detail':'File too large'},status_code=413)(scope,receive,send)
  while True:
   msg=await receive()
   if msg['type']=='http.disconnect':return
   chunk=msg.get('body',b'');size+=len(chunk)
   if size>11*1024*1024:return await JSONResponse({'detail':'File too large'},status_code=413)(scope,receive,send)
   chunks.append(chunk)
   if not msg.get('more_body',False):break
  sent=False
  async def replay():
   nonlocal sent
   if not sent:sent=True;return {'type':'http.request','body':b''.join(chunks),'more_body':False}
   return await receive()
  await self.app(scope,replay,send)
app.add_middleware(BodyCap)
@app.middleware('http')
async def security(request:Request,call_next):
 rid=uuid.uuid4().hex[:12]
 try:response=await call_next(request)
 except Exception:
  # Never echo exception text: provider responses or validation can contain health input.
  return JSONResponse({'detail':'Please try again, or ask the demo operator.','request_id':rid},status_code=500)
 response.headers['X-Request-Id']=rid
 response.headers['X-Content-Type-Options']='nosniff'
 response.headers['Referrer-Policy']='no-referrer'
 response.headers['Permissions-Policy']='camera=(self), microphone=(self), geolocation=()'
 if request.url.path.startswith('/v1'):response.headers['Cache-Control']='no-store'
 return response
@app.exception_handler(RequestValidationError)
async def invalid(request,exc):
 return JSONResponse({'detail':'Check the highlighted input fields.','fields':['.'.join(str(p) for p in e['loc']) for e in exc.errors()]},status_code=422)
@app.get('/health')
def health():return {'status':'ok'}
@app.get('/ready')
async def ready():
 try:
  async with Session() as s:await s.execute(text('SELECT 1'))
  return {'status':'ok','profile':'demo','payment_mode':payment_mode(),'models':gw.MODEL_STATUS,'stt_model':gw.STT_MODEL}
 except Exception:return JSONResponse({'status':'database_unavailable','profile':'demo','payment_mode':payment_mode()},status_code=503)
@app.get('/v1/plans')
def all_plans():return list(plans().values())
@app.get('/v1/example')
def example():return simulate(date(2026,10,31),['hypertension'])
@app.get('/v1/method')
def method():return {'text':(ROOT/'docs/method.md').read_text()}
DIST=ROOT/'apps/web/dist'
if (DIST/'assets').exists():app.mount('/assets',StaticFiles(directory=DIST/'assets'),name='assets')
@app.get('/{path:path}',response_class=HTMLResponse)
def home(path:str=''):
 if path.startswith(('v1/','internal/')):return JSONResponse({'detail':'Not found'},status_code=404)
 if (DIST/'index.html').exists():return FileResponse(DIST/'index.html')
 return '''<meta name="viewport" content="width=device-width,initial-scale=1"><title>PakkaCover demo</title><style>body{font:18px system-ui;max-width:600px;margin:4em auto;padding:20px;background:#f5f4ee;color:#163e38}a{display:block;padding:20px;background:white;margin:16px 0;border-radius:16px}</style><h1>PakkaCover</h1><p>Understand your cover, one confirmed fact at a time.</p><p>Hackathon demo · Sample terms · Education only</p><a href="/v1/example">Sunita’s calculated example</a><a href="/docs">Try consent and interview in the API explorer</a>'''
