import speech_recognition as sr
import subprocess
import requests

# Core setup
r = sr.Recognizer()
mic = sr.Microphone(device_index=2)  # USB mic

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "phi3:mini"

def speak(text):
    """Text-to-speech"""
    subprocess.run(['espeak', text])

def ask_ai(question):
    """Query Ollama"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": MODEL_NAME, "prompt": question, "stream": False},
            timeout=20
        )
        return response.json().get('response', 'No response')
    except:
        return "Error contacting Ollama."

speak("Hi! Say something or 'exit' to quit.")
while True:
    with mic as source:
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio).lower()
        if query in ["exit", "quit"]:
            speak("Goodbye!")
            break
        speak("Thinking...")
        answer = ask_ai(query)
        speak(answer)
    except:
        speak("I didn't catch that.")
