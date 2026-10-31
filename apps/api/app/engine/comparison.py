"""Short comparison facts and a shared calendar scale, calculated without models."""
from datetime import date
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from apps.api.app.engine.rules import cover_start,fact

def comparison_details(plan,d0:date,conditions:list[str]):
 condition='hypertension' if 'hypertension' in conditions else (conditions[0] if conditions else None)
 hospital=cover_start(plan,d0,'illness',set())
 accident=cover_start(plan,d0,'accident',set(),'accident')
 hospital_day=(date.fromisoformat(hospital.value)-d0).days+1
 accident_day=(date.fromisoformat(accident.value)-d0).days+1
 rows=[{'kind':'covers','label_en':f'Hospital: day {hospital_day} · Accident: day {accident_day}','label_hi':f'अस्पताल: दिन {hospital_day} · दुर्घटना: दिन {accident_day}','facts':[hospital,accident]}]
 start=cover_start(plan,d0,condition,set(conditions)) if condition else None
 timeline=None
 if start:
  covered=date.fromisoformat(start.value);delta=relativedelta(covered,d0)
  months=delta.years*12+delta.months+int(delta.days>0)
  approximate=delta.days>0
  end=d0+relativedelta(months=36)
  percentage=max(Decimal(0),min(Decimal(100),Decimal((covered-d0).days)*100/Decimal((end-d0).days)))
  timeline={'start':d0.isoformat(),'end':end.isoformat(),'covered_from':covered.isoformat(),'months':36,'wait_percent':round(float(percentage),4),'wait_months':months,'approximate_months':approximate}
  rows.append({'kind':'condition','condition_key':condition,'date':covered.isoformat(),'months':months,'approximate':approximate,'fact':start})
 if plan.instant_cover and any(c in plan.instant_conditions for c in conditions):
  rows.append({'kind':'addon','label_en':'Instant Cover add-on needed','label_hi':'Instant Cover ऐड-ऑन ज़रूरी','fact':fact('required','instant_cover_required',plan.instant_cover.clause_ref,'This date assumes the paid Instant Cover add-on is selected and accepted.','यह तारीख भुगतान वाले Instant Cover ऐड-ऑन की स्वीकृति मानती है।')})
 if plan.copay_pct and plan.copay_clause:
  watch=fact(plan.copay_pct,'copay',plan.copay_clause,'The modelled co-pay is deducted from eligible claim expenses.','पात्र खर्च से मानी हुई सह-भुगतान राशि घटती है।')
  en=f'Co-pay: {plan.copay_pct}%';hi=f'सह-भुगतान: {plan.copay_pct}%'
 else:
  # Do not invent a cap or apply optional Smart Select to the base Care plan.
  no_limit="'No limit'" in plan.room_rent.quote
  actuals='At Actuals' in plan.room_rent.quote
  en='Room rent: check issued schedule' if not no_limit else 'Room rent: no separate limit'
  hi='कमरे का किराया: जारी शेड्यूल जाँचें' if not no_limit else 'कमरे के किराये की अलग सीमा नहीं'
  explanation='Room rent is at actuals unless the issued schedule says otherwise.' if actuals else 'No separate room-charge restriction in this sample wording.' if no_limit else 'This pinned hospitalization clause does not establish a room-rent cap. Verify the issued schedule with the insurer.'
  watch=fact('at_actuals_subject_to_schedule' if actuals else 'no_separate_limit' if no_limit else 'verify_schedule','room_rent_check',plan.room_rent,explanation,'कमरे की शर्त जारी शेड्यूल और बीमा कंपनी से जाँचें।')
 rows.append({'kind':'watch','label_en':en,'label_hi':hi,'fact':watch})
 return {'condition_key':condition,'condition_start':start,'for_you':rows,'timeline':timeline}
