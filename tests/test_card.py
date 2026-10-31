from tests.conftest import start,interview
async def test_card_requires_individual_confirm_and_shows_clause_dates(client):
 j,h=await start(client);body=await interview(client,j,h)
 for l in body['lines']:
  await client.post(f'/v1/lines/{l["id"]}/confirm',headers=h,json={'version':l['version']})
 r=await client.post(f'/v1/journeys/{j}/select',headers=h,json={'plan_id':'care_supreme_ic','d0':'2026-10-31','receipt':'2026-11-02'})
 assert r.status_code==200,r.text
 card=r.json();rows={row['key']:row for row in card['rows']}
 assert rows['hypertension']['fact']['value']=='2026-11-30'
 assert rows['free_look']['fact']['value']=='2026-12-01'
 assert rows['audit_nudge']['fact']['value']=='2026-11-13'
 assert len(card['upcoming'])==len(card['rows'])
 assert all(row['label_en'] and row['label_hi'] and row['fact']['clause_ref']['quote'] for row in card['rows'])
 other,ho=await start(client)
 assert (await client.get(f'/v1/journeys/{j}/card',headers=ho)).status_code==404
async def test_advisor_button_records_real_request(client):
 j,h=await start(client)
 r=await client.post(f'/v1/journeys/{j}/advisor',headers=h)
 assert r.status_code==200 and r.json()['request_id'] and r.json()['label']=='Pilot callback within 24 h'
