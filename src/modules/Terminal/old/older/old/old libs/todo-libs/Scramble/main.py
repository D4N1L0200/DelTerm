from random import choice

def fix(scramble):
    for i in scramble:
        if len(i)-1:
            
        break

scramble_size = 50
moveset = ["R", "R'", "L", "L'", "U", "U'", "D", "D'", "F", "F'", "B", "B'", ]

scramble = []
for i in range(scramble_size):
    scramble.append(choice(moveset))

out = scramble.pop(0)
for move in scramble:
    out += " " + move
print(out)