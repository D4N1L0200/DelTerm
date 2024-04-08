import os
from pathlib import Path


def index():
    return ["help_", "error_", "cmd", "cd", "cls", "dir", "sett", "show"]


def help_(libr, function=None):
    """
    Replies with a helpful message about the function.
        Usage:
        Get\\all\\commands> ?
        Get\\one\\command> ? <command name>
    """
    if not function:
        function = "help"
    try:
        eval(f"help(libr.{function})")
    except AttributeError:
        libr.error_(libr, f"Function <{function}> not found.")


def error_(libr, msg):
    print(f"\033[91m{msg}\033[0m")


def cmd(lib, *args):
    os.system(" ".join(args))


def cd(lib, path: str = ""):
    """
    Changes current directory.
        Usage:
        Change\\to\\path> cd <folder path>
    """
    if path == "/":
        next_dir: Path = Path(lib.settings.root)
    else:
        next_dir: Path = Path(lib.settings.current_dir) / path.lower()
    if next_dir.is_file():
        lib.error_(lib, "Cannot cd into a file.")
        return
    if next_dir.exists():
        os.chdir(next_dir)
        lib.settings.current_dir = os.getcwd()
    else:
        lib.error_(lib, f"Cannot cd into '{next_dir}' because it doesn't exist.")


def cls(lib):
    """
    Clears the terminal.
        Usage:
        Clear\\everything> cls
    """
    os.system("cls" if os.name == "nt" else "clear")


def dir(lib, path: str = ""):
    """
    Prints files and folders in directory.
        Usage:
        Print\\on\\current> dir
        Print\\on\\other> dir <folder path>
    """
    if path:
        folder_path = Path(lib.settings.current_dir) / path
        if not folder_path.exists():
            lib.error_(lib, "Cannot show folder contents because it does not exist.")
            return
        if folder_path.is_file():
            lib.error_(lib, "Cannot show a file, use 'show' instead.")
            return
        files: list[str] = []
        folders: list[str] = []
        for item in os.listdir(folder_path):
            if (folder_path / item).is_dir():
                folders.append(item)
            else:
                files.append(item)
        print(f"\\{folder_path.name}")
        [
            print(f"\t\\{folder}")
            for folder in folders
            if lib.settings.show_hidden_files
            or not (folder.startswith(".") or folder.startswith("_"))
        ]
        [
            print(f"\t{file}")
            for file in files
            if lib.settings.show_hidden_files
            or not (file.startswith(".") or file.startswith("_"))
        ]
    else:
        if Path(lib.settings.current_dir).is_file():
            lib.error_(lib, "Cannot show a file, use 'show' instead.")
            return
        files: list[str] = []
        folders: list[str] = []
        for item in os.listdir(lib.settings.current_dir):
            if (Path(lib.settings.current_dir) / item).is_dir():
                folders.append(item)
            else:
                files.append(item)
        print(f"\\{Path(lib.settings.current_dir).name}")
        [
            print(f"\t\\{folder}")
            for folder in folders
            if lib.settings.show_hidden_files
            or not (folder.startswith(".") or folder.startswith("_"))
        ]
        [
            print(f"\t{file}")
            for file in files
            if lib.settings.show_hidden_files
            or not (file.startswith(".") or file.startswith("_"))
        ]


def sett(lib, config: str = "", value: str = ""):
    """
    Gets or sets config parameters.
        Usage:
        Get\\all\\settings> set
        Get\\one\\setting> set <setting name>
        Set\\one\\setting> set <setting name> <type and value>
    """
    if value:
        if not hasattr(lib.settings, config):
            lib.error_(lib, f"No setting with name '{config}'.")
            return
        var_type, value = value.split(":", maxsplit=1)
        match var_type:
            # bool:path:str:int:float | bfips
            case "bool":
                if value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                else:
                    value = None
            case "str":
                value = str(value)
            case _:
                lib.error_(lib, f"Type '{var_type}' does not exist.")
                return
        lib.settings.__setattr__(config, value)
    if config:
        if not hasattr(lib.settings, config):
            lib.error_(lib, f"No setting with name '{config}'.")
            return
        value = lib.settings.__getattribute__(config)
        print(f"\t{config}: {value}")
    else:
        for key in lib.settings.__dict__:
            if not key.startswith("_"):
                value = lib.settings.__getattribute__(key)
                print(f"\t{key}: {value}")


def show(lib, path: str = ""):
    """
    Prints all contents of a file.
        Usage:
        Print\\single\\file> print <file path>
    """
    if not path:
        lib.error_(lib, "Please type a file path to show.")
        return
    file_path = Path(lib.settings.current_dir) / path
    if file_path.is_dir():
        lib.error_(lib, "Cannot print a folder, use 'dir' instead.")
        return
    try:
        with open(file_path, "r") as file:
            content = file.read()
            print(f"\n{content}\n")
    except FileNotFoundError:
        lib.error_(lib, f"The file at path '{file_path}' does not exist.")
