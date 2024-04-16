"""The todo module for the terminal."""

from .todo import *

commands = {
    "todo": {
        "type": "command",
        "func": todo,
        "desc": "Todo list",
        "min_args": 0,
        "max_args": -1,
        "pass_args": True,
    }
}
