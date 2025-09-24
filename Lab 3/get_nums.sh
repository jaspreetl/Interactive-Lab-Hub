#!/bin/bash
# Shell script to ask a user for a number via voice and record the spoken response

VOICE_MODEL="$HOME/.local/share/piper/en_US-lessac-medium.onnx"
PROMPT="What is your lucky number:"

echo "$PROMPT" | piper --model "$VOICE_MODEL" --output-file prompt.wav
aplay prompt.wav

speaker-test -t sine -f 1000 -l 1 -p 200 > /dev/null 2>&1 & sleep 0.5; kill $!
arecord -d 5 -r 16000 -c 1 -f S16_LE response.wav
vosk-transcriber -i response.wav -o result.txt

echo "Your lucky number was:"
cat result.txt
