"""Two payment adapters. Staging-only networking; callback never decides paid status."""
import json
from decimal import Decimal,InvalidOperation
from urllib.parse import urlsplit
from paytmchecksum import PaytmChecksum
from fastapi import HTTPException
from apps.api.app.config import get
from apps.api.app.gateway import client
from apps.api.app.db import Payment,uid
from sqlalchemy import select

STAGING_HOST='https://securestage.paytmpayments.com'
SIMULATED_BANNER='SIMULATED — Paytm test keys pending'
TEST_BANNER='TEST PAYMENT — koi paisa nahi katega. Launch par yeh step licensed broker ka checkout hoga.'
def allowed_host(host):
 u=urlsplit(host)
 if u.scheme!='https' or u.hostname!='securestage.paytmpayments.com' or u.port not in (None,443) or u.username or u.password or u.path not in ('','/') or u.query or u.fragment:raise ValueError('Only the Paytm staging host is allowed')
 return STAGING_HOST

def signed_payload(body,key):
 raw=json.dumps(body,separators=(',',':'),ensure_ascii=False)
 signature=PaytmChecksum.generateSignature(raw,key)
 # The body bytes signed are embedded unchanged, rather than serialized twice.
 return '{"body":'+raw+',"head":{"signature":'+json.dumps(signature)+'}}'
def valid_signature(body,key,signature):
 if not signature:return False
 for separators in [(',',':'),(', ',': ')]:
  try:
   if PaytmChecksum.verifySignature(json.dumps(body,separators=separators,ensure_ascii=False),key,signature):return True
  except Exception:continue
 return False
class SimulatedAdapter:
 mode='simulated'
 async def initiate(self,order_id,owner):return {'mode':self.mode,'order_id':order_id,'amount':'1.00','status':'PENDING','banner':SIMULATED_BANNER}
 async def status(self,order_id):return {'status':'PENDING','verified':False}
 def verify_callback(self,params):return False
class StagingAdapter:
 mode='staging'
 def __init__(self,mid,key,host=STAGING_HOST,website='WEBSTAGING',public_url=None):
  self.mid=mid;self.key=key;self.host=allowed_host(host);self.website=website;self.public_url=public_url
 async def call(self,path,body,params=None):
  payload=signed_payload(body,self.key)
  try:
   async with client(10) as c:
    r=await c.post(self.host+path,params=params,content=payload,headers={'Content-Type':'application/json'});r.raise_for_status()
   data=r.json()
   if not valid_signature(data.get('body',{}),self.key,data.get('head',{}).get('signature','')):raise HTTPException(502,'Paytm staging response signature could not be verified')
   return data['body']
  except HTTPException:raise
  except Exception:raise HTTPException(502,'Paytm staging is unavailable; retry the TEST order') from None
 async def initiate(self,order_id,owner):
  public=(self.public_url or get('PUBLIC_URL')).rstrip('/')
  parsed=urlsplit(public)
  if parsed.scheme!='https' or not parsed.hostname or parsed.username or parsed.password:raise HTTPException(503,'Start the HTTPS demo tunnel before creating a staging order')
  body={'requestType':'Payment','mid':self.mid,'websiteName':self.website,'orderId':order_id,'callbackUrl':public+'/v1/pay/callback','txnAmount':{'value':'1.00','currency':'INR'},'userInfo':{'custId':owner}}
  result=await self.call('/theia/api/v1/initiateTransaction',body,{'mid':self.mid,'orderId':order_id})
  if result.get('resultInfo',{}).get('resultStatus')!='S' or not result.get('txnToken'):raise HTTPException(502,'Paytm could not create this TEST order')
  return {'mode':self.mode,'order_id':order_id,'amount':'1.00','status':'PENDING','txn_token':result['txnToken'],'mid':self.mid,'host':self.host,'banner':TEST_BANNER}
 async def status(self,order_id):
  result=await self.call('/v3/order/status',{'mid':self.mid,'orderId':order_id})
  state=result.get('resultInfo',{}).get('resultStatus','PENDING')
  if state=='TXN_SUCCESS':
   try:valid_amount=Decimal(str(result.get('txnAmount')))==Decimal('1.00')
   except (InvalidOperation,TypeError):valid_amount=False
   if result.get('orderId')!=order_id or result.get('mid')!=self.mid or not valid_amount or result.get('currency','INR')!='INR':raise HTTPException(502,'TEST payment identity or amount did not match')
  return {'status':state if state in ('TXN_SUCCESS','TXN_FAILURE') else 'PENDING','verified':state=='TXN_SUCCESS'}
 def verify_callback(self,params):
  params=dict(params);sig=params.pop('CHECKSUMHASH','')
  if params.get('MID')!=self.mid:return False
  try:
   if Decimal(params.get('TXNAMOUNT','0'))!=Decimal('1.00'):return False
   return bool(sig and PaytmChecksum.verifySignature(params,self.key,sig))
  except Exception:return False

def select_adapter():
 mid,key=get('PAYTM_MID'),get('PAYTM_MERCHANT_KEY')
 # The configured host is validated even before any network operation.
 host=allowed_host(get('PAYTM_HOST',STAGING_HOST))
 return StagingAdapter(mid,key,host,get('PAYTM_WEBSITE','WEBSTAGING')) if mid and key else SimulatedAdapter()
ADAPTER=select_adapter()
