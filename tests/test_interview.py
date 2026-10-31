import pytest
from apps.api.app.interview import canonical_condition,explicit_condition_answer,extract
from apps.api.app import gateway as gw
@pytest.mark.parametrize('value',['High blood pressure','बी पी है','माँ को बीपी है','Hypertension','उच्च रक्तचाप'])
def test_bp_aliases_are_explicit_not_guessed(value):assert canonical_condition(value)=='hypertension'
@pytest.mark.parametrize('value',['Mujhe BP nahi hai','No high blood pressure','मुझे बीपी नहीं है','Sugar border pe hai'])
def test_literal_condition_fallback_does_not_invert_negations(value):assert explicit_condition_answer({'key':'conditions'},value) is None
async def test_bad_model_quote_can_fall_back_only_to_explicit_source_condition(monkeypatch):
 async def moderate(**kwargs):return None
 async def invalid(*args,**kwargs):raise ValueError('unaligned_quote')
 monkeypatch.setattr(gw,'moderate',moderate);monkeypatch.setattr(gw,'structured',invalid)
 values,source=await extract({'key':'conditions','en':'Any illness?','choices':[]},'मेरी माँ को बीपी है।')
 assert values=={'conditions':'BP / hypertension'} and source=='source_anchored_condition_fallback'
 values,_=await extract({'key':'conditions','en':'Any illness?','choices':[]},'कोई जानकारी नहीं।')
 assert values=={}
