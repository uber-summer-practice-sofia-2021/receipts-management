import os

directory = os.path.dirname(__file__) + "/src/config.json"
#print(directory)
os.remove(directory)
