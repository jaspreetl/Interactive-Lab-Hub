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
    global reminders
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)

def speak(message):
    os.system(f'espeak "{message}" 2>/dev/null')
NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12
}

def normalize_time_words(text):
    for word, num in NUMBER_WORDS.items():
        text = re.sub(rf"\b{word}\b", str(num), text, flags=re.I)
    return text
def parse_reminder(text):
    """
    Parse 'remind me to X at TIME' or 'by end of day'.
    Adds a default status 'to do'.
    """
    original_text = text.lower()
    text = normalize_time_words(original_text)  # convert 'seven' → '7'

    reminder = {
        "task": None,
        "time": None,
        "status": "to do"
    }

    # Default task text = everything after "remind me to"
    task_text = re.sub(r"^.*remind me to\s*", "", original_text, flags=re.I).strip()

    # Remove "at TIME" or "by end of day" from task_text
    task_text = re.sub(r"\bat\s+\d{1,2}(:\d{2})?\s?(am|pm)?", "", task_text, flags=re.I)
    task_text = re.sub(r"\bby end of day\b", "", task_text, flags=re.I)
    task_text = task_text.strip()

    reminder["task"] = task_text if task_text else original_text

    # Handle "end of day"
    if "end of day" in original_text:
        today = datetime.date.today()
        reminder["time"] = str(datetime.datetime.combine(today, datetime.time(23, 59)))
        return reminder

    # Handle times
    time_match = re.search(r"(\d{1,2})(?:\:(\d{2}))?\s?(am|pm)", text, re.I)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2)) if time_match.group(2) else 0
        ampm = time_match.group(3).lower()
        if ampm == "pm" and hour != 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0
        today = datetime.date.today()
        reminder["time"] = str(datetime.datetime.combine(today, datetime.time(hour, minute)))

    return reminder



def mark_complete(command):
    """
    Matches after 'complete' and updates the first matching reminder.
    """
    global reminders
    task_match = command.replace("complete", "").strip().lower()

    for reminder in reminders:
        if task_match in reminder["task"].lower():
            reminder["status"] = "complete"
            save_reminders()
            speak(f"I marked '{reminder['task']}' as complete.")
            return True

    speak("I couldn't find that task to complete.")
    return False

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
        speak("I am listening. What would you like me to do?")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")

def main():
    load_reminders()
    command = listen_and_transcribe()
    if command:
        command_lower = command.lower()

        if "remind" in command_lower:
            reminder = parse_reminder(command)
            reminders.append(reminder)
            save_reminders()
            speak(f"Okay, I added your reminder: {reminder['task']}")
        
        elif "complete" in command_lower:
            mark_complete(command)
        
        else:
            speak("Sorry, I only handle reminders right now.")

if __name__ == "__main__":
    main()
