import json

# Ensure the file is opened with UTF-8 encoding when reading
with open("test.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Ensure the file is written with UTF-8 encoding
with open("test_refactored.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
