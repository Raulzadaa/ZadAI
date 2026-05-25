from src.audio import WakeWordDetector , WhisperSTT , PiperTTS
from src.brain import LLMModule
import threading

class ZadAI:
    def __init__(self):

        self.wake_detector = WakeWordDetector()
        self.ears = WhisperSTT()
        self.brain = LLMModule()
        self.mouth = PiperTTS()

    def start(self):
        threading.Thread(target=self.ears.recorder, daemon=True).start()

        while True:
            # prompt = self.ears.transcriber()
            prompt = input("Write: ")
            text = self.brain.prompt(prompt)
            print(text)
            self.mouth.speak(text)

zadai = ZadAI()

zadai.start()