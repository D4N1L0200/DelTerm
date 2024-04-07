from ...locals import Action


def cls() -> list[Action]:
    return [Action("terminal.cls")]


def resize(args: list[str]) -> list[Action]:
    return [Action("terminal_screen.resize", [int(args[0]), int(args[1])])]


def rescale(args: list[str]) -> list[Action]:
    return [Action("terminal_screen.rescale", [float(args[0]), float(args[1])])]


def sset(args: list[str]) -> list[Action]:
    return [Action("terminal.set.set", args)]


def sget(args: list[str]) -> list[Action]:
    return [Action("terminal.set.get", args)]


def sreload() -> list[Action]:
    return [Action("terminal.set.reload")]
