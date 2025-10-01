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

def parse_reminder(text):
    """
    Parse reminders like:
      - "Remind me to call mom at 7pm"
      - "Remind me to call mom at seven pm"
      - "Remind me to finish homework by end of day"
      - "Remind me in 30 minutes to check the oven"
      - "Remind me tomorrow at 9am ..."

    Returns a dict: {"task": <short task text>, "time": <ISO datetime string or None>, "status": "to do"}
    """
    now = datetime.datetime.now()
    reminder = {"task": text, "time": None, "status": "to do"}

    text_orig = text.strip()
    text_low = re.sub(r'\s+', ' ', text_orig.lower()).strip()

    # 1) Prefer dateparser if available (handles "seven pm", "tomorrow at 7", "in 30 minutes", etc.)
    try:
        import dateparser
        dt = dateparser.parse(
            text_low,
            settings={'RELATIVE_BASE': now, 'PREFER_DATES_FROM': 'future'}
        )
        if dt:
            # build a cleaned task: remove common time-phrases after parsing
            task = re.sub(r'\b(remind( me)?( to)?)\b', '', text_orig, flags=re.I).strip()
            task = re.sub(r'\b(at|by|in|on|tomorrow|today|this|tonight|midnight|noon|end of day)\b.*',
                          '', task, flags=re.I).strip()
            reminder['task'] = task if task else text_orig
            reminder['time'] = dt.isoformat(sep=' ')
            return reminder
    except Exception:
        # dateparser not installed — we'll use fallback parsing below
        pass

    # 2) Explicit "end of day"
    if 'end of day' in text_low:
        today = datetime.date.today()
        reminder['time'] = str(datetime.datetime.combine(today, datetime.time(23, 59)))
        task = re.sub(r'\b(remind( me)?( to)?)\b', '', text_orig, flags=re.I)
        task = re.sub(r'end of day', '', task, flags=re.I)
        reminder['task'] = task.strip() if task.strip() else text_orig
        return reminder

    # 3) Normalize common tokens to numeric-ish forms so regex can catch them:
    #    - "noon" -> "12 pm"
    #    - "midnight" -> "12 am"
    text_low = text_low.replace('noon', '12 pm').replace('midnight', '12 am')

    # maps for converting spelled hours/minutes to digits
    hour_map = {
        'one':'1','two':'2','three':'3','four':'4','five':'5','six':'6',
        'seven':'7','eight':'8','nine':'9','ten':'10','eleven':'11','twelve':'12'
    }
    minute_map = {
        'half':'30','thirty':'30','quarter':'15','fifteen':'15',
        'forty-five':'45','forty five':'45','fortyfive':'45',
        'ten':'10','twenty':'20','five':'05'
    }

    # Replace patterns like "seven thirty", "seven thirty pm", "seven half pm" -> "7:30 pm"
    pattern_h_m = r'\b(' + '|'.join(hour_map.keys()) + r')\s+(thirty|half|quarter|fifteen|forty[- ]five|ten|twenty|five|\d{1,2})\b'
    def repl_h_m(m):
        hour_word = m.group(1)
        minute_word = m.group(2)
        hour = hour_map[hour_word]
        if minute_word in minute_map:
            minute = minute_map[minute_word]
        else:
            # numeric minutes like "7 30"
            minute = minute_word.zfill(2)
        return f"{hour}:{minute}"
    text_low = re.sub(pattern_h_m, repl_h_m, text_low)

    # Replace single hour words: "seven pm" -> "7 pm"
    pattern_hour = r'\b(' + '|'.join(hour_map.keys()) + r')\b'
    text_low = re.sub(pattern_hour, lambda m: hour_map[m.group(1)], text_low)

    # 4) Look for numeric time patterns now: "at 7:30 pm", "7 pm", "by 19:00", etc.
    time_regex = re.search(r'(?:(?:at|by)\s*)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text_low)
    if time_regex:
        hour = int(time_regex.group(1))
        minute = int(time_regex.group(2)) if time_regex.group(2) else 0
        ampm = time_regex.group(3)
        if ampm:
            if ampm.lower() == 'pm' and hour != 12:
                hour += 12
            elif ampm.lower() == 'am' and hour == 12:
                hour = 0

        date = datetime.date.today()
        if 'tomorrow' in text_low:
            date += datetime.timedelta(days=1)

        dt = datetime.datetime.combine(date, datetime.time(hour, minute))
        # Prefer future times: if parsed time already passed today, bump to next day
        if dt <= now:
            dt += datetime.timedelta(days=1)

        reminder['time'] = dt.isoformat(sep=' ')

        # try to remove the matched time substring from the original text to make 'task' readable
        matched = time_regex.group(0)  # matched part in the normalized lower case
        task = re.sub(re.escape(matched), '', text_orig, flags=re.I)
        task = re.sub(r'\b(remind( me)?( to)?)\b', '', task, flags=re.I)
        task = re.sub(r'\b(by|at|in|on|tomorrow|today|this|tonight)\b.*', '', task, flags=re.I).strip()
        reminder['task'] = task if task else text_orig
        return reminder

    # 5) "in X minutes/hours" -> relative time
    in_match = re.search(r'in\s+(\d+)\s+(minute|minutes|hour|hours)', text_low)
    if in_match:
        val = int(in_match.group(1))
        unit = in_match.group(2)
        delta = datetime.timedelta(hours=val) if 'hour' in unit else datetime.timedelta(minutes=val)
        dt = now + delta
        reminder['time'] = dt.isoformat(sep=' ')
        task = re.sub(in_match.group(0), '', text_orig, flags=re.I)
        task = re.sub(r'\b(remind( me)?( to)?)\b', '', task, flags=re.I)
        reminder['task'] = task.strip() if task.strip() else text_orig
        return reminder

    # 6) Fallback: no time found — return cleaned task only
    reminder['task'] = re.sub(r'\b(remind( me)?( to)?)\b', '', text_orig, flags=re.I).strip()
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

        if "remind me" in command_lower:
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
