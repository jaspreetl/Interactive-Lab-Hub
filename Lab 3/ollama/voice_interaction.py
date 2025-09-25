
import speech_recognition as sr
import subprocess
import requests

r = sr.Recognizer()
mic = sr.Microphone(device_index=2)  

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "phi3:mini"

def speak(text):
    """Convert text to speech using espeak"""
    print(f"Assistant: {text}")
    subprocess.run(['espeak', text])

def ask_ai(question):
    """Send a query to Ollama API"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": MODEL_NAME, "prompt": question, "stream": False},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get('response', 'No response')
        else:
            return f"Error: Ollama API returned status {response.status_code}"
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

def main():
    speak("Hello! I'm your Ollama voice assistant. Say 'exit' to quit.")
    
    while True:
        with mic as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        
        try:
            query = r.recognize_google(audio)
            print(f"You said: {query}")
            
            if query.lower() in ["quit", "exit", "bye", "goodbye"]:
                speak("Goodbye! Have a great day!")
                break
            
            # Send query to Ollama
            speak("Thinking...")
            answer = ask_ai(query)
            speak(answer)
        
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()