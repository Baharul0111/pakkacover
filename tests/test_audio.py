from io import BytesIO
import wave,pytest
from apps.api.app.media_worker import audio_duration

def wav(seconds):
 out=BytesIO()
 with wave.open(out,'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000);w.writeframes(b'\0\0'*int(seconds*16000))
 return out.getvalue()
def test_audio_duration_is_measured_instead_of_trusting_client():
 assert abs(audio_duration(wav(2))-2)<.1
 with pytest.raises(ValueError,match='audio_duration_limit'):audio_duration(wav(27))
