import os

from pathlib import Path

import tkinter
from tkinter import filedialog

from importlib import import_module as iimport
from importlib import reload as reimport

from json_handler import JSONObj

from libs.info.commands import info


class Lib:
    def __init__(self, modules=None):
        if modules is None:
            modules = {}
        self.commands = []
        self.modules = modules
        self.settings: JSONObj = JSONObj(
            os.getcwd() + "/data/settings.json"
        )
        # self.settings: JSONObj = JSONObj(
        #     "C:\\Users\\danil\\Documents\\Coding\\Os\\data\\settings.json"
        # )

    def help_(self, libr, param):
        pass

    def error_(self, libr, msg):
        pass


def load_libs(reload=False):
    libs_path = lib.settings.libs_path
    lib.commands = []

    for libr in os.scandir(libs_path):
        if libr.is_dir():
            if not reload:
                module = iimport(f"libs.{libr.name}.commands")
            else:
                module = reimport(lib.modules[libr.name])
            lib.modules[libr.name] = module
            commands = module.index()
            for cmd in commands:
                try:
                    exec(f"lib.{cmd} = module.{cmd}")
                except AttributeError:
                    lib.error_(
                        lib,
                        f"The module '{str(libr.name)}' does not have the command '{str(cmd)}'.",
                    )
            lib.commands = [*lib.commands, *commands]


lib = Lib()
while True:
    try:
        load_libs()
        break
    except FileNotFoundError:
        lib.error_(
            lib,
            f"Cannot find os folder '{lib.settings.os_path}', please select one in the dialog box",
        )
        tkinter.Tk().withdraw()
        lib.settings.os_path = str(Path(filedialog.askdirectory()))
        lib.settings.libs_path = str(Path(lib.settings.os_path) / "libs")
        lib.settings.data_path = str(Path(lib.settings.os_path) / "data")

root: Path = Path(lib.settings.root)
while True:
    try:
        os.chdir(root)
        break
    except FileNotFoundError:
        lib.error_(
            lib,
            f"Cannot find root folder '{lib.settings.root}', please select one in the dialog box",
        )
        tkinter.Tk().withdraw()
        lib.settings.root = str(Path(filedialog.askdirectory()))
        root = Path(lib.settings.root)

info(lib)
while True:
    inp = input(f"{lib.settings.current_dir}> ")
    if not inp:
        continue
    inp = inp.replace("\\", "\\\\")
    inp = inp.replace("/", "\\\\")
    split_inp: list[str] = inp.split()
    match split_inp[0]:
        case "exit":
            break
        case "reload":
            load_libs(reload=True)
        case "?":
            try:
                lib.help_(lib, split_inp[1])
            except IndexError:
                out = []
                for command in sorted(lib.commands):
                    if not command.endswith("_"):
                        out.append(command)
                print(out)
        case _:
            if not hasattr(lib, split_inp[0]):
                lib.error_(lib, f"Unknown command: {split_inp[0]}")
                continue
            match len(split_inp):
                case 1:
                    eval(f"lib.{split_inp[0]}(lib)")
                case 2:
                    eval(f"lib.{split_inp[0]}(lib, '{str(split_inp[1])}')")
                case _:
                    args = "'" + str(split_inp[1]) + "'"
                    for arg in split_inp[2:]:
                        args += ", '" + str(arg) + "'"
                    eval(f"lib.{split_inp[0]}(lib, {args})")
            # except TypeError:
            #     lib.error_(lib, "Too many or too little arguments.")
