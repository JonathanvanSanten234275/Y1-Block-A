import json

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