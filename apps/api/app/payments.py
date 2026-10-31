"""Clearly labelled, local-only demonstration. Never contacts a payment provider."""
class DemoAdapter:
 mode='demo'
 async def initiate(self,order_id,owner):
  return {'mode':'demo','order_id':order_id,'amount':'1.00','status':'PENDING','verified':False,'label':'Demo'}
ADAPTER=DemoAdapter()
