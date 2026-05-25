import pyaudio
from piper import PiperVoice
from config.config import TTS_DIR 

class PiperTTS():
    def __init__(self):
        
        # self.model_path = f"{TTS_DIR}/en_US-kristin-medium.onnx"
        self.model_path = f"{TTS_DIR}/pt_BR-cadu-medium.onnx"
        self.voice = PiperVoice.load(self.model_path)

        self.pyAudio = pyaudio.PyAudio()

        self.stream = self.pyAudio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.voice.config.sample_rate,
            output=True
        )

    def speak(self,text):
        for audio_bytes in self.voice.synthesize(text):
            self.stream.write(audio_bytes.audio_int16_bytes)