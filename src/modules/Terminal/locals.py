class Action:
    def __init__(self, model: str, arg: list = None) -> None:
        if arg is None:
            arg = []
        self.model: str = model
        self.arg: list = arg

    def get_model(self) -> list[str]:
        return self.model.split(".")


class Response:
    def __init__(self, title: str) -> None:
        self.title: str = title
        self.actions: list[Action] = []

    def add_action(self, action: Action) -> None:
        self.actions.append(action)

    def unknown(self) -> None:
        self.actions.append(Action("terminal.output", ["Unknown command."]))

    def bad_args(self, arg_len: int, min_args: int, max_args: int = -1) -> None:
        if arg_len < min_args:
            self.actions.append(Action("terminal.output", ["Not enough arguments."]))
        elif max_args != -1 and arg_len > max_args:
            self.actions.append(Action("terminal.output", ["Too many arguments."]))
        else:
            raise ValueError
