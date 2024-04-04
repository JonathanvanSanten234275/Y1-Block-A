import tkinter as tk
from tkinter import ttk
import json

class Character():
    def __init__(self, voice, prompttemplate_add, name, conversation_pairs):
        self.voice = voice
        self.prompttemplate_add = prompttemplate_add
        self.name = name
        self.conversation_pairs = conversation_pairs

def LoadJSON(file_name):
    # Specify the filename of the JSON file you want to read
    file_name = "character_data.json"
    
    # Open the JSON file in read mode
    with open(file_name, "r") as json_file:
        # Load the JSON data from the file
        return json.load(json_file)
    

# Now, 'data' contains the content of the JSON files
data = LoadJSON('character_data')
l = []


for key in data:
    l.append(key)
print(l)

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
    Voice = tk.Button(root, text="Voice")
    Voice.grid(row=1, column=6, padx=2, pady=10, sticky="e")

    # Create Generate Audio mode button
    AudioGenButton = tk.Button(root, text="Generate Speech")
    AudioGenButton.grid(row=1, column=5, padx=2, pady=10, sticky="e")

    # Create the submit button
    submit = tk.Button(root, text="Send")
    submit.grid(row=1, column=4, padx=2, pady=10, sticky="e")

    def on_select(event):
        selected_option = dropdown.get()
        version = data[selected_option]
        global character
        character = Character(version['voice'], version['prompttemplate_add'], version['name'], version['conversation_pairs'])
        print(f"Selected Option: {character}")
        print(character.voice)
        print(character.prompttemplate_add)
        print(character.name)
        print(character.conversation_pairs)

    options = l
    
    dropdown = ttk.Combobox(root, values=options)
    dropdown.set("Select an option")
    
    dropdown.bind("<<ComboboxSelected>>", on_select)
    
    dropdown.grid(row=1, column=3, padx=10, pady=10)

    # Start the UI loop
    root.mainloop()

launchUI()