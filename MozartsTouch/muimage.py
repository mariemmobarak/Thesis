# from datasets import load_dataset

# # Load the dataset
# dataset = load_dataset("MUImage")  # this works if it's available online; if local, pass the path

# # Print the features (labels/columns)
# print("Available labels/features:")
# print(dataset["train"].features)

# # Print a sample data entry
# print("\nExample entry:")
# print(dataset["train"][0])

import json

# Specify the path to your downloaded JSON file
json_file_path = 'MozartsTouch/MUImageInstructions.json'  

# Open the JSON file and load its contents
with open(json_file_path, 'r', encoding='utf8') as file:
    data = json.load(file)

# Print the loaded data to inspect it
print(data)