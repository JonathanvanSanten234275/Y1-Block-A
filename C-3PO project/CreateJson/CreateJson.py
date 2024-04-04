import json

# Create a Python dictionary (or list) with your data
data = {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}

# Convert the dictionary to a JSON string
json_string = json.dumps(data)

# Specify the filename for your JSON file
file_name = "my_data.json"

# Write the JSON string to a file
with open(file_name, "w") as json_file:
    json_file.write(json_string)

# Close the file
json_file.close()