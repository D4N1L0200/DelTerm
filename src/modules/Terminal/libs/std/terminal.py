"""Terminal related commands."""

from ...locals import Action


def cls() -> list[Action]:
    """Clear the terminal.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    return [Action("terminal.cls")]


def resize(args: list[str]) -> list[Action]:
    """Resize the terminal screen.

    Args:
        args (list[str]): The arguments for the command.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    return [Action("terminal_screen.resize", [int(args[0]), int(args[1])])]


def rescale(args: list[str]) -> list[Action]:
    """Rescale the terminal screen.

    Args:
        args (list[str]): The arguments for the command.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    return [Action("terminal_screen.rescale", [float(args[0]), float(args[1])])]


def sset(args: list[str]) -> list[Action]:
    """Set a setting in the terminal.

    Args:
        args (list[str]): The arguments for the command.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    return [Action("terminal.set.set", args)]


def sget(args: list[str]) -> list[Action]:
    """Get a setting in the terminal.

    Args:
        args (list[str]): The arguments for the command.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    return [Action("terminal.set.get", args)]


def sreload() -> list[Action]:
    """Reload the settings in the terminal.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    return [Action("terminal.set.reload")]
