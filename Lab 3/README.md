# Chatterboxes
**Jaspreet Lal (jl4536), Arya Prasad (ap2535)**

<details>
  [![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)
In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

Please check instructions in [prep.md](prep.md) and complete the setup before class on Wednesday, Sept 23rd.

### Pick up Web Camera If You Don't Have One

Students who have not already received a web camera will receive their [Logitech C270 Webcam](https://www.amazon.com/Logitech-Desktop-Widescreen-Calling-Recording/dp/B004FHO5Y6/ref=sr_1_3?crid=W5QN79TK8JM7&dib=eyJ2IjoiMSJ9.FB-davgIQ_ciWNvY6RK4yckjgOCrvOWOGAG4IFaH0fczv-OIDHpR7rVTU8xj1iIbn_Aiowl9xMdeQxceQ6AT0Z8Rr5ZP1RocU6X8QSbkeJ4Zs5TYqa4a3C_cnfhZ7_ViooQU20IWibZqkBroF2Hja2xZXoTqZFI8e5YnF_2C0Bn7vtBGpapOYIGCeQoXqnV81r2HypQNUzFQbGPh7VqjqDbzmUoloFA2-QPLa5lOctA.L5ztl0wO7LqzxrIqDku9f96L9QrzYCMftU_YeTEJpGA&dib_tag=se&keywords=webcam%2Bc270&qid=1758416854&sprefix=webcam%2Bc270%2Caps%2C125&sr=8-3&th=1) and bluetooth speaker on Wednesday at the beginning of lab. If you cannot make it to class this week, please contact the TAs to ensure you get these. 

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. There are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2025
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2022Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.
</details>

## Part 1.
<details>
### Setup 

Activate your virtual environment

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ cd Lab\ 3
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python3 -m venv .venv
pi@ixe00:~/Interactive-Lab-Hub $ source .venv/bin/activate
(.venv)pi@ixe00:~/Interactive-Lab-Hub $ 
```

Run the setup script
```(.venv)pi@ixe00:~/Interactive-Lab-Hub $ pip install -r requirements.txt  ```

Next, run the setup script to install additional text-to-speech dependencies:
```
(.venv)pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ ./setup.sh
```
</details>

### Text to Speech 
<details>
In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using the microphone and speaker on your webcamera. In the directory is a folder called `speech-scripts` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/speech-scripts $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files `.sh` by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/speech-scripts $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech
```
You can test the commands by running
```
echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? 
Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.
</details>

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)
See Lab 3/speech-scripts/hi_jaspreet.sh. 
<img width="639" height="298" alt="Screenshot 2025-09-24 at 7 24 05 PM" src="https://github.com/user-attachments/assets/2a4a7e13-dd17-448e-afc6-50498613dddd" />


---
Bonus: For the bonus section, I was able to run both commands and play them on my speaker. I did have to manually download the Lessac model configure it in the terminal. I used ChatGPT to help with this setup. 

<details>
[Piper](https://github.com/rhasspy/piper) is another fast neural based text to speech package for raspberry pi which can be installed easily through python with:
```
pip install piper-tts
```
and used from the command line. Running the command below the first time will download the model, concurrent runs will be faster. 
```
echo 'Welcome to the world of speech synthesis!' | piper \
  --model en_US-lessac-medium \
  --output_file welcome.wav
```
Check the file that was created by running `aplay welcome.wav`. Many more languages are supported and audio can be streamed dirctly to an audio output, rather than into an file by:

```
echo 'This sentence is spoken first. This sentence is synthesized while the first sentence is spoken.' | \
  piper --model en_US-lessac-medium --output-raw | \
  aplay -r 22050 -f S16_LE -t raw -
```
</details>

### Speech to Text. 

<details>
Next setup speech to text. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 

Make sure you're running in your virtual environment with the dependencies already installed:
```
source .venv/bin/activate
```

Test if vosk works by transcribing text:

```
vosk-transcriber -i recorded_mono.wav -o test.txt
```

You can use vosk with the microphone by running 
```
python test_microphone.py -m en
```
</details>

<img width="294" height="485" alt="Screenshot 2025-09-24 at 7 36 12 PM" src="https://github.com/user-attachments/assets/2f7753a5-465a-4efe-b64c-62b5fb598bfc" />

---
Bonus:
<details>
[Whisper](https://openai.com/index/whisper/) is a neural network–based speech-to-text (STT) model developed and open-sourced by OpenAI. Compared to Vosk, Whisper generally achieves higher accuracy, particularly on noisy audio and diverse accents. It is available in multiple model sizes; for edge devices such as the Raspberry Pi 5 used in this class, the tiny.en model runs with reasonable latency even without a GPU.

By contrast, Vosk is more lightweight and optimized for running efficiently on low-power devices like the Raspberry Pi. The choice between Whisper and Vosk depends on your scenario: if you need higher accuracy and can afford slightly more compute, Whisper is preferable; if your priority is minimal resource usage, Vosk may be a better fit.

In this class, we provide two Whisper options: A quantized 8-bit faster-whisper model for speed, and the standard Whisper model. Try them out and compare the trade-offs.

Make sure you're in the Lab 3 directory with your virtual environment activated:
```
cd ~/Interactive-Lab-Hub/Lab\ 3/speech-scripts
source ../.venv/bin/activate
```

Then test the Whisper models:
```
python whisper_try.py
```
and

```
python faster_whisper_try.py
```
</details>
\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*
See Lab 3/get_nums.sh. <img width="683" height="486" alt="Screenshot 2025-09-24 at 7 43 50 PM" src="https://github.com/user-attachments/assets/ed9fbca7-11a0-4dd9-9b11-9d3d31b5576b" />


### 🤖 NEW: AI-Powered Conversations with Ollama
<details>
Want to add intelligent conversation capabilities to your voice projects? **Ollama** lets you run AI models locally on your Raspberry Pi for sophisticated dialogue without requiring internet connectivity!

#### Quick Start with Ollama

**Installation** (takes ~5 minutes):
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download recommended model for Pi 5
ollama pull phi3:mini

# Install system dependencies for audio (required for pyaudio)
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-dev

# Create separate virtual environment for Ollama (due to pyaudio conflicts)
cd ollama/
python3 -m venv ollama_venv
source ollama_venv/bin/activate

# Install Python dependencies in separate environment
pip install -r ollama_requirements.txt
```
#### Ready-to-Use Scripts

We've created three Ollama integration scripts for different use cases:

**1. Basic Demo** - Learn how Ollama works:
```bash
python3 ollama_demo.py
```

**2. Voice Assistant** - Full speech-to-text + AI + text-to-speech:
```bash
python3 ollama_voice_assistant.py
```

**3. Web Interface** - Beautiful web-based chat with voice options:
```bash
python3 ollama_web_app.py
# Then open: http://localhost:5000
```

#### Integration in Your Projects

Simple example to add AI to any project:
```python
import requests

def ask_ai(question):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "phi3:mini", "prompt": question, "stream": False}
    )
    return response.json().get('response', 'No response')

# Use it anywhere!
answer = ask_ai("How should I greet users?")
```

**📖 Complete Setup Guide**: See `OLLAMA_SETUP.md` for detailed instructions, troubleshooting, and advanced usage!
</details>


\*\***Try creating a simple voice interaction that combines speech recognition, Ollama processing, and text-to-speech output. Document what you built and how users responded to it.**\*\*
See Lab 3/ollama/voice_interaction.py. 

I built a voice assistant on a Raspberry Pi that uses Ollama to generate AI responses and espeak for text-to-speech output. Users found it engaging, but became frustrated when it failed to recognize their speech. The assistant took some time to response and conversations with it seemed abrupt. For this reason, I scaled back the funcationality of the script. The assistant was quicker to mention when it 'Didn't catch that', but I found it underperformed with voice recognition. 


### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) 

\*\***Post your storyboard and diagram here.**\*\*
Verplank Diagram: ![image](https://github.com/user-attachments/assets/a676e1f1-bd00-4e3e-a81b-ae6820f4d2f3)

Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 

\*\***Please describe and document your process.**\*\*

To create the interaction model for our speech-enabled device, Nudge, my partner and I began by brainstorming everyday situations where setting or checking reminders would feel natural. Using digital sticky notes as virtual idea cards, we captured and organized our thoughts into key categories:
- Setting basic reminders
- Checking existing reminders (including when none are scheduled)
- Scheduling for the same day (requiring only a time)
- Scheduling for a future day (requiring date and time)
- Handling errors or unclear inputs
- Managing overlapping reminders
- End-of-day summaries (reviewing completed tasks and wrapping up)
With these seven categories defined, we drafted storyboards for each, focusing on how a natural, conversational exchange might unfold between a user and the device.

Storyboards: 
![image](https://github.com/user-attachments/assets/ec72df74-1ffa-4157-81e9-a3cd771159b9)  

![image](https://github.com/user-attachments/assets/b7d871d5-e40f-48ab-9207-7c563c5eebd9)  

![image](https://github.com/user-attachments/assets/1c386a16-c252-42ac-9a0f-a62ad8dd8d2c)  

![image](https://github.com/user-attachments/assets/82f579c2-d168-4e0a-8715-d557b530a2bc)  

![image](https://github.com/user-attachments/assets/d882c4b1-b284-47d0-ad05-72246979f4a2)  

![image](https://github.com/user-attachments/assets/50e014e7-3bfe-4d6b-a8e5-627c7050db95)  

![image](https://github.com/user-attachments/assets/eecb0a98-b744-473f-8229-95beea110a34)  


### Acting out the dialogue
\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

https://drive.google.com/file/d/1u_3OkhGrxARDf5sqwKVKEyVudCLVKsal/view?usp=drivesdk

Acting out the dialogue did turn ouy as we imagined for the most part. We did find slight differences with what Nudge needed to add, delete and remind the user and at what times. During the acting, we added "Call Mom at 7pm" as a task, but forgot to remind the user despite adding it to the schedule. 

### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...
2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?
3. Make a new storyboard, diagram and/or script based on these reflections.

## Prototype your system

*Document how the system works*  
Nudge is a voice-activated reminder manager built using Python, Vosk (speech recognition), and eSpeak (text-to-speech). It allows you to add reminders, set them with times, and mark tasks complete using natural speech. Reminders are stored in a JSON file called remidners.json so they persist. 

*Include videos or screencaptures of both the system and the controller.*  
https://drive.google.com/file/d/13rie_ak0-cq1xNEr-kii4EEgyVFGneHg/view?usp=sharing

<details>
  <summary><strong>Submission Cleanup Reminder (Click to Expand)</strong></summary>
  
  **Before submitting your README.md:**
  - This readme.md file has a lot of extra text for guidance.
  - Remove all instructional text and example prompts from this file.
  - You may either delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
  - Your final submission should be neat, focused on your own work, and easy to read for grading.
  
  This helps ensure your README.md is clear professional and uniquely yours!
</details>

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?

The system was able to capture simple commands, parse out times (like “7 pm” or “end of day”), and store reminders with a status flag. On the other hand, the parsing was somewhat difficult. Variations in phrasing/pronounciation or background noise sometimes led to incorrect transcription. Matching tasks to mark them complete was too strict, so we had to phrase commands very closely to the stored task. 

### What worked well about the controller and what didn't?

Using voice as the controller made this a hands-free and somewhat natural system, especially for quick reminder setting. The speech feedback with eSpeak provided immediate confirmation. However, the system only supported a very small set of commance (“remind” and “complete”), with little error correction or flexibility. Continuous listening could also be unreliable due to background noise or misrecognition.

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

The WoZ setup showed how important real-time feedback and flexible interpretation are for users. Since people don’t always phrase commands the same way, the system needs to handle variation gracefully. The WoZ approach underscored that autonomy requires not only good speech recognition, but also context awareness (knowing what the user likely means given time, past tasks, or environment) to reduce friction and errors.

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

The system could log every spoken input, the parsed command, and the system’s response, creating a dataset of raw speech → transcription → parsed intent → outcome. This would be useful for training more robust natural language models. Other sensing modalities could include video/gesture input (for confirming or dismissing reminders) or context sensing (such as time of day or location) to better understand when and how users set reminders. 

