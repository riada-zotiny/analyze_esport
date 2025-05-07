import json 


# Ouverture des fichiers json 

def open_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


data = open_json('dataMouseKeybord/mouse_actions.json')    
print(data)

counter = 0
for element in data:
    counter += 1
    print("Cet elements ", counter, " est ", element)