from urllib import response
import nltk
from nltk.chat.util import Chat, reflections
import tkinter as tk
import psutil
import subprocess
from playsound import playsound as ps
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyaudio

model = Model(r"E:\vosk-model-en-us-0.22\vosk-model-en-us-0.22")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

def change_mode():
    global Voice_mode
    Voice_mode = not Voice_mode
    print(Voice_mode)

def trigger_listen():
    if Voice_mode == True:
        return True
    else:
        return False

Voice_mode = False
while trigger_listen() == True:
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        print(text[14:-3])


# Define the chat pairs for the bot
pairs = [
    [
        r"my name is (.*)",
        ["It is a pleasure to meet you, %1. My name is 3PO, Human-Cyborg Relations.",]
    ],
    [
        r"hi|hello|hey",
        ["Oh my! Hello there, how may I assist you?", "Greetings, sir/madam. How may I be of service?", "Hello, I am C-3PO, human-cyborg relations. How may I assist you today?",]
    ],
    [
        r"what's your name?",
        ["I'm 3PO, human cyborg relations. I am fluent in over six million forms of communication. How can I assist you today?",]
    ],
    [
        r"how are you?",
        ["I am functioning perfectly, thank you for asking. How may I assist you today?"]
    ],
    [
        r"what can you do?",
        ["I am fluent in over six million forms of communication and am proficient in a variety of protocols and etiquette. How may I assist you today?", "I am a protocol droid, sir/madam, skilled in various forms of diplomacy and communication. How may I be of service?",]
    ],
    [
        r"(.*) help (.*)",
        ["Sure, I'd be happy to help. What do you need assistance with?",]
    ],
    [
        r"thank you",
        ["You are most welcome, sir/madam.", "You are quite welcome, sir/madam.", "It was my pleasure to assist you, sir/madam.",]
    ],

    [
        r"quit",
        ["Thank you for chatting with me today. Goodbye!",]
    ],
    [
        r"may the force be with you",
        ["And with you as well, sir/madam.", "May the force be with us all, sir/madam.", "A most appropriate sentiment, sir/madam. May the force be with you.",]
    ],
    [
        r"joke",
        ["Why did Yoda stop using his credit card? Because he always gets charged with MasterCard!", "Why did the stormtrooper buy an iphone? He couldn't find the anDroid he was looking for."]
    ],
    [
        r"iracing",
        ["I'll launch the software needed",]
    ]
]

#launching executable after checking if it is already running, program is exe file name, path is raw string of path
def launch(program=str, path=str):
    found = False
    while True:
        for proc in psutil.process_iter():
            if proc.name() == program:
                print("program is already running")
                found = True
                break
        break
    if found == False:
        subprocess.Popen([path])
        print("Started program")

# Define the chatbot function
def chatbot():
    chatbot = Chat(pairs, reflections)
    response = chatbot.respond(entry.get())
    conversation.insert(tk.END, "You: " + entry.get() + "\n")
    conversation.insert(tk.END, "3PO: " + response + "\n")
    entry.delete(0, tk.END)
    if response == "I'll launch the software needed":
        launch("iRacingUI.exe",r'C:\Program Files (x86)\iRacing\ui\iRacingUI.exe')
        launch("simracingstudio.exe",r'C:\Program Files\SimRacingStudio 2.0\simracingstudio.exe')
        launch("CrewChiefV4.exe",r'C:\Program Files (x86)\Britton IT Ltd\CrewChiefV4\CrewChiefV4.exe')
        file = "I'll ask R2 to launch the software.wav"
        ps(file)

# Create the UI
root = tk.Tk()
root.title("3PO")

# Create the conversation window
conversation = tk.Text(root, height=10, width=50)
conversation.pack()


entry = tk.Entry(root, width=40)
entry.pack()

# Create the submit button
submit = tk.Button(root, text="Send", command=chatbot)
submit.pack()

Mic = tk.Button(root, text="Voice mode", command = change_mode)
Mic.pack()

root.grid_columnconfigure(1, weight=1)

# Start the UI loop
root.mainloop()
