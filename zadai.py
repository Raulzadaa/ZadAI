from src.audio import WakeWordDetector , WhisperSTT , PiperTTS, Recorder
from src.brain import LLMModule
from config.config import ONLY_TEXT
import threading

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
            
            text = self.brain.prompt(prompt)
            print(text)
            if not ONLY_TEXT:
                self.mouth.speak(text)

zadai = ZadAI()

zadai.start()