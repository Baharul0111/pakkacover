#!/usr/bin/env python3
"""Reproduce the hand-entered demo rules and pin their PDF quote anchors."""
import hashlib,json,re,unicodedata
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
CACHE={}
def norm(t):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',t)).strip()
def quote(doc,page,section,anchor,length=270):
 if doc not in CACHE:CACHE[doc]=[norm(p.extract_text()) for p in PdfReader(ROOT/f'data/plans/src/{doc}.pdf').pages]
 text=CACHE[doc][page-1]
 if anchor.lower() not in text.lower():
  matches=[(n+1,t) for n,t in enumerate(CACHE[doc]) if anchor.lower() in t.lower()]
  if not matches: raise ValueError(f'Missing anchor: {doc} {anchor}')
  page,text=matches[0]
 i=text.lower().index(anchor.lower()); q=text[i:i+length]
 if i+length<len(text):q=q.rsplit(' ',1)[0]
 return dict(doc_id=doc,page=page,section=section,quote=q,quote_sha=hashlib.sha256(q.encode()).hexdigest())
def term(value,*args):return dict(value=value,clause_ref=quote(*args))
common={'rules_version':'1.0.0-demo','sample_notice':'Sample terms from public policy wording — education only','specific_list':['cataract'],'copay_pct':0,'copay_clause':None,'instant_cover':None,'instant_conditions':[],'instant_conditions_clause':None,'exclusions':[{'key':'unproven_treatment','text_en':'Unproven treatments: see exact exclusion and its scope.','text_hi':'अप्रमाणित उपचार: पूरा अपवाद देखें।'}]}
a=dict(common,plan_id='optima_secure',display_label='Plan A',product_name='HDFC ERGO my:Optima Secure',uin='HDFHLIP26058V082526',source_doc='optima_secure_current',
 initial_wait=term(30,'optima_secure_current',32,'C.1.c Excl03','illness within 30 days'),
 ped_wait=term(36,'optima_secure_current',30,'C.1.a Excl01','expiry of 36 months'),
 specific_wait=term(24,'optima_secure_current',31,'C.1.b Excl02','expiry of 24 months'),
 moratorium=term(60,'optima_secure_current',36,'D.1.6','After completion of sixty'),
 free_look=term(30,'optima_secure_current',37,'D.1.8','free look period of thirty'),
 room_rent=quote('optima_secure_current',11,'B.1.1','Room rent limit shall'),
 specific_list_clause=quote('optima_secure_current',31,'C.1.b list','Cataract and other'),
 exclusion_clause=quote('optima_secure_current',34,'C.2 Excl16','Unproven'),
 consumables_covered=True,consumables_clause=quote('optima_secure_current',16,'B.2.3 Protect Benefit','The Company shall indemnify the Insured Person for the Non'),
 assumptions=['Current downloaded wording UIN differs from architecture; source pinned by SHA256.','Optima Secure with default Protect Benefit retained; example non-medical items assumed listed in Annexure B.','No voluntary deductible or room modification. Independent claims; no reinstatement or bonus modeled.'])
b=dict(common,plan_id='care_supreme_ic',display_label='Plan B',product_name='Care Supreme + Instant Cover',uin='CHIHLIP25047V022425',source_doc='care_supreme',
 initial_wait=term(30,'care_supreme',35,'4.1(a)(iii) Excl03','illness within 30 days'),
 ped_wait=term(36,'care_supreme',33,'4.1(a)(i) Excl01','expiry of 36'),
 specific_wait=term(24,'care_supreme',34,'4.1(a)(ii) Excl02','expiry of 24'),
 moratorium=term(60,'care_supreme',46,'5.12','After completion of five'),
 free_look=term(30,'care_supreme',47,'5.15','free look period of thirty'),
 room_rent=quote('care_supreme',20,'3.1(ix)','The eligible Room Rent'),
 specific_list_clause=quote('care_supreme',34,'4.1(a)(ii) list','4. Cataract'),
 exclusion_clause=quote('care_supreme',38,'4.1(b) Excl16','Unproven Treatments'),
 instant_cover=term(31,'care_supreme',25,'3.2.5','the 31st day'),
 instant_conditions=['diabetes','hypertension','hyperlipidemia','asthma'],instant_conditions_clause=quote('care_supreme',24,'3.2.5','waive off'),
 consumables_covered=False,consumables_clause=quote('care_supreme',38,'4.2(1)','Any item or condition or treatment specified'),
 assumptions=['Paid Instant Cover selected on first policy; declared conditions assumed accepted by insurer.','Smart Select not selected: no automatic 20% outside-listed-hospital copay.','Claim Shield not selected; illustrative non-medical share is not payable.'])
c=dict(common,plan_id='tata_premier',display_label='Plan C',product_name='Tata AIG MediCare Premier',uin='TATHLIP26052V052526',source_doc='tata_premier',
 initial_wait=term(30,'tata_premier',34,'C.i.1.i Excl03','illness within 30 days'),
 ped_wait=term(24,'tata_premier',36,'C.i.1.iii Excl01','expiry of 24'),
 specific_wait=term(24,'tata_premier',34,'C.i.1.ii Excl02','expiry of 24'),
 moratorium=term(60,'tata_premier',44,'D.12','After completion of five'),
 free_look=term(30,'tata_premier',45,'D.14','free look period of thirty'),
 room_rent=quote('tata_premier',11,'B1 In-patient treatment','We will cover for expenses for hospitalization'),
 specific_list_clause=quote('tata_premier',35,'C.i.1.ii list','Cataract'),
 exclusion_clause=quote('tata_premier',37,'C.i.2 Excl16','Unproven treatments (Code'),
 consumables_covered=True,consumables_clause=quote('tata_premier',16,'B12 Consumables Benefit','We will pay for expenses incurred, for specified consumables'),
 assumptions=['Example consumables assumed to be on the specified covered list; excluded items remain excluded.','No voluntary deductible or copay assumed; actual issued schedule takes precedence.'])
for plan in [a,b,c]:
 (ROOT/f'data/plans/plan_{plan["display_label"][-1].lower()}.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
 print(plan['display_label'],plan['uin'],'authored')
