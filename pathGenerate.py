import os, json

directory = os.path.dirname(__file__) + "\\config"
directory = directory.replace("\\", "/")
# print(directory)
data = {
    "CONFIG_PATH" : directory
}

with open('src/config.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)