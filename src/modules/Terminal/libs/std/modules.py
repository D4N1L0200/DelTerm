"""Modules related commands."""

from ...locals import Action


def modules(args: list[str]) -> list[Action]:
    """Manage installed modules.

    Args:
        args (list[str]): The arguments for the command.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    if not args:
        return [Action("terminal.modules.get")]

    match args[0]:
        case "reload":
            return [
                Action("terminal.modules.reload", args[1:]),
            ]
        case "load":
            return [
                Action("terminal.modules.load", args[1:]),
            ]
        case "unload":
            return [
                Action("terminal.modules.unload", args[1:]),
            ]
