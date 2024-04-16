# from rich import print as rprint
#
#
# class Tape:
#     def __init__(self, inp, rules, state):
#         self.tape = [i for i in str(inp)]
#         self.pos = 0
#         self.rules = rules
#         self.state = state
#         self.halted = False
#         self.steps = 0
#
#     def move(self, direction):
#         if direction < 0:
#             if self.pos + direction < 0:
#                 self.pos = 0
#                 self.tape = ["_"] * (-1 * direction + self.pos) + self.tape
#             else:
#                 self.pos += direction
#         else:
#             self.pos += direction
#             if self.pos >= len(self.tape):
#                 self.tape += ["_"] * (self.pos - (len(self.tape) - 1))
#
#     def write(self, val):
#         self.tape[self.pos] = str(val)
#
#     def read(self):
#         return self.tape[self.pos]
#
#     def execute(self, commands):
#         val = str(self.read())
#         for rule in commands:
#             if val in rule:
#                 for idx, com in enumerate(commands[rule]):
#                     match com:
#                         case "R":
#                             self.move(commands[rule][idx + 1])
#                         case "L":
#                             self.move(-commands[rule][idx + 1])
#                         case "W":
#                             self.write(commands[rule][idx + 1])
#                         case "S":
#                             self.state = commands[rule][idx + 1]
#                         case "H":
#                             self.halted = True
#
#     def run(self):
#         while not self.halted:
#             if self.steps % 1 == 0:
#                 print(f"{self.steps}: {len(self.tape)}")
#             # print(f"{self.state}: {self.tape}")
#             self.execute(self.rules[self.state])
#             self.steps += 1
#         # print(self.tape)
#
#
# rules = {
#     "start": {"[0, 1]": ["R", 1], "[_]": ["L", 1, "S", "carry"]},
#     "carry": {"[1]": ["W", 0, "L", 1], "[0, _]": ["W", 1, "H"]},
# }
#
# # rules = {
# #     "A": {
# #         "[0, _]": ["W", 1, "R", 1, "S", "B"],
# #         "[1]": ["R", 1, "H"]
# #     },
# #     "B": {
# #         "[0, _]": ["W", 0, "R", 1, "S", "C"],
# #         "[1]": ["R", 1]
# #     },
# #     "C": {
# #         "[0, _]": ["W", 1, "L", 1],
# #         "[1]": ["L", 1, "S", "A"]
# #     },
# # }
#
# # rules = {
# #     "A": {
# #         "[0, _]": ["W", 1, "R", 1, "S", "B"],
# #         "[1]": ["L", 1, "S", "B"]
# #     },
# #     "B": {
# #         "[0, _]": ["W", 1, "L", 1, "S", "A"],
# #         "[1]": ["R", 1, "H"]
# #     }
# # }
#
# # rules = {
# #     "A": {
# #         "[0, _]": ["W", 1, "R", 1, "S", "B"],
# #         "[1]": ["L", 1, "S", "B"]
# #     },
# #     "B": {
# #         "[0, _]": ["W", 1, "L", 1, "S", "A"],
# #         "[1]": ["W", 0, "L", 1, "S", "C"]
# #     },
# #     "C": {
# #         "[0, _]": ["W", 1, "R", 1, "H"],
# #         "[1]": ["L", 1, "S", "D"]
# #     },
# #     "D": {
# #         "[0, _]": ["W", 1, "R", 1],
# #         "[1]": ["W", 0, "R", 1, "S", "A"]
# #     },
# # }
#
# # rules = {
# #     "A": {
# #         "[0, _]": ["W", 1, "R", 1, "S", "B"],
# #         "[1]": ["L", 1, "S", "C"]
# #     },
# #     "B": {
# #         "[0, _]": ["W", 1, "R", 1, "S", "C"],
# #         "[1]": ["R", 1]
# #     },
# #     "C": {
# #         "[0, _]": ["W", 1, "R", 1, "S", "D"],
# #         "[1]": ["W", 0, "L", 1, "S", "E"]
# #     },
# #     "D": {
# #         "[0, _]": ["W", 1, "L", 1, "S", "A"],
# #         "[1]": ["W", 0, "L", 1]
# #     },
# #     "E": {
# #         "[0, _]": ["W", 1, "R", 1, "H"],
# #         "[1]": ["W", 0, "L", 1, "S", "A"]
# #     },
# # }
#
# # rules = {
# #     "A": {
# #         "[0, _]": ["W", 1, "R", 1, "S", "B"],
# #         "[1]": ["L", 1, "S", "E"]
# #     },
# #     "B": {
# #         "[0, _]": ["W", 1, "L", 1, "S", "C"],
# #         "[1]": ["W", 0, "R", 1, "S", "A"]
# #     },
# #     "C": {
# #         "[0, _]": ["W", 1, "L", 1, "S", "D"],
# #         "[1]": ["W", 0, "R", 1, "S", "C"]
# #     },
# #     "D": {
# #         "[0, _]": ["W", 1, "L", 1, "S", "E"],
# #         "[1]": ["W", 0, "L", 1, "S", "F"]
# #     },
# #     "E": {
# #         "[0, _]": ["W", 1, "L", 1, "S", "A"],
# #         "[1]": ["L", 1, "S", "C"]
# #     },
# #     "F": {
# #         "[0, _]": ["W", 1, "L", 1, "S", "E"],
# #         "[1]": ["W", 1, "R", 1, "H"]
# #     },
# # }
#
# tape = Tape(1011101011111, rules, "start")
# rprint(tape.rules)
# tape.run()


class Turing: ...
