"""Todo commands."""

from ...locals import Action
from src.modules.FileManager import JSON


def todo(args: list[str]) -> list[Action]:
    """Todo list.

    Args:
        args (list[str]): The arguments for the command.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    todos: JSON = JSON("Terminal/data/todos.json")

    if not args:
        out = "\tTODOS:"
        for item in todos["todos"]:
            out += f"\n- {item}"
        return [Action("terminal.output", [out])]

    match args[0]:
        case "list":
            out = "\tTODOS:"
            for idx, item in enumerate(todos["todos"]):
                out += f"\n{idx + 1} - {item}"
            return [Action("terminal.output", [out])]

    if args[0] == "add":
        text = " ".join(args[1:])
        todos["todos"].append(text)
        todos.save()
        return [Action("terminal.output", ["Added todo: " + text])]

    if args[0] == "del":
        if num := int(args[1]) < 1 or int(args[1]) > len(todos["todos"]):
            return [Action("terminal.output", ["No such todo: " + args[1]])]
        del todos["todos"][num - 1]
        todos.save()
        return [Action("terminal.output", ["Deleted todo: " + str(args[1])])]
