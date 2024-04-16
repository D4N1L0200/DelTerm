from .todo import *

commands = {
    "todo": {
        "type": "command",
        "func": todo,
        "desc": "Show todo list",
        "min_args": 0,
        "max_args": -1,
        "pass_args": True,
    }
}
