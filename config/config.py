import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
MISC_DIR = os.path.join(BASE_DIR, "misc")

TTS_DIR = os.path.join(MODELS_DIR, "tts")
WAKE_WORD_DIR = os.path.join(MODELS_DIR, "wakeword")

AUDIO_FILE = f"{MISC_DIR}/audio.wav"