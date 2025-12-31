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

model = GPT4All(
    r"D:\Projects\AI\models\gpt4all-falcon-newbpe-q4_0.gguf",
    allow_download=False
)
assistant_name = "max"
listening_for_trigger_word = True
should_run = True
source = sr.Microphone()
recognizer = sr.Recognizer()
print("Loading Whisper model...")

# base_model_path = os.path.expanduser('~/.cache/whisper/base.pt')
base_model = whisper.load_model("base")


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
    

    if "add a task" in command:
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
    respond(f"{assistant_name} is ready.")
    while should_run:
        command = listen_for_command()
        perform_command(command)
        time.sleep(0.5)

if __name__ == "__main__":
    main()