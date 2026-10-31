import pytest
from apps.api.app.gateway import numeric_guard,guarded_question
from apps.api.app.interview import Turn,Slot,validate_turn
@pytest.mark.parametrize('i',range(50))
def test_g7_zero_invented_numbers(i):
 bad=f'Your cover starts in {i+100} days and pays ₹{i+10000}.'
 assert guarded_question(bad,'BP since 2019, Telma 40','standard question')=='standard question'
def test_numbers_already_in_source_and_hindi_words():
 assert numeric_guard('Telmisartan 40','Telma 40')
 assert numeric_guard('52','बावन साल')
 assert not numeric_guard('41','Telma 40')
def test_false_quote_and_number_fail():
 node={'key':'since'}
 with pytest.raises(ValueError):validate_turn(Turn(slots=[Slot(key='since',value='2018',quote='since 2019')],question='',needs_clarification=False),'since 2019',node)
 with pytest.raises(ValueError):validate_turn(Turn(slots=[Slot(key='since',value='2019',quote='2019')],question='',needs_clarification=False),'I do not know',node)
