from faster_whisper import WhisperModel
from config.config import AUDIO_FILE

import queue
import sounddevice as sd
import numpy as np

class WhisperSTT:
    def __init__(self):

        self.lenguage = "pt"

        self.model_size = "medium"
        self.device = "cuda"
        self.comptute_type = "float16"

        self.model = WhisperModel(
            self.model_size, 
            device=self.device, 
            compute_type=self.comptute_type
            )
            
        self.phrase = []
        
    def transcriber(self):
        segments, info = self.model.transcribe(AUDIO_FILE, beam_size=6)
        for segment in segments:
            print(segment.text)
            return segment.text
