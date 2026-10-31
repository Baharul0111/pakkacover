from tests.conftest import start,interview
async def test_card_requires_individual_confirm_and_shows_clause_dates(client):
 j,h=await start(client);body=await interview(client,j,h)
 for l in body['lines']:
  await client.post(f'/api/lines/{l["id"]}/confirm',headers=h,json={'version':l['version']})
 r=await client.post(f'/api/journeys/{j}/select',headers=h,json={'plan_id':'care_supreme_ic','d0':'2026-10-31','receipt':'2026-11-02'})
 assert r.status_code==200,r.text
 card=r.json();rows={row['key']:row for row in card['rows']}
 assert rows['hypertension']['fact']['value']=='2026-11-30'
 assert rows['free_look']['fact']['value']=='2026-12-01'
 assert rows['audit_nudge']['fact']['value']=='2026-11-13'
 assert len(card['upcoming'])==len(card['rows'])
 assert all(row['label_en'] and row['label_hi'] and row['fact']['clause_ref']['quote'] for row in card['rows'])
 other,ho=await start(client)
 assert (await client.get(f'/api/journeys/{j}/card',headers=ho)).status_code==404
async def test_advisor_button_records_real_request(client):
 j,h=await start(client)
 r=await client.post(f'/api/journeys/{j}/advisor',headers=h)
 assert r.status_code==200 and r.json()['request_id'] and r.json()['label']=='Pilot callback within 24 h'

async def test_comparison_timeline_dates_are_engine_facts_with_bp_clause(client):
 j,h=await start(client);body=await interview(client,j,h)
 for line in body['lines']:
  await client.post(f'/api/lines/{line["id"]}/confirm',headers=h,json={'version':line['version']})
 r=await client.post(f'/api/journeys/{j}/simulate',headers=h,json={'d0':'2026-10-31'})
 assert r.status_code==200
 rows=r.json()
 assert [row['condition_start']['value'] for row in rows]==['2026-11-30','2028-10-31','2029-10-31']
 assert '31st day' in rows[0]['condition_start']['clause_ref']['quote']
 assert [row['total'] for row in rows]==[644000,300000,100000]

async def test_select_all_three_plans_after_review_and_exact_reconfirmation(client):
 j,h=await start(client);body=await interview(client,j,h)
 for line in body['lines']:
  await client.post(f'/api/lines/{line["id"]}/confirm',headers=h,json={'version':line['version']})
 for plan in ['care_supreme_ic','tata_premier','optima_secure']:
  r=await client.post(f'/api/journeys/{j}/select',headers=h,json={'plan_id':plan,'d0':'2026-10-31','receipt':'2026-10-31'})
  assert r.status_code==200,r.text
 # Reopening creates a genuinely unanswered question. Route back to Talk, without
 # treating the former Check screen's confirmed count as authoritative.
 changed=next(line for line in body['lines'] if line['key']=='weight')
 await client.post(f'/api/lines/{changed["id"]}/reopen',headers=h)
 r=await client.post(f'/api/journeys/{j}/select',headers=h,json={'plan_id':'care_supreme_ic','d0':'2026-10-31','receipt':'2026-10-31'})
 assert r.status_code==409 and r.json()['detail']['phase']=='interview'
 assert r.json()['detail']['line_id']==changed['id'] and r.json()['detail']['question_key']=='weight'
 await client.post(f'/api/journeys/{j}/answer',headers=h,json={'text':'68 kilo'})
 r=await client.post(f'/api/journeys/{j}/select',headers=h,json={'plan_id':'care_supreme_ic','d0':'2026-10-31','receipt':'2026-10-31'})
 assert r.status_code==409 and r.json()['detail']['phase']=='review' and r.json()['detail']['line_id']==changed['id']
 stale=await client.post(f'/api/lines/{changed["id"]}/confirm',headers=h,json={'version':changed['version']})
 assert stale.status_code==409 and stale.json()['detail']['line_id']==changed['id']
 fresh=(await client.get(f'/api/journeys/{j}',headers=h)).json()
 line=next(line for line in fresh['lines'] if line['id']==changed['id'])
 assert (await client.post(f'/api/lines/{line["id"]}/confirm',headers=h,json={'version':line['version']})).status_code==200
 assert (await client.post(f'/api/journeys/{j}/select',headers=h,json={'plan_id':'care_supreme_ic','d0':'2026-10-31','receipt':'2026-10-31'})).status_code==200

async def test_fully_confirmed_old_journey_with_new_required_question_routes_to_talk(client):
 from apps.api.app.db import Session,Journey,Line
 from sqlalchemy import delete
 j,h=await start(client);body=await interview(client,j,h)
 for line in body['lines']:
  await client.post(f'/api/lines/{line["id"]}/confirm',headers=h,json={'version':line['version']})
 # Reproduce the observed old-session mismatch: all stored lines confirmed but
 # today's interview has a question that was not present when it was completed.
 async with Session() as s:
  journey=await s.get(Journey,j);slots=dict(journey.payload['slots']);slots.pop('treatment');journey.payload={**journey.payload,'slots':slots}
  await s.execute(delete(Line).where(Line.journey_id==j,Line.slot=='treatment'));await s.commit()
 r=await client.post(f'/api/journeys/{j}/select',headers=h,json={'plan_id':'care_supreme_ic','d0':'2026-10-31','receipt':'2026-10-31'})
 assert r.status_code==409 and r.json()['detail']=={'code':'review_required','phase':'interview','line_id':None,'question_key':'treatment'}
