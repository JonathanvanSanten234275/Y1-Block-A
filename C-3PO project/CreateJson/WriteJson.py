import json

def ChangeJSON(file_name, new_character, new_prompttemplate):
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    data[new_character] = {"prompttemplate_add" : new_prompttemplate}
    with open(file_name, "w") as json_file:
        json.dump(data, json_file)
    
ChangeJSON("character_data2.json", "AI assitant", "The most helpful AI assistant")