"""Generate a clearly labelled, in-memory issued-policy demo fixture."""
from io import BytesIO
from datetime import date,timedelta
from dateutil.relativedelta import relativedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
VARIANTS={'clean','m1_ped_addon_missing','m2_declared_condition_missing','m3_dob_wrong'}
def make_policy(plan,member,conditions,d0,variant='clean'):
 if variant not in VARIANTS:raise ValueError('unknown_variant')
 addon=bool(plan.instant_cover)
 ped=plan.ped_wait.value
 age=member['age']
 declared=', '.join(sorted(set(conditions))) or 'None'
 if variant=='m1_ped_addon_missing':addon=False;ped=36
 if variant=='m2_declared_condition_missing':declared='None'
 if variant=='m3_dob_wrong':age+=3
 expiry=d0+relativedelta(years=1)-timedelta(days=1)
 fields=[('Schedule',[
  ('Policy Number','SAMPLE-PC-2026'),('Plan Name',plan.product_name),('Plan UIN',plan.uin),('Policy Start',d0.isoformat()),('Policy Expiry',expiry.isoformat()),('Sum Insured','500000')]),
  ('Insured Member', [('Member Label','Member 1'),('Member Age',str(age)),('Member Sex',member['sex']),('Declared Conditions',declared)]),
  ('Optional Covers and Waiting Periods',[('Instant Cover','Yes' if addon else 'No'),('PED Waiting Months',str(ped)),('Initial Waiting Days',str(plan.initial_wait.value)),('Specific Waiting Months',str(plan.specific_wait.value))])]
 buffer=BytesIO();c=Canvas(buffer,pagesize=A4);width,height=A4
 c.setTitle('PakkaCover generated SAMPLE policy — no insurance issued')
 c.setFont('Helvetica-Bold',20);c.setFillColorRGB(.1,.25,.20);c.drawString(48,height-62,'PAKKACOVER | SAMPLE POLICY')
 c.setFont('Helvetica-Bold',10);c.setFillColorRGB(.7,.25,.12);c.drawString(48,height-86,'HACKATHON FIXTURE - NOT AN INSURANCE CONTRACT')
 y=height-130
 for section,pairs in fields:
  c.setFillColorRGB(.1,.25,.2);c.setFont('Helvetica-Bold',12);c.drawString(48,y,section);y-=25
  c.setFillColorRGB(.2,.2,.2);c.setFont('Helvetica',10)
  for key,val in pairs:
   c.drawString(48,y,f'{key}: {val}');y-=21
  y-=20
 c.setFont('Helvetica',9);c.setFillColorRGB(.5,.5,.5)
 c.drawString(48,68,'Fictional sample generated from the confirmed demo declaration.')
 c.drawString(48,52,'Only the quoted public wording is used for illustrative engine calculations.')
 c.save();return buffer.getvalue()
