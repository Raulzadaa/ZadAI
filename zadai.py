from src.audio import WakeWordDetector , WhisperSTT , PiperTTS, Recorder
from src.brain import LLMModule
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
            self.recorder.create_wav_file()
            prompt = self.ears.transcriber()
            # prompt = input("Write: ")
            text = self.brain.prompt(prompt)
            print(text)
            self.mouth.speak(text)

zadai = ZadAI()

zadai.start()