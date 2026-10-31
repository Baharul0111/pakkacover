from datetime import date,timedelta
from decimal import Decimal
import pytest
from hypothesis import given,strategies as st
from apps.api.app.engine.rules import plans,Claim,cover_start,payout,promise,simulate

D0=date(2026,10,31)

def test_sunita_hand_computed_fixture():
 rows=simulate(D0,['hypertension'],52)
 assert [r['display_label'] for r in rows]==['Plan B','Plan C','Plan A']
 assert [r['total'] for r in rows]==[644000,300000,100000]
 assert [[c['amount'] for c in r['claims']] for r in rows]==[[184000,184000,184000,92000,0],[0,0,200000,100000,0],[0,0,0,100000,0]]
 assert cover_start(plans()['care_supreme_ic'],D0,'hypertension',{'hypertension'}).value=='2026-11-30'
 assert cover_start(plans()['tata_premier'],D0,'hypertension',{'hypertension'}).value=='2028-10-31'
 assert cover_start(plans()['optima_secure'],D0,'hypertension',{'hypertension'}).value=='2029-10-31'

@pytest.mark.parametrize('start',[date(2024,2,29),date(2025,1,31),date(2026,10,31),date(2027,12,31)])
def test_boundary_sweep(start):
 for plan in plans().values():
  for condition,kind in [('hypertension','illness'),('cataract','specific')]:
   boundary=date.fromisoformat(cover_start(plan,start,condition,{condition},kind).value)
   for delta in range(-3,4):
    result=payout(plan,start,{condition},Claim(date=boundary+timedelta(days=delta),condition_key=condition,kind=kind,billed_inr=200000))
    assert (result['amount']>0)==(delta>=0)

def test_day_count_and_leap_year():
 plan=plans()['care_supreme_ic'];rows={r['key']:r['fact'].value for r in promise(plan,date(2024,2,29),date(2024,2,29),['hypertension'])}
 assert rows['illness']=='2024-03-30'
 assert rows['free_look']=='2024-03-29'
 assert rows['audit_nudge']=='2024-03-11'
 assert rows['moratorium']=='2029-02-28'

def test_specific_and_ped_use_longer_wait():
 p=plans()['optima_secure']
 assert cover_start(p,D0,'cataract',{'cataract'}).value=='2029-10-31'

def test_instant_cover_not_applied_to_unknown_condition():
 p=plans()['care_supreme_ic']
 assert cover_start(p,D0,'unknown',{'unknown'}).value=='2029-10-31'

@given(st.integers(0,10000000),st.integers(1,1000000),st.integers(0,100))
def test_money_bounds_and_monotonic_copay(bill,si,copay):
 for plan in plans().values():
  c=Claim(date=D0,condition_key='accident',kind='accident',billed_inr=bill,sum_insured=si)
  before=payout(plan,D0,{'hypertension'},c)['amount']
  after=payout(plan,D0,{'hypertension'},c.model_copy(update={'copay_pct':Decimal(copay)}))['amount']
  assert 0<=after<=before<=min(bill,si)

def test_permanent_exclusion():
 for p in plans().values():
  assert payout(p,D0,set(),Claim(date=date(2030,1,1),condition_key='unproven_treatment',billed_inr=100000))['amount']==0

def test_negative_money_is_rejected():
 with pytest.raises(ValueError):Claim(date=D0,condition_key='accident',billed_inr=-1)
