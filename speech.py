import sounddevice as sd
import numpy as np
import queue
import json
from vosk import Model, KaldiRecognizer
from datetime import datetime
# Set up audio capture parameters

#print(sd.query_devices())
sample_rate = sd.query_devices(7, 'input')['default_samplerate'] # Vosk requires 16kHz audio
#sample_rate = 44100.0
q = queue.Queue()

print("\33[34mLoading speech recognition model please wait...")
model = Model("/home/martenzo7/Downloads/model")
recognizer = KaldiRecognizer(model, sample_rate)
#print(sd.query_devices())
device_index = 5
def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))
def listen_and_transcribe():
    with sd.RawInputStream(samplerate=sample_rate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback, device=device_index):
        print("\33[34mListening... Press Ctrl+C to stop.")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get('text', '')
                if text.strip():
                    print(f"\33[31m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: \33[37m{text}")
try:
    listen_and_transcribe()
except KeyboardInterrupt:
    print("\nTranscription stopped.")
except sd.PortAudioError:
    print("Invalid number of channels, try using diffrent microphone.")
