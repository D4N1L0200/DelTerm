import os, json

reset_state = { "started": False, "player": {} }

path = os.path.abspath(os.getcwd()) + "/data.json"
with open(path, 'w') as file:
    json.dump(reset_state, file)