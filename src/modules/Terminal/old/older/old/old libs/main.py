import os
from importlib import import_module as iimport
from importlib import reload as reimport

from rich import print as rprint


class Lib:
    def __init__(self, modules={}):
        self._modules = modules


def loadLibs(reload=False):
    LIBS_PATH = os.getcwd() + "\\libs"
    LIBS_PATH = (
        "C:\\Users\\danil\\OneDrive\\Coding\\Projects\\Python\\Os\\old libs\\old libs\\libs"
    )

    for lib in os.scandir(LIBS_PATH):
        if lib.is_dir():
            if not reload:
                module = iimport(f"libs.{lib.name}.commands")
            else:
                module = reimport(LIB._modules[lib.name])
            LIB._modules[lib.name] = module
            for command in dir(module):
                if command[0] != "_":
                    exec(f"LIB.{command} = module.{command}")
    rprint([i for i in dir(LIB) if i[0] != "_"])


LIB = Lib()
loadLibs()

os.system("cls")
while True:
    inp = input(">> ").split()
    if inp == ["exit"]:
        break
    elif inp == ["reload"]:
        loadLibs(reload=True)
    elif inp[0] == "help":
        try:
            LIB.help_(LIB, inp[1])
        except IndexError:
            LIB.help_(LIB, "help_")
    else:
        try:
            match len(inp):
                case 0:
                    continue
                case 1:
                    eval(f"LIB.{inp[0]}({LIB})")
                case 2:
                    eval(f"LIB.{inp[0]}(LIB, '{str(inp[1])}')")
                case _:
                    args = "'" + str(inp[1]) + "'"
                    for arg in inp[2:]:
                        args += ", '" + str(arg) + "'"
                    eval(f"LIB.{inp[0]}(LIB, {args})")
        except AttributeError:
            print("Command not found.")
        except SyntaxError:
            print("Command not found.")
        except Exception as e:
            print(e)

#############################

# from threading import Timer

# class RepeatedTimer(object):
#     def __init__(self, interval, function, *args, **kwargs):
#         self._timer = None
#         self.interval = interval
#         self.function = function
#         self.args = args
#         self.kwargs = kwargs
#         self.is_running = False
#         self.start()

#     def _run(self):
#         self.is_running = False
#         self.start()
#         self.function(*self.args, **self.kwargs)

#     def start(self):
#         if not self.is_running:
#             self._timer = Timer(self.interval, self._run)
#             self._timer.start()
#             self.is_running = True

#     def stop(self):
#         self._timer.cancel()
#         self.is_running = False
