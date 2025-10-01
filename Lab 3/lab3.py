import os
import json
import queue
import sounddevice as sd
import vosk
import datetime
import re

# Simple reminder store (in-memory + file backup)
REMINDERS_FILE = "reminders.json"
reminders = []

def load_reminders():
    global reminders
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as f:
            reminders = json.load(f)

def save_reminders():
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)

def speak(message):
    os.system(f'espeak "{message}" 2>/dev/null')

def parse_reminder(text):
    """
    Very simple parsing for 'remind me to X at TIME' or 'by end of day'.
    """
    reminder = {"task": text, "time": None}
    time_match = re.search(r"(\d{1,2})(?:\:(\d{2}))?\s?(am|pm)?", text, re.I)
    if "end of day" in text.lower():
        today = datetime.date.today()
        reminder["time"] = str(datetime.datetime.combine(today, datetime.time(23, 59)))
    elif time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2)) if time_match.group(2) else 0
        ampm = time_match.group(3)
        if ampm:
            if ampm.lower() == "pm" and hour != 12:
                hour += 12
            elif ampm.lower() == "am" and hour == 12:
                hour = 0
        today = datetime.date.today()
        reminder["time"] = str(datetime.datetime.combine(today, datetime.time(hour, minute)))
    return reminder

def listen_and_transcribe():
    model = vosk.Model(lang="en-us")
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        speak("I am listening. What reminder would you like to add?")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")
            # else: keep listening

def main():
    load_reminders()
    command = listen_and_transcribe()
    if command:
        if "remind me" in command.lower():
            reminder = parse_reminder(command)
            reminders.append(reminder)
            save_reminders()
            speak(f"Okay, I added your reminder: {reminder['task']}")
        else:
            speak("Sorry, I only handle reminders right now.")

if __name__ == "__main__":
    main()
