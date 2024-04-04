import time
import gradio as gr
import subprocess
import psutil
from datetime import datetime
import requests
import torch
import json
from LLM import LLM
from whisper2 import WhisperTTS
from ChromadbTest import Vectordb_query

# class to initiate character prompt, TTS voice
class Character():
    #def __init__(self, voice, prompttemplate_add, name, conversation_pairs):
    def __init__(self, prompttemplate_add):
        #self.voice = voice
        self.prompttemplate_add = prompttemplate_add
        #self.name = name
        #self.conversation_pairs = conversation_pairs

def get_vectordb_query(history):
    print(Vectordb_query(history[-1][1]))

def get_time(input):
    local_time = datetime.now()
    formatted_local_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
    return f"Local Time: {formatted_local_time}"

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
          "what is the weather like": [get_weather, ''],
          "what time is it": [get_time, ''],
          "what is your name": "Hello I'm C3PO, human cyborg relations. I am fluent in over six million forms of communication. How can I assist you today?"
        }

def on_select(selected_option):
    version = LoadJSON("character_data.json")[selected_option]
    global character
    #character = Character(version['voice'], version['prompttemplate_add'], version['name'], version['conversation_pairs'])
    character = Character(version['prompttemplate_add'])

def LoadJSON(file_name):
    with open(file_name, "r") as json_file:
        return json.load(json_file)
    
def ChangecharacterJSON(new_character, new_prompttemplate):
    with open("character_data.json", "r") as json_file:
        data = json.load(json_file)
    data[new_character] = {"prompttemplate_add" : new_prompttemplate}
    with open("character_data.json", "w") as json_file:
        json.dump(data, json_file)

def get_keylist(json_file):
    l = []
    for key in json_file:
        l.append(key)
    return l

def bot(history):
    tokens = ""
    for option in get_keylist(pairs):
        if option == history[-1][0].lower():
            try:
                tokens = str(pairs[option][0](pairs[option][1]))
            except:
                tokens = str(pairs[option])
    if tokens == "":
        output_generator = LLM(history, character.prompttemplate_add)
        for output in output_generator:
            history[-1][1] = output
            yield history
    history[-1][1] = ""
    for token in tokens:
        history[-1][1] += token
        time.sleep(0.02)
        yield history

def call_TTS_env(history):
    script_path = "C:/Users/jvsan/Documents/C-3PO project/TTSpart.py"
    other_env_python = "C:/Users/jvsan/miniconda3/envs/tortoise/python.exe"
    textin = history[-1][1]
    TTSstart = time.perf_counter()
    print(TTSstart)
    result = subprocess.run([other_env_python, script_path, "--textin", textin], capture_output=True, text=True)
    TTSend = time.perf_counter()
    print(TTSend - TTSstart)
    return "generated.wav"
    
def user(user_message, history):
    return "", history + [[user_message, None]]

def regenerate(history):
    history[-1][1] = ""
    output_generator = LLM(history, character.prompttemplate_add)
    for output in output_generator:
        history[-1][1] = output
        yield history

def unloadGPU():
    torch.cuda.empty_cache()

def save_conversation(history):
    with open("conversation_data.json", "r") as json_file:
        data = json.load(json_file)
    data[datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = {"Conversation" : history}
    with open("conversation_data.json", "w") as json_file:
        json.dump(data, json_file)
    

with gr.Blocks(theme = gr.themes.Monochrome()) as demo:
    with gr.Tab("Chatbot"):
        character_select = gr.Dropdown(get_keylist(LoadJSON("character_data.json")), label="Choose Character")
        chatbot = gr.Chatbot(show_copy_button=True)
        with gr.Tab("Text"):
            msg = gr.Textbox(placeholder="Make sure to select a character")
        
        with gr.Tab("Voice"):
            with gr.Row():
                record_text = gr.Button("Record input")
                send = gr.Button("Send")
            STT_output = gr.Textbox(placeholder="STT output will apear here", label="Check output, if correct press send", interactive=False)
            
        with gr.Row():
            regenerate_output = gr.Button("Regenerate")
            clear = gr.Button("Clear")
            unload_LLM = gr.Button("Unload GPU")
            generateTTS = gr.Button("Generate TTS output")
            query_vectorDB = gr.Button("Query VectorDB")

        with gr.Accordion(open=False, label = "Conversation"):
            with gr.Row():
                save_conversation_button = gr.Button("Save conversation")
                load_conversaton_menu = gr.Dropdown(get_keylist(LoadJSON("conversation_data.json")), label = "Saved Conversations")
            
        TTS_out = gr.Audio()
        
        query_vectorDB.click(get_vectordb_query, chatbot)
        save_conversation_button.click(save_conversation, inputs=chatbot)
        regenerate_output.click(regenerate, chatbot, chatbot)
        character_select.input(on_select, character_select)
        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
        clear.click(lambda: None, None, chatbot, queue=False)
        record_text.click(fn=WhisperTTS, outputs=STT_output)
        unload_LLM.click(unloadGPU)
        send.click(user, [STT_output, chatbot], [STT_output, chatbot], queue=False).then(bot, chatbot, chatbot)
        generateTTS.click(call_TTS_env, chatbot, TTS_out)

    with gr.Tab("Character Creator"):

        new_character = gr.Textbox(label="1. New Character Name")
        new_prompt_template = gr.Textbox(label="2. New Prompt Template")
        submit_new_character = gr.Button("Submit Character")

        with gr.Accordion("Show JSON"):
            json_output = gr.JSON(LoadJSON("character_data.json"))

        submit_new_character.click(ChangecharacterJSON, inputs=[new_character, new_prompt_template])

demo.queue()
demo.launch()