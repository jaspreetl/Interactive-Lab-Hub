import speech_recognition as sr
import pyttsx3
import requests

engine = pyttsx3.init()
engine.setProperty('rate', 150)

voices = engine.getProperty('voices')
voice_found = False
for v in voices:
    if 'en' in v.id: 
        engine.setProperty('voice', v.id)
        voice_found = True
        break

if not voice_found:
    print("No English voice found, using default.")

r = sr.Recognizer()
mic = sr.Microphone(device_index=2) 

def ask_ai(question):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "phi3:mini", "prompt": question, "stream": False}
    )
    return response.json().get('response', 'No response')

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

while True:
    with mic as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        print(f"You said: {query}")
        if query.lower() in ["quit", "exit"]:
            print("Exiting...")
            speak("Goodbye!")
            break
        answer = ask_ai(query)
        speak(answer)
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
