"""One spawned, bounded worker with hard wall timeouts and immediate warm respawn."""
import asyncio,multiprocessing,os,signal,subprocess
from concurrent.futures import ProcessPoolExecutor
from apps.api.app import media_worker

class Media:
 def __init__(self):self.pool=None;self.lock=asyncio.Lock();self.baseline=None;self.queued=0
 def start(self):
  if self.pool is None:self.pool=ProcessPoolExecutor(max_workers=1,mp_context=multiprocessing.get_context('spawn'),max_tasks_per_child=100,initializer=media_worker.initialize)
 async def warm(self):
  self.start();self.baseline=await asyncio.wait_for(asyncio.get_running_loop().run_in_executor(self.pool,media_worker.warm),10);return self.baseline
 def close(self):
  if self.pool:
   for process in (getattr(self.pool,'_processes',{}) or {}).values():
    if process.is_alive():process.terminate()
   self.pool.shutdown(wait=False,cancel_futures=True);self.pool=None
 async def call(self,kind,data):
  if self.queued>=3:raise ValueError('media_busy')
  self.queued+=1
  try:
   async with asyncio.timeout(20 if kind in ('image','audio') else 60):
    async with self.lock:
     self.start()
     try:return await asyncio.wait_for(asyncio.get_running_loop().run_in_executor(self.pool,{'image':media_worker.image_clean,'audio':media_worker.audio_duration,'pdf':media_worker.pdf_text}[kind],data),4 if kind in ('image','audio') else 45)
     except Exception:
      self.close();await self.warm();raise
  finally:self.queued-=1
media=Media()
