import json

def load(key=False):
    with open("data.json") as file:
        data = json.load(file)
    if key or type(key) == int:
        return data[str(key)]
    else:
        return data

def save(self, data, key=False):
    if key:
        fulldata = self.load()
        fulldata[key] = data
        with open("data.json", "w") as file:
            json.dump(fulldata, file)
    else:
        with open("data.json", "w") as file:
            json.dump(data, file)