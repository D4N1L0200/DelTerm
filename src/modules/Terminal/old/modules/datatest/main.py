import os
import json

def _load(key=False):
    with open(datapath) as file:
        data = json.load(file)
    if key or type(key) == int:
        return data[str(key)]
    else:
        return data


def _save(data, key=False):
    if key:
        fulldata = _load()
        fulldata[key] = data
        with open(datapath, "w") as file:
            json.dump(fulldata, file)
    else:
        with open(datapath, "w") as file:
            json.dump(data, file)



def _init():
    os.system("cls")
    global datapath
    datapath = f"{os.path.abspath(os.getcwd())}/modules/datatest/data.json"
    return "[DataTest]"


def _exit():
    print("Goodbye!")


def _notfound():
    print("Command not found.")

def run():
    data = _load()
    for key in data:
        print(f"{key}: {data[key]}")