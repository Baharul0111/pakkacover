from io import BytesIO
import pytest
from PIL import Image
from apps.api.app.medicine import Reading,agreement,normalize_reading
from apps.api.app.media_worker import image_clean

def reading(salt='Telmisartan',strength='40 mg',visible='Telma 40 Telmisartan Tablets IP 40 mg'):
 return Reading(source_type='printed',brand='Telma 40',salt_text=salt,strength=strength,form='tablet',visible_text=visible,unreadable=[])
def test_two_reader_agreement_still_requires_human_condition():
 out=agreement([reading(),reading()]);assert out['status']=='agree'
 assert out['must_ask_indication'] and 'condition' not in out['candidates'][0]
def test_disagreement_is_never_resolved_by_guessing():
 r=reading('Amlodipine','5 mg','Amlodipine 5 mg')
 out=agreement([reading(),r]);assert out['status']=='choose' and len(out['candidates'])==2
def test_blurred_or_empty_photo_is_ask_buyer():
 r=Reading(source_type='unclear',brand='',salt_text='',strength='',form='',visible_text='',unreadable=['blur'])
 assert agreement([r,r])['status']=='unreadable'
def test_invented_salt_or_strength_rejected():
 assert normalize_reading(reading('Metformin')) is None
 assert normalize_reading(reading(strength='80 mg')) is None
 assert normalize_reading(reading('Notarealmedicine','5 mg','Notarealmedicine 5 mg')) is None
def test_one_reader_failure_is_amber_choose():
 assert agreement([reading(),None])['status']=='choose'
def test_exif_is_stripped_and_dimensions_bounded():
 img=Image.new('RGB',(2000,1000),'white');f=BytesIO();img.save(f,format='JPEG',exif=Image.Exif())
 clean=image_clean(f.getvalue());result=Image.open(BytesIO(clean))
 assert max(result.size)<=1600 and not result.getexif()
def test_oversized_pixel_dimensions_rejected():
 img=Image.new('1',(4000,4000));f=BytesIO();img.save(f,format='PNG')
 with pytest.raises(ValueError,match='image_pixel_limit'):image_clean(f.getvalue())

def test_handwriting_is_declined_even_when_readable():
 r=reading();r.source_type='handwritten'
 assert agreement([r,r])['status']=='unreadable'
def test_strength_units_cannot_be_invented():
 assert normalize_reading(reading(strength='40 mcg')) is None
