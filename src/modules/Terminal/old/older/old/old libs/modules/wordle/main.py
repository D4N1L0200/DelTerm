import os
import json
import time
import random
from threading import Timer

def _load(file, key=False):
    path = f"{os.path.abspath(os.getcwd())}/modules/idleminer/data/{file}.json"
    with open(path) as file:
        data = json.load(file)
    if key or type(key) == int:
        return data[str(key)]
    else:
        return data


def _save(file, data, key=False):
    if key:
        path = f"{os.path.abspath(os.getcwd())}/modules/idleminer/data/{file}.json"
        fulldata = _load(file)
        fulldata[key] = data
        with open(path, "w") as file:
            json.dump(fulldata, file)
    else:
        path = f"{os.path.abspath(os.getcwd())}/modules/idleminer/data/{file}.json"
        with open(path, "w") as file:
            json.dump(data, file)



def _init():
    os.system("cls")
    data = _load("save")
    if not data["started"]:
        data["started"] = True
        _save("save", data)
        print("Your profile has been created! [profile]")
        print("You will now automatically receive items in your backpack, use [sell]  to sell them.")
        print("Use [guide] for more information on how to play!")
        print("You can reset your profile at any time with [reset]")
    return "[Wordle]"


def _exit():
    print("Goodbye!")

def _wordinp(word):
    if _get("isplaying"):
        print("yes")
    else:
        print("no")

def _notfound(word):
    # try:
    _wordinp(str(word))
    # except something:
    # print("Command not found.")


def reset(confirm=["no"]):
    if confirm[0] == "confirm":
        print("A")
    else:
        print("B")
