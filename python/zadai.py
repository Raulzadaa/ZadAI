from whisperz import Whisperz
import threading

whisperz = Whisperz()

while True:
    prompt = input("Write: ")
    print(whisperz.llmz.prompt(prompt))

# threading.Thread(target=whisperz.recorder, daemon=True).start()

# whisperz.transcriber()