"""Media-only subprocess targets. No API/DB/model SDK imports; raw media never reaches disk."""
from io import BytesIO
import os

def warm():
 import resource
 from PIL import Image
 import pypdf
 return {'rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'pid':os.getpid()}

def image_clean(data):
 from PIL import Image,ImageOps
 Image.MAX_IMAGE_PIXELS=12_000_000
 with Image.open(BytesIO(data)) as img:
  if img.width*img.height>12_000_000:raise ValueError('image_pixel_limit')
  img=ImageOps.exif_transpose(img);img.thumbnail((1600,1600));img=img.convert('RGB')
  out=BytesIO();img.save(out,format='JPEG',quality=85)
  return out.getvalue()

def pdf_text(data):
 from pypdf import PdfReader
 reader=PdfReader(BytesIO(data))
 if reader.is_encrypted or len(reader.pages)>40:raise ValueError('unsupported_pdf')
 root=reader.trailer['/Root']
 if '/OpenAction' in root or '/AA' in root or '/JavaScript' in root.get('/Names',{}):raise ValueError('active_pdf')
 pages=[]
 for p in reader.pages:
  if '/AA' in p:raise ValueError('active_pdf')
  for annotation in p.get('/Annots',[]):
   ann=annotation.get_object()
   if '/A' in ann and ann['/A'].get('/S') in ('/JavaScript','/Launch'):raise ValueError('active_pdf')
  contents=p.get_contents()
  if contents is not None and len(contents.get_data())>8*1024*1024:raise ValueError('expanded_pdf_limit')
  pages.append(p.extract_text()[:50000])
 return pages

def initialize():
 import resource
 # A local Mac has no Render cgroup; bound per-worker data allocation instead.
 cap=768*1024*1024
 _,hard=resource.getrlimit(resource.RLIMIT_DATA)
 if hard!=resource.RLIM_INFINITY:cap=min(cap,hard)
 resource.setrlimit(resource.RLIMIT_DATA,(cap,hard))

def audio_duration(data):
 import av
 from io import BytesIO
 length=0.0
 with av.open(BytesIO(data)) as source:
  for frame in source.decode(audio=0):
   length+=frame.samples/frame.sample_rate
   if length>25.6:raise ValueError('audio_duration_limit')
 if length<=0:raise ValueError('audio_duration_limit')
 return length
