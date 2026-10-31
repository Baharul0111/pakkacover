from datetime import date
from apps.api.app.engine.rules import plans,cover_start
from apps.api.app.engine.comparison import comparison_details

def test_shared_timeline_uses_actual_dates_and_calendar_36_month_end():
 d0=date(2026,10,31);results={key:comparison_details(plan,d0,['hypertension']) for key,plan in plans().items()}
 b=results['care_supreme_ic'];c=results['tata_premier'];a=results['optima_secure']
 assert 0<b['timeline']['wait_percent']<5
 assert 60<c['timeline']['wait_percent']<70
 assert a['timeline']['wait_percent']==100
 assert {result['timeline']['end'] for result in results.values()}=={'2029-10-31'}
 assert [b['timeline']['wait_months'],c['timeline']['wait_months'],a['timeline']['wait_months']]==[1,24,36]
 for key,result in results.items():
  assert result['timeline']['covered_from']==cover_start(plans()[key],d0,'hypertension',{'hypertension'}).value
  assert len(result['for_you'])<=4
  for row in result['for_you']:
   for fact in row.get('facts',[row.get('fact')]):assert fact.clause_ref.quote and fact.clause_ref.page>=1
 assert any(row['kind']=='addon' for row in b['for_you'])
 assert all(row['kind']!='addon' for row in a['for_you']+c['for_you'])
 assert not any('20%' in row.get('label_en','') for result in results.values() for row in result['for_you'])

def test_no_declared_condition_has_no_bp_claim_or_addon_in_summary():
 result=comparison_details(plans()['care_supreme_ic'],date(2026,10,31),[])
 assert result['condition_start'] is None and result['timeline'] is None
 assert not any(row['kind'] in ('condition','addon') for row in result['for_you'])
