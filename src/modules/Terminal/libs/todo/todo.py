from ...locals import Action
from src.modules.FileManager import JSON


def todo(args: list[str]) -> list[Action]:
    todos: JSON = JSON("Terminal/data/todos.json")
    out = "\tERIVERTOS:\n"
    for item in todos["todos"]:
        out += f"- {item}\n"
    return [Action("terminal.output", [out])]
