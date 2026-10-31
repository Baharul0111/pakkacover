"""Model-free policy calculations. All money uses Decimal; dates use calendar arithmetic."""
from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal, ROUND_FLOOR
from functools import lru_cache
from pathlib import Path
from typing import Literal
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, ConfigDict, Field

ROOT = Path(__file__).resolve().parents[4]

class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid')

class Clause(Strict):
    doc_id: str
    page: int = Field(ge=1)
    section: str
    quote: str = Field(min_length=1)
    quote_sha: str

class Exclusion(Strict):
    key:str
    text_en:str
    text_hi:str
    clause_ref:Clause

class Term(Strict):
    value: int = Field(ge=0)
    clause_ref: Clause

class Plan(Strict):
    plan_id: str
    display_label: str
    product_name: str
    uin: str
    source_doc: str
    rules_version: str = '1.0.0-demo'
    sample_notice: str = 'Sample terms from public policy wording — education only'
    initial_wait: Term
    ped_wait: Term
    specific_wait: Term
    moratorium: Term
    free_look: Term
    room_rent: Clause
    specific_list: list[str]
    specific_list_clause: Clause
    exclusions: list[Exclusion]
    exclusion_clause: Clause
    instant_cover: Term | None = None
    instant_conditions: list[str] = []
    instant_conditions_clause: Clause | None = None
    copay_pct: int = Field(default=0, ge=0, le=100)
    copay_clause: Clause | None = None
    consumables_covered: bool = False
    consumables_clause: Clause
    assumptions: list[str] = []

class Fact(Strict):
    value: str | int
    rule_id: str
    clause_ref: Clause
    explain_en: str
    explain_hi: str

class Claim(Strict):
    date: date
    condition_key: str
    kind: Literal['illness','accident','specific'] = 'illness'
    billed_inr: Decimal = Field(ge=0, le=100000000)
    consumables_share: Decimal = Field(default=Decimal('0.08'), ge=0, le=1)
    sum_insured: Decimal = Field(default=Decimal('500000'),gt=0,le=100000000)
    deductible_inr: Decimal = Field(default=Decimal(0),ge=0)
    copay_pct: Decimal = Field(default=Decimal(0),ge=0,le=100)
    sub_limit_inr: Decimal | None = Field(default=None,ge=0)

@lru_cache
def plans() -> dict[str,Plan]:
    return {p.plan_id:p for path in sorted((ROOT/'data/plans').glob('plan_*.json')) if (p:=Plan.model_validate_json(path.read_text()))}

def fact(value, rule_id, clause, en, hi='') -> Fact:
    return Fact(value=value.isoformat() if isinstance(value,date) else value,rule_id=rule_id,clause_ref=clause,explain_en=en,explain_hi=hi or en)

def cover_start(plan: Plan, d0: date, condition: str, declared: set[str], kind='illness') -> Fact:
    if kind=='accident':
        return fact(d0,'accident',plan.initial_wait.clause_ref,'Accidents bypass the initial illness waiting period.','दुर्घटना पर शुरुआती बीमारी की प्रतीक्षा लागू नहीं होती।')
    candidates=[(d0+timedelta(days=plan.initial_wait.value),'initial_wait',plan.initial_wait.clause_ref)]
    if condition in declared:
        if plan.instant_cover and condition in plan.instant_conditions:
            candidates.append((d0+timedelta(days=plan.instant_cover.value-1),'instant_cover',plan.instant_cover.clause_ref))
        else:
            candidates.append((d0+relativedelta(months=plan.ped_wait.value),'ped_wait',plan.ped_wait.clause_ref))
    if condition in plan.specific_list:
        candidates.append((d0+relativedelta(months=plan.specific_wait.value),'specific_wait',plan.specific_wait.clause_ref))
    start,rule,clause=max(candidates,key=lambda c:(c[0],{'initial_wait':0,'instant_cover':1,'ped_wait':1,'specific_wait':2}[c[1]]))
    return fact(start,rule,clause,'The latest applicable waiting-period end controls this illustrative claim. Confirm boundary dates with the insurer/advisor.','लागू प्रतीक्षा अवधियों में सबसे बाद की तारीख ली गई है। सीमा की तारीख सलाहकार से जाँचें।')

def payout(plan:Plan,d0:date,declared:set[str],claim:Claim)->dict:
    start=cover_start(plan,d0,claim.condition_key,declared,claim.kind)
    steps=[start]
    if claim.date < date.fromisoformat(str(start.value)):
        return {'amount':0,'fact':fact(0,start.rule_id,start.clause_ref,'Claim is before its applicable cover date.','दावा कवर शुरू होने से पहले है।'),'steps':steps}
    if claim.condition_key in {x.key for x in plan.exclusions}:
        return {'amount':0,'fact':fact(0,'permanent_exclusion',plan.exclusion_clause,'This example matches a permanent exclusion.'),'steps':steps}
    eligible=claim.billed_inr
    calculation=[f'Example bill ₹{claim.billed_inr}']
    if not plan.consumables_covered:
        eligible*=1-claim.consumables_share
        calculation.append(f'Less {claim.consumables_share*100}% assumed non-payable items = ₹{eligible}')
        steps.append(fact(str(eligible),'non_payable_items',plan.consumables_clause,'Illustrative non-payable items are deducted; the actual item list must be checked.'))
    if claim.sub_limit_inr is not None:
        eligible=min(eligible,claim.sub_limit_inr)
        calculation.append(f'Condition cap ₹{claim.sub_limit_inr} gives ₹{eligible}')
    eligible=max(Decimal(0),eligible-claim.deductible_inr)
    calculation.append(f'Assumed deductible ₹{claim.deductible_inr}; assumed co-pay {claim.copay_pct+Decimal(plan.copay_pct)}%')
    eligible*=1-min(Decimal(100),claim.copay_pct+Decimal(plan.copay_pct))/100
    amount=int(min(claim.sum_insured,eligible).quantize(Decimal(1),rounding=ROUND_FLOOR))
    final=fact(amount,'illustrative_payout',plan.consumables_clause,'; '.join(calculation)+f'; cap ₹{claim.sum_insured}; payout rounded down = ₹{amount}. Independent examples, not one policy-year total.','; '.join(calculation)+f'; बीमा राशि की मानी हुई सीमा ₹{claim.sum_insured}; रुपये में नीचे की ओर पूर्णांक = ₹{amount}। हर उदाहरण अलग है।')
    steps.append(final)
    return {'amount':amount,'fact':final,'steps':steps}

def scenarios(d0:date,conditions:list[str],age:int=52,amounts:dict|None=None):
    amounts=amounts or {}; result=[]
    for condition in sorted(set(conditions)):
        for month in (3,18,30):
            result.append({'label':f'{condition} · month {month}','claim':Claim(date=d0+relativedelta(months=month),condition_key=condition,billed_inr=amounts.get('illness',200000))})
    result.append({'label':'Accident · day 10','claim':Claim(date=d0+timedelta(days=9),condition_key='accident',kind='accident',billed_inr=amounts.get('accident',100000))})
    if age>=50:
        result.append({'label':'Cataract · month 20','claim':Claim(date=d0+relativedelta(months=20),condition_key='cataract',kind='specific',billed_inr=amounts.get('cataract',60000))})
    return result

def simulate(d0:date,conditions:list[str],age:int=52,amounts:dict|None=None):
    rows=[]
    for plan in plans().values():
        claims=[]
        for item in scenarios(d0,conditions,age,amounts):
            result=payout(plan,d0,set(conditions),item['claim'])
            claims.append({'label':item['label'],'date':item['claim'].date,'billed':int(item['claim'].billed_inr),**result})
        rows.append({'plan_id':plan.plan_id,'display_label':plan.display_label,'product_name':plan.product_name,'total':sum(c['amount'] for c in claims),'claims':claims,'addon_required':bool(plan.instant_cover),'sample_notice':plan.sample_notice,'assumptions':plan.assumptions})
    return sorted(rows,key=lambda r:(-r['total'],r['addon_required'],r['display_label']))

def promise(plan:Plan,d0:date,receipt:date,conditions:list[str])->list[dict]:
    rows=[{'key':'accident','label_en':'Accidents','label_hi':'दुर्घटनाएँ','fact':cover_start(plan,d0,'accident',set(),'accident')},
          {'key':'illness','label_en':'Most illnesses','label_hi':'अधिकांश बीमारियाँ','fact':cover_start(plan,d0,'illness',set())}]
    for c in sorted(set(conditions)):
        rows.append({'key':c,'label_en':f'Declared {c}','label_hi':'घोषित बीमारी: '+{'hypertension':'उच्च रक्तचाप','diabetes':'मधुमेह'}.get(c,c),'fact':cover_start(plan,d0,c,set(conditions))})
    rows.extend([
        {'key':'specific','label_en':'Listed procedures (e.g. cataract)','label_hi':'सूचीबद्ध ऑपरेशन (जैसे मोतियाबिंद)','fact':cover_start(plan,d0,'cataract',set(conditions),'specific')},
        {'key':'moratorium','label_en':'Moratorium (fraud exception applies)','label_hi':'मोराटोरियम (धोखाधड़ी अपवाद लागू)','fact':fact(d0+relativedelta(months=plan.moratorium.value),'moratorium',plan.moratorium.clause_ref,'Continuous cover assumed; established fraud remains an exception.')},
        {'key':'free_look','label_en':'Act by: free-look deadline','label_hi':'फ्री-लुक: इस तारीख तक कदम उठाएँ','fact':fact(receipt+timedelta(days=plan.free_look.value-1),'free_look',plan.free_look.clause_ref,'Conservative inclusive day count from receipt; refund deductions and no-claim terms apply.')},
        {'key':'audit_nudge','label_en':'Day-12 policy check','label_hi':'बारहवें दिन पॉलिसी की जाँच','fact':fact(receipt+timedelta(days=11),'audit_nudge',plan.free_look.clause_ref,'Day 12 is our reminder within the free-look window, not an insurer deadline.')},
    ])
    return rows
