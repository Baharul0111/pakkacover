#!/usr/bin/env python3
"""Download public wording documents with system trust, retaining provenance."""
import concurrent.futures, hashlib, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def fetch(item):
 key,entry=item
 target=ROOT/'data/plans/src'/entry['file'] if 'file' in entry else ROOT/f'data/plans/src/{key}.pdf'
 result=subprocess.run(['curl','--fail','--location','--silent','--show-error','--max-time','40',entry['url'],'--output',str(target)],capture_output=True,text=True)
 if result.returncode or not target.exists() or not target.read_bytes().startswith(b'%PDF'):
  return key,dict(entry,status='blocked',error=result.stderr.strip())
 data=target.read_bytes()
 return key,{'url':entry['url'],'file':target.name,'sha256':hashlib.sha256(data).hexdigest(),'status':'downloaded','bytes':len(data)}
if __name__=='__main__':
 p=ROOT/'data/plans/sources.json'; entries=json.loads(p.read_text())
 results=dict(concurrent.futures.ThreadPoolExecutor(5).map(fetch,entries.items()))
 p.write_text(json.dumps(results,indent=2)+'\n')
 for k,v in results.items(): print(k,v['status'],v.get('bytes',v.get('error')))
