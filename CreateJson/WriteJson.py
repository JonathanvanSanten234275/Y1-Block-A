import json

# Specify the filename of the JSON file you want to update
file_name = "my_data.json"

# Read the existing JSON data from the file
with open(file_name, "r") as json_file:
    data = json.load(json_file)

# Modify the data as needed
data["age"] = 31
data["city"] = "Los Angeles"

# Open the same JSON file in write mode
with open(file_name, "w") as json_file:
    # Write the updated data back to the file
    json.dump(data, json_file)

# The JSON file has been updated with the new data