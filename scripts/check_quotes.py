#!/usr/bin/env python3
"""G2: verify source bytes, UIN, page alignment and every verbatim rule quote."""
import hashlib,json,re,unicodedata,sys
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from apps.api.app.engine.rules import Plan

def normalize(text):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',text)).strip()
def clauses(obj):
 if isinstance(obj,dict):
  if {'doc_id','page','quote','quote_sha'}<=obj.keys():yield obj
  else:
   for val in obj.values():yield from clauses(val)
 elif isinstance(obj,list):
  for val in obj:yield from clauses(val)
def check_plan(plan:dict,sources:dict,cache:dict):
 Plan.model_validate(plan)
 for q in clauses(plan):
  doc=q['doc_id']; source=sources[doc]; path=ROOT/'data/plans/src'/source['file']
  if doc not in cache:
   assert hashlib.sha256(path.read_bytes()).hexdigest()==source['sha256'],f'{doc}: source bytes changed'
   cache[doc]=[normalize(p.extract_text()) for p in PdfReader(path).pages]
  assert hashlib.sha256(q['quote'].encode()).hexdigest()==q['quote_sha'],f'{doc}: quote hash changed'
  assert normalize(q['quote']) in cache[doc][q['page']-1],f'{doc}: quote absent on page {q["page"]}'
 uin=re.sub(r'\W','',plan['uin'])
 assert uin in re.sub(r'\W','',''.join(cache[plan['source_doc']])),f'{plan["plan_id"]}: UIN mismatch'
 assert plan['initial_wait']['value']==30
 assert plan['ped_wait']['value']<=36 and plan['specific_wait']['value']<=36
 assert plan['moratorium']['value']==60 and plan['free_look']['value']>=30
 return sum(1 for _ in clauses(plan))
def check_all():
 sources=json.loads((ROOT/'data/plans/sources.json').read_text()); cache={};count=0
 for file in sorted((ROOT/'data/plans').glob('plan_*.json')):
  plan=json.loads(file.read_text()); n=check_plan(plan,sources,cache);count+=n
  print(f'{plan["display_label"]}: {n} clause references verified')
 return count
if __name__=='__main__':print(f'PASS: {check_all()} PDF-aligned clause references')
