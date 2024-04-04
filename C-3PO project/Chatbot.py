from urllib import response
from LLM import LLM
from voice import STT
from nltk.chat.util import Chat, reflections
import tkinter as tk
import time
import subprocess
from functools import lru_cache
import threading
import psutil
import requests
from datetime import datetime

def get_time():
    local_time = datetime.now()
    formatted_local_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
    return("Local Time:", formatted_local_time)

def get_weather(input):
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    API_KEY = '65d96c2b20138cb80583dcfbe3232309'

    # Replace 'YOUR_CITY' and 'YOUR_COUNTRY_CODE' with your city and country code
    CITY = 'Dordrecht'
    COUNTRY_CODE = 'nl'

    # Construct the API URL
    API_URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY_CODE}&appid={API_KEY}'

    # Make the API request
    response = requests.get(API_URL)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp'] - 273.15  # Convert temperature from Kelvin to Celsius
        description = data['weather'][0]['description']
        return str(f"Weather in {CITY}, {COUNTRY_CODE}, Temperature: {temperature:.2f}°C, Description: {description}")
    else:
        return("Failed to retrieve weather data. Check your API key and location.")


def call_app(app = str):
    found = False
    name = {'steam': ['steam.exe', r'C:\Program Files (x86)\Steam\steam.exe'],
            'iracing': ['iRacingUI.exe', r'C:\Program Files (x86)\iRacing\ui\iRacingUI.exe'],
            'simracing studio': ['simracingstudio.exe', r'C:\Program Files\SimRacingStudio 2.0\simracingstudio.exe'],
            'crew chief': ['CrewChiefV4.exe',r'C:\Program Files (x86)\Britton IT Ltd\CrewChiefV4\CrewChiefV4.exe']
            }
    while True:
        for proc in psutil.process_iter():
            if proc.name() == name[app][0]:
                print("app is already running")
                found = True
                break
        break
    if found == False:
        subprocess.Popen([name[app][1]])
        print("Started app")
    print("code finished correctly")
    return 'succes'

pairs = { "open simracing studio" : [call_app, 'simracing studio'],
          "open crew chief" : [call_app, 'crew chief'],
          "open iracing" : [call_app, 'iracing'],
          "open steam" : [call_app, 'steam'],
          "what is the weather": [get_weather, ''],
          "what is your name": "Hello I'm C3PO, human cyborg relations. I am fluent in over six million forms of communication. How can I assist you today?"
        }

class Voicemode:
    state = False

def getList(dict):
    keys = []
    for key in dict.keys():
        keys.append(key)
    return(keys)

# Function to handle sending when Enter key is pressed
def send_on_enter(event):
    chatbot()  # Call the chatbot function

@lru_cache
def call_TTS_env(textin, *args):
    script_path = "C:/Users/jvsan/Documents/C-3PO project/TTSpart.py"
    other_env_python = "C:/Users/jvsan/miniconda3/envs/tortoise/python.exe"
    TTSstart = time.perf_counter()
    print(TTSstart)
    result = subprocess.run([other_env_python, script_path, "--textin", textin, *args], capture_output=True, text=True)
    TTSend = time.perf_counter()
    print(TTSend - TTSstart)
    return result.stdout

def SwitchVoiceMode():
    if Voicemode.state == False:
        Voicemode.state = True
    elif Voicemode.state == True:
        Voicemode.state = False
    print(Voicemode.state)

# Define the chatbot function
def chatbot():
    global last_response
    response = ''
    if Voicemode.state == False:
        for i in getList(pairs):
            if i == entry.get().lower():
                try:
                    response = pairs[i][0](pairs[i][1])
                    print(response)
                except:
                    response = pairs[i]
                    print(response)
        if response == '':
            response = LLM(entry.get())
        last_response = response
        conversation.insert(tk.END, "You: " + entry.get() + "\n")
        conversation.insert(tk.END, "C3PO: " + response + "\n")
        entry.delete(0, tk.END)
    elif Voicemode.state == True:
        STTinput = STT()
        for i in getList(pairs):
            if i == STTinput.lower():
                try:
                    response = pairs[i][0](pairs[i][1])
                except:
                    response = pairs[i]
        if response == '':
            response = LLM(STTinput)
        last_response = response
        conversation.insert(tk.END, "You: " + entry.get() + "\n")
        conversation.insert(tk.END, "C3PO: " + response + "\n")
        entry.delete(0, tk.END)

def AudioGen():
    call_TTS_env(last_response)
    print('Audio generated')

def launchUI():
    # Create the UI
    root = tk.Tk()
    root.title("C3PO")

    # Create the conversation window
    global conversation
    conversation = tk.Text(root, wrap="word")
    conversation.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

    # Create the input field
    global entry
    entry = tk.Entry(root, width=50)
    entry.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # Create voice mode button
    Voice = tk.Button(root, text="Voice", command=SwitchVoiceMode)
    Voice.grid(row=1, column=4, padx=2, pady=10, sticky="e")

    # Create Generate Audio mode button
    AudioGenButton = tk.Button(root, text="Generate Speech", command=threading.Thread(target=AudioGen).start)
    AudioGenButton.grid(row=1, column=5, padx=2, pady=10, sticky="e")

    # Create the submit button
    submit = tk.Button(root, text="Send", command=chatbot)
    submit.grid(row=1, column=3, padx=2, pady=10, sticky="e")
    
    # Bind Enter key to chatbot function
    entry.bind("<Return>", lambda event=None: chatbot())

    # Start the UI loop
    root.mainloop()