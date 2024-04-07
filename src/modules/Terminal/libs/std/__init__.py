from .misc import *
from .terminal import *

commands = {
    "len": {"func": lenght, "min_args": 1, "max_args": -1, "pass_args": True},
    "echo": {"func": echo, "min_args": 1, "max_args": -1, "pass_args": True},
    "help": {"func": get_help, "min_args": 0, "max_args": -1, "pass_args": False},
    "exit": {"func": exit_term, "min_args": 0, "max_args": -1, "pass_args": False},
    "cls": {"func": cls, "min_args": 0, "max_args": -1, "pass_args": False},
    "resize": {"func": resize, "min_args": 2, "max_args": 2, "pass_args": True},
    "rescale": {"func": rescale, "min_args": 2, "max_args": 2, "pass_args": True},
    "sset": {"func": sset, "min_args": 2, "max_args": -1, "pass_args": True},
    "sget": {"func": sget, "min_args": 1, "max_args": 1, "pass_args": True},
    "sreload": {"func": sreload, "min_args": 0, "max_args": -1, "pass_args": False},
}
