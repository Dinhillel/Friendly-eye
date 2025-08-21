from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "data" / "models"
AUDIO_DIR = ROOT / "data" / "audio"

YOLO_MODEL = str(MODELS_DIR / "yolov8n.pt")
YOLO_CONF = 0.35
CAM_INDEX = 0
CAM_WIDTH = 1280
CAM_HEIGHT = 720
SHOW_WINDOW = True

WHISPER_SIZE = "base"
WHISPER_LANGUAGE = "he"
AUDIO_TMP = str(AUDIO_DIR / "query.wav")

T5_MODEL = "google/t5-v1_1-small"
MAX_NEW_TOKENS = 64

TTS_RATE = 180
TTS_VOLUME = 1.0
TTS_VOICE = None

FPS_LIMIT = 30
