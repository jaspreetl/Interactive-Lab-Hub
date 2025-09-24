# vosk-transcriber: command not found
# File written by ChatGPT

from vosk import Model, KaldiRecognizer
import sys
import json
import wave

wf = wave.open("recorded_mono.wav", "rb")
model = Model(lang="en")  # downloads or loads the English model
rec = KaldiRecognizer(model, wf.getframerate())

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())

print(rec.FinalResult())
