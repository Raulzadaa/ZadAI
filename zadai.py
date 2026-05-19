from whisperz import Whisperz
import threading
print("rodou")
whisperz = Whisperz()

threading.Thread(target=whisperz.recorder, daemon=True).start()

whisperz.transcriber()