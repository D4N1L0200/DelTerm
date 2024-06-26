"""The standard library used in the terminal."""

import src.modules.Terminal.libs.std.misc as misc
import src.modules.Terminal.libs.std.terminal as terminal
import src.modules.Terminal.libs.std.modules as modules
import src.modules.Terminal.libs.std.numbers as numbers

commands = {
    "len": {
        "type": "command",
        "func": misc.length,
        "desc": "Count the length of a string",
        "min_args": 1,
        "max_args": -1,
        "pass_args": True,
    },
    "echo": {
        "type": "command",
        "func": misc.echo,
        "desc": "Echo the input",
        "min_args": 1,
        "max_args": -1,
        "pass_args": True,
    },
    "help": {
        "type": "command",
        "func": misc.get_help,
        "desc": "Get help on a command",
        "min_args": 0,
        "max_args": -1,
        "pass_args": False,
    },
    "exit": {
        "type": "command",
        "func": misc.exit_term,
        "desc": "Exit the terminal",
        "min_args": 0,
        "max_args": -1,
        "pass_args": False,
    },
    "terminal": {
        "type": "category",
        "cls": {
            "type": "command",
            "func": terminal.cls,
            "desc": "Clear the terminal",
            "min_args": 0,
            "max_args": -1,
            "pass_args": False,
        },
        "resize": {
            "type": "command",
            "func": terminal.resize,
            "desc": "Resize the terminal screen",
            "min_args": 2,
            "max_args": 2,
            "pass_args": True,
        },
        "rescale": {
            "type": "command",
            "func": terminal.rescale,
            "desc": "Rescale the terminal screen",
            "min_args": 2,
            "max_args": 2,
            "pass_args": True,
        },
        "sset": {
            "type": "command",
            "func": terminal.sset,
            "desc": "Set a setting in the terminal",
            "min_args": 2,
            "max_args": -1,
            "pass_args": True,
        },
        "sget": {
            "type": "command",
            "func": terminal.sget,
            "desc": "Get a setting in the terminal",
            "min_args": 1,
            "max_args": 1,
            "pass_args": True,
        },
        "sreload": {
            "type": "command",
            "func": terminal.sreload,
            "desc": "Reload the settings in the terminal",
            "min_args": 0,
            "max_args": -1,
            "pass_args": False,
        },
    },
    "modules": {
        "type": "command",
        "func": modules.modules,
        "desc": "Manage installed modules",
        "min_args": 0,
        "max_args": -1,
        "pass_args": True,
    },
    "numbers": {
        "type": "category",
        "calc": {
            "type": "command",
            "func": numbers.calc,
            "desc": "Calculate a math expression",
            "min_args": 1,
            "max_args": -1,
            "pass_args": True,
        },
        "convert": {
            "type": "command",
            "func": numbers.convert,
            "desc": "Convert numbers to another unit",
            "min_args": 2,
            "max_args": 2,
            "pass_args": True,
        },
    },
}
