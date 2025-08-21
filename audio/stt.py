## Speech-to-Text – transcribes user voice commands 👂
import sounddevice as sd
from scipy.io.wavfile import write
import os

# audio/stt.py
try:
    import whisper
except ImportError:
    whisper = None

def record_to_file(path: str, seconds: float = 3.0, sr: int = 16000) -> str:
    """
    מקליט קול למשך 'seconds' שניות ושומר בקובץ WAV בנתיב path
    """
    audio = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="int16")
    sd.wait()
    write(path, sr, audio)
    return path

def transcribe(path: str, model_size: str = "base", language: str | None = None) -> str:
    """
    ממיר קול לטקסט באמצעות מודל Whisper
    """
    if whisper is None:
        raise RuntimeError("Whisper not installed. Run: pip install openai-whisper")
    
    model = whisper.load_model(model_size)
    result = model.transcribe(path, language=language)
    return result.get("text", "").strip()

