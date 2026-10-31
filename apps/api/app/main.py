from datetime import date
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from apps.api.app.engine.rules import plans, simulate
app=FastAPI(title='PakkaCover · Hackathon Demo')
@app.get('/health')
def health(): return {'status':'ok'}
@app.get('/ready')
def ready(): return {'status':'ok','profile':'demo','payment_mode':'simulated','step':1}
@app.get('/v1/plans')
def all_plans(): return list(plans().values())
@app.get('/v1/example')
def example(): return simulate(date(2026,10,31),['hypertension'])
@app.get('/',response_class=HTMLResponse)
def home():
 return '''<meta name="viewport" content="width=device-width,initial-scale=1"><title>PakkaCover demo</title><style>body{font:18px system-ui;max-width:600px;margin:4em auto;padding:20px;background:#f5f4ee;color:#163e38}a{display:block;padding:20px;background:white;margin:16px 0;border-radius:16px}</style><h1>PakkaCover</h1><p>Understand your cover, one confirmed fact at a time.</p><p>Hackathon demo · Sample terms · Education only</p><a href="/v1/example">Try Sunita’s calculated example</a><a href="/docs">API explorer</a>'''
