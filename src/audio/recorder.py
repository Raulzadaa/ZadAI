import sounddevice as sd
import numpy as np
from scipy.io import wavfile

from config.config import AUDIO_FILE

class Recorder:
    def __init__(self):
            self.samplerate = 16000
            self.wav_file = AUDIO_FILE

            self.silence_threshold = 0.7
            self.silence_timeout = 5

            self.record_audio = []
            self.seconds_in_silence = 0.0
            self.chunck_duration = 0.1

    def callback(self, indata, frames, time , status):
       
       volume = np.sqrt(np.mean(indata**2))

       self.record_audio.append(indata.copy())

       if volume < self.silence_threshold:
           self.seconds_in_silence += self.chunck_duration
       else:
           self.seconds_in_silence = 0.0


    def create_wav_file(self):
        print("Start Listening... ")

        self.record_audio = []
        self.seconds_in_silence = 0.0

        with sd.InputStream(
            samplerate=self.samplerate,
            channels=1,
            callback=self.callback,
            blocksize=int(self.samplerate * self.chunck_duration)
        ):
            while True:
                sd.sleep(100)
                if self.seconds_in_silence >= self.silence_timeout:
                    print("Stop Recording... ")
                    break

        audio = np.concatenate(self.record_audio , axis = 0 )
        audio_int16 = (audio * 32767).astype(np.int16)

        wavfile.write(self.wav_file, self.samplerate, audio_int16)
        