import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

TTS_DIR = os.path.join(MODELS_DIR, "tts")

WAKE_WORD_DIR = os.path.join(MODELS_DIR, "wakeword")