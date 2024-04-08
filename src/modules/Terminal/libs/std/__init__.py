from .misc import *
from .terminal import *
from .modules import *

commands = {
    "len": {
        "func": lenght,
        "desc": "Count the length of a string",
        "min_args": 1,
        "max_args": -1,
        "pass_args": True,
    },
    "echo": {
        "func": echo,
        "desc": "Echo the input",
        "min_args": 1,
        "max_args": -1,
        "pass_args": True,
    },
    "help": {
        "func": get_help,
        "desc": "Get help on a command",
        "min_args": 0,
        "max_args": -1,
        "pass_args": False,
    },
    "exit": {
        "func": exit_term,
        "desc": "Exit the terminal",
        "min_args": 0,
        "max_args": -1,
        "pass_args": False,
    },
    "cls": {
        "func": cls,
        "desc": "Clear the terminal",
        "min_args": 0,
        "max_args": -1,
        "pass_args": False,
    },
    "resize": {
        "func": resize,
        "desc": "Resize the terminal screen",
        "min_args": 2,
        "max_args": 2,
        "pass_args": True,
    },
    "rescale": {
        "func": rescale,
        "desc": "Rescale the terminal screen",
        "min_args": 2,
        "max_args": 2,
        "pass_args": True,
    },
    "sset": {
        "func": sset,
        "desc": "Set a setting in the terminal",
        "min_args": 2,
        "max_args": -1,
        "pass_args": True,
    },
    "sget": {
        "func": sget,
        "desc": "Get a setting in the terminal",
        "min_args": 1,
        "max_args": 1,
        "pass_args": True,
    },
    "sreload": {
        "func": sreload,
        "desc": "Reload the settings in the terminal",
        "min_args": 0,
        "max_args": -1,
        "pass_args": False,
    },
    "modules": {
        "func": modules,
        "desc": "Get and manage modules",
        "min_args": 0,
        "max_args": -1,
        "pass_args": True,
    },
}
