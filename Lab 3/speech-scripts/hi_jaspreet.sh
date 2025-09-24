#!/bin/bash
# A simple TTS greeting using espeak

# Replace this with your actual name
MY_NAME="Jaspreet"

# The message we want to say
MESSAGE="Hi $MY_NAME!"

# Send the message to espeak
echo "$MESSAGE" | espeak