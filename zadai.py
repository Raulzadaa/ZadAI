import os
import threading

import uvicorn

from backend.src.audio import WakeWordDetector, WhisperSTT, PiperTTS, Recorder
from backend.src.brain import LLMModule
from backend.config.config import ONLY_TEXT
from backend.src.api import settings
from backend.src.api.main import app
from backend.src.api.zadai_client import brain_lock, set_brain
from backend.src.api.tunnel import Tunnel

class ZadAI:
    def __init__(self):
        self.wake_detector = WakeWordDetector()
        self.recorder = Recorder()
        self.ears = WhisperSTT()
        self.brain = LLMModule()
        self.mouth = PiperTTS()

    def start(self):
        while True:
            if ONLY_TEXT:
                prompt = input("Write: ")
            else:
                self.recorder.create_wav_file()
                prompt = self.ears.transcriber()

            with brain_lock:  # divide o modelo com as requisições da web
                text = self.brain.prompt(prompt)
            print(text)
            if not ONLY_TEXT:
                self.mouth.speak(text)


def start_web() -> uvicorn.Server:
    server = uvicorn.Server(uvicorn.Config(app, host=settings.HOST, port=settings.PORT, log_level="info", proxy_headers=True, forwarded_allow_ips="*"))
    threading.Thread(target=server.run, name="zadai-web", daemon=True).start()
    return server


if __name__ == "__main__":
    zadai = ZadAI()
    set_brain(zadai.brain)
    server = start_web()
    tunnel = Tunnel(settings.PORT).start() if settings.TUNNEL else None
    print(f"ZadAI web em http://{settings.HOST}:{settings.PORT}")
    try:
        zadai.start()
    except KeyboardInterrupt:
        pass
    finally:
        if tunnel:
            tunnel.stop()
        server.should_exit = True