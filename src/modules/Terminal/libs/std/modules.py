from ...locals import Action


def modules(args: list[str]) -> list[Action]:
    output = "To be done.\n"
    return [Action("terminal.output", [output])]
