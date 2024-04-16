import os
import json
import time
import random
from threading import Timer


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


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


def _genitems():
    data = _load("save")
    mine = _load("mine", data["level"])
    if not data["itemammount"] >= data["backpackmax"]:
        data["itemammount"] += 1
        data["blocksbroken"] += 1

        choices = []
        for item, weight in mine.items():
            choices.extend([item] * weight)
        item = random.choice(choices)
        data["items"][str(item)] += 1
        _save("save", data)


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
    global rt
    rt = RepeatedTimer(1, _genitems)
    return "[IdleMiner]"


def _exit():
    rt.stop()
    print("Goodbye!")


def _notfound():
    print("Command not found.")


def sell():
    data = _load("save")
    money = data["money"]
    itemammount = data["itemammount"]
    items = data["items"]

    if itemammount:
        itemss = "items" if itemammount > 1 else "item"
        fillpercentage = round(itemammount / data["backpackmax"] * 100, 2)
        print(f"Sold {itemammount} {itemss} from your backpack ({fillpercentage}%)")

        prices = _load("mine", 0)
        selltotal = 0
        for item in items:
            if items[item]:
                price = prices[item] * items[item]
                selltotal += price
                print(f"{item.capitalize()} x{items[item]} | ${price}")
                items[item] = 0

        print(f"Total: ${selltotal}")
        money += selltotal
        print(f"You now have ${money}")

        data["money"] = money
        data["itemammount"] = 0
        _save("save", data)
    else:
        print("Your backpack needs time to fill up so there's no point in spamming this command")


# TODO
# def help(args):
#     if not args:
#         print("This is the default help message.")
#     else:
#         try:
#             helpstr = gethelp(float(args))
#             for key in helpstr:
#                 print(helpstr[key])
#         except ValueError:
#             helpstr = gethelp(str(args))
#             for key in helpstr:
#                 print(helpstr[key])


def reset(confirm=["no"]):
    global resettime
    if confirm[0] == "confirm":
        currenttime = time.time()
        if currenttime - resettime < 10:
            rt.stop()
            data = _load("starter")
            _save("save", data)
            _init()
            rt.start()
            resettime = 0
        else:
            print("Time ran out, use [reset] again.")
    else:
        print("This will fully reset all your data with no way back.")
        print("If you are sure you want to do this, use [reset confirm] in the next 10 seconds.")
        resettime = time.time()
