import os, json

def cls():
    os.system("cls")

class Game:
    def __init__(self):
        self.loadData()
        if self.data["started"]:
            # self.continueSave()
            pass
        else:
            self.startSave()

    def yorn(self, question):
        confirm = input(f"{question} (s/n) ").lower()
        if "s" in confirm:
            return True
        else:
            return False

    def loadData(self):
        path = os.path.abspath(os.getcwd()) + "/data.json"
        with open(path, 'r') as file:
            data = json.load(file)    
        self.data = data

    def save_data(self):
        path = os.path.abspath(os.getcwd()) + "/data.json"
        with open(path, 'w') as file:
            json.dump(self.data, file)

    def startSave(self):
        self.player = Character(self.yorn).create()
        self.data["player"]["name"] = self.player.name
        self.data["player"]["maxhp"] = self.player.maxhp
        self.data["started"] = True
        self.save_data()

class Character:
    def __init__(self, yorn):
        self.yorn = yorn
        self.name = "Player Name"
        self.maxhp = 100
        self.hp = 100
    
    def create(self):
        cls()
        while True:
            name = input("Qual é o seu nome? ").title()
            confirm = self.yorn(f"Tem certeza que quer usar '{name}'?")
            if confirm:
                self.name = name
                break
        return self

game = Game()
print("Digaí macho, cê caiu aqui, nem sei quem é tu, mas sinto que você vai precisar de ajuda.")
print("Você morreu.")
