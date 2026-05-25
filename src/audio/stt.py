from faster_whisper import WhisperModel
import queue
import sounddevice as sd
import numpy as np

class WhisperSTT:
    def __init__(self):
        self.samplerate = 16000
        self.block_duration = 0.5
        self.chunk_duration = 2
        self.channels = 1

        self.lenguage = "en"

        self.frames_per_block = int(self.samplerate * self.block_duration)
        self.frames_per_chunk = int(self.samplerate * self.chunk_duration)

        self.audio_queue = queue.Queue()
        self.audio_buffer = []

        self.model_size = "medium.en"
        self.device = "cuda"
        self.comptute_type = "float32"

        self.model = WhisperModel(
            self.model_size, 
            device=self.device, 
            compute_type=self.comptute_type
            )
            
        self.phrase = []

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(indata.copy())

    def recorder(self):
        with sd.InputStream(
                samplerate=self.samplerate, 
                channels=self.channels,
                callback=self.audio_callback,
                blocksize=self.frames_per_block):
            print("Listening... ")
            while True:
                sd.sleep(100)

    def transcriber(self):
        while True:
            block = self.audio_queue.get()
            self.audio_buffer.append(block)

            total_frames = sum(len(b) for b in self.audio_buffer)
            if total_frames >= self.frames_per_block:
                audio_data = np.concatenate(self.audio_buffer)[:self.frames_per_chunk]

                self.audio_buffer = []
                audio_data = audio_data.flatten().astype(np.float32)

                segments, info = self.model.transcribe(
                    audio_data,
                    language=self.lenguage,
                    vad_filter=True,
                    condition_on_previous_text=False,
                    beam_size=1
                )
                
                for segment in segments:
                    print(segment.text)
                    self.phrase.append(segment.text)
                    print(len(self.phrase))
                    if(len(self.phrase) > 10):
                        text = " ".join(self.phrase)
                        print(text)
                        self.phrase = []
                        return text