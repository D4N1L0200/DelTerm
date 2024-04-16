"""Miscellaneous commands."""

from ...locals import Action


def length(args: list[str]) -> list[Action]:
    """Count the length of a string.

    Args:
        args (list[str]): The arguments for the command.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    output = str(len(" ".join(args)))
    return [Action("terminal.output", [output])]


def echo(args: list[str]) -> list[Action]:
    """Echo the input.

    Args:
        args (list[str]): The arguments for the command.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    output = " ".join(args)
    return [Action("terminal.output", [output])]


def get_help() -> list[Action]:
    """Get help on a command.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    return [Action("terminal.help")]


def exit_term() -> list[Action]:
    """Exit the terminal.

    Returns:
        list[Action]: The resulting actions of the command.
    """
    return [Action("app.exit")]
