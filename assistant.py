from os import system
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from gpt4all import GPT4All
import sys
import whisper
import warnings
import time
import pyautogui
import webbrowser
import os

model = GPT4All(
    r"D:\Projects\AI\models\gpt4all-falcon-newbpe-q4_0.gguf",
    allow_download=False
)
assistant_name = "max"
listening_for_trigger_word = True
should_run = True
print("Loading Whisper model...")

# base_model_path = os.path.expanduser('~/.cache/whisper/base.pt')
base_model = whisper.load_model("tiny")


if sys.platform != "darwin":
    import pyttsx3
    engine = pyttsx3.init() 


def respond(text):
    print(f"Assistant: {text}")
    if sys.platform == "darwin":
        clean_text = ''.join(c for c in text if c.isalnum() or c in " .,?!")
        system(f"say '{clean_text}'")
    else:
        engine.say(text)
        engine.runAndWait()

tasks = []
listening_to_task = False
asking_question = False



def listen_for_command(duration=5, fs=16000):
    print("Listening...")

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype=np.int16
    )
    sd.wait()

    write("command.wav", fs, recording)

    result = base_model.transcribe("command.wav")
    command = result["text"].strip().lower()

    print("Heard:", command)
    return command





def perform_command(command):
    global listening_to_task, asking_question, should_run

    if len(command) < 3:
        return

    if not command:
        return

    if listening_to_task:
        tasks.append(command)
        listening_to_task = False
        respond(f"Task added. You now have {len(tasks)} tasks.")
        return

    if asking_question:
        asking_question = False
        respond("Thinking...")
        output = model.generate(command, max_tokens=200)
        respond(output)
        return
    

    if "add" in command and "task" in command:
        listening_to_task = True
        respond("Sure, what is the task?")
    elif "list tasks" in command:
        if not tasks:
            respond("Your task list is empty.")
        else:
            respond("Your tasks are:")
            for task in tasks:
                respond(task)
                
    elif "take a screenshot" in command:
        pyautogui.screenshot("screenshot.png")
        respond("Screenshot taken.")
    elif "open chrome" in command:
        respond("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "ask a question" in command:
        asking_question = True
        respond("What is your question?")
    elif "exit" in command or "quit" in command:
        respond("Goodbye.")
        should_run = False
    else:
        respond("Sorry, I did not understand that.")

def main():
    respond(f"{assistant_name} is ready. Say '{assistant_name}' to wake me up.")

    while should_run:
        command = listen_for_command()

        if not command or len(command.strip()) < 3:
            continue

        if assistant_name in command:
            print("Wake word detected")

            command = command.replace(assistant_name, "").strip()

            if not command:
                respond("Yes?")
                continue

            perform_command(command)
        else:
            print("Wake word not detected")
        time.sleep(0.5)









if __name__ == "__main__":
    main()