import json

with open('pygame_project/level/World.json') as json_file:
    data = json.load(json_file)
    print(data['layers'])
