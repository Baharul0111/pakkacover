import copy,json
from pathlib import Path
import pytest
from scripts.check_quotes import check_all,check_plan,ROOT

def test_g2_all_public_wording_quotes():assert check_all()>=30

def test_g2_rejects_modified_clause():
 plan=json.loads((ROOT/'data/plans/plan_b.json').read_text())
 plan['ped_wait']['clause_ref']['quote']='A fabricated policy term'
 with pytest.raises(AssertionError,match='quote hash changed'):
  check_plan(plan,json.loads((ROOT/'data/plans/sources.json').read_text()),{})

def test_g2_rejects_wrong_uin():
 plan=json.loads((ROOT/'data/plans/plan_c.json').read_text());plan['uin']='WRONG_UIN'
 with pytest.raises(AssertionError,match='UIN mismatch'):
  check_plan(plan,json.loads((ROOT/'data/plans/sources.json').read_text()),{})
