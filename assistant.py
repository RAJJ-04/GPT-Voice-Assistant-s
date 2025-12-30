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

model = GPT4All("D:\Projects\AI\models\gpt4all-falcon-newbpe-q4_0.gguf", allow_download=False)
assistant_name = "max"
listening_for_trigger_word = True
should_run = True
source = sr.Microphone()
recognizer = sr.Recognizer()
print("Loading Whisper model...")

# base_model_path = os.path.expanduser('~/.cache/whisper/base.pt')
base_model = whisper.load_model(base_model_path)

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



def listen_for_command():
    with source as s:
        recognizer.adjust_for_ambient_noise(s, duration=0.5)
        print("Listening...")
        audio = recognizer.listen(s)
                                                                                 # LISTEN FUNCTION 
    with open("command.wav", "wb") as f:
        f.write(audio.get_wav_data())

    result = base_model.transcribe("command.wav")
    command = result["text"].strip().lower()

    print("Heard:", command)
    return command




def perform_command(command):
    global listening_to_task, asking_question, should_run

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
    
    
    if command:
        print("Command: ", command)
        if listeningToTask:
            tasks.append(command)
            listeningToTask = False
            respond("Adding " + command + " to your task list. You have " + str(len(tasks)) + " currently in your list.")
        elif "add a task" in command:
            listeningToTask = True
            respond("Sure, what is the task?")
        elif "list tasks" in command:
            respond("Sure. Your tasks are:")
            for task in tasks:
                respond(task)
        elif "take a screenshot" in command:
            pyautogui.screenshot("screenshot.png")
            respond("I took a screenshot for you.")
        elif "open chrome" in command:
            respond("Opening Chrome.")
            webbrowser.open("http://www.youtube.com")
        elif "ask a question" in command:
            askingAQuestion = True
            respond("What's your question?")
            return
        elif askingAQuestion:
            askingAQuestion = False
            respond("Thinking...")
            print("User command: ", command)
            output = model.generate(command, max_tokens=200)
            print("Output: ", output)
            respond(output)
        elif "exit" in command:
            should_run = False
        else:
            respond("Sorry, I'm not sure how to handle that command.")
    listening_for_trigger_word = True

def main():
    global listening_for_trigger_word
    while should_run:
        command = listen_for_command()
        if listening_for_trigger_word:
            listening_for_trigger_word = False
        else:
            perform_command(command)
        time.sleep(1)
    respond("Goodbye.")

if __name__ == "__main__":
    main()