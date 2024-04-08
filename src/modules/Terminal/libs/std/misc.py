from ...locals import Action


def lenght(args: list[str]) -> list[Action]:
    output = str(len(" ".join(args))) + "\n"
    return [Action("terminal.output", [output])]


def echo(args: list[str]) -> list[Action]:
    output = " ".join(args) + "\n"
    return [Action("terminal.output", [output])]


def get_help() -> list[Action]:
    return [Action("terminal.help")]


def exit_term() -> list[Action]:
    return [Action("app.exit")]
