from os import system
import speech_recognition as sr
from gpt4all import GPT4All
import sys
import whisper
import warnings
import time
import pyautogui
import webbrowser
import os

model = GPT4All("C:/Users/cptli/Documents/dev/Python", allow_download=False)
assistant_name = "max"
listening_for_trigger_word = True
should_run = True
source = sr.Microphone()
recognizer = sr.Recognizer()
base_model_path = os.path.expanduser('~/.cache/whisper/base.pt')
base_model = whisper.load_model(base_model_path)

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init() 

tasks = []
listeningToTask = False
askingAQuestion = False

def respond(text):
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$:+-/ ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    else:
        engine.say(text)
        engine.runAndWait()

def listen_for_command():
    with source as s:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)