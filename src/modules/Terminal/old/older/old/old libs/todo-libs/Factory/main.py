import os
import utils

class factory:
    def __init__(self, savedata):
        self.savedata = savedata
        self.money = savedata["money"]
        self.inv = savedata["inv"]
        self.prices = savedata["prices"]

    def display(self, page="resources"):
        match page:
            case "resources":
                for item in self.inv["resources"]:
                    print(str(item) + ": " + str(self.inv["resources"][item]))
            case "prices":
                print("Item: buy - sell\n")
                for item in self.prices["resources"]:
                    buyprice = self.prices["resources"][item]["buy"]
                    sellprice = self.prices["resources"][item]["sell"]
                    print(f"{item.capitalize()}: R$ {buyprice} - R$ {sellprice}")

    def buy(self, ammount, item):
        buyprice = round(self.prices["resources"][item]["buy"] * float(ammount), 2)
        if self.money >= buyprice:
            self.money -= buyprice
            self.inv["resources"][item] += int(ammount)
            print(f"Bought {str(ammount)} {item} for R$ {buyprice}")
        else:
            print(f"You need R$ {round(buyprice - self.money, 2)} more to buy this.")

if __name__ == "__main__":
    os.system("cls")
    savedata = utils.load()
    factory = factory(savedata)
    while True:
        inp = input(">>> ").lower().split()
        match inp[0]:
            case "buy":
                item = ""
                ammount = inp[1]
                for name_ in inp[2:]:
                    item = item + str(name_)
                factory.buy(ammount, item)
            case "resources":
                factory.display("resources")
            case "prices":
                factory.display("prices")