"""Action and Response classes for the Terminal module."""


class Action:
    """An action for the Terminal module.

    Attributes:
        model (str): The model of the action.
        arg (list): The arguments of the action.
    """

    def __init__(self, model: str, arg: list = None) -> None:
        if arg is None:
            arg = []
        self.model: str = model
        self.arg: list = arg

    def get_model(self) -> list[str]:
        """Get the model in a list."""
        return self.model.split(".")


class Response:
    """A response for the Terminal module.

    Attributes:
        title (str): The title of the response.
        actions (list): The actions of the response.
    """

    def __init__(self, title: str) -> None:
        self.title: str = title
        self.actions: list[Action] = []

    def add_action(self, action: Action) -> None:
        """Add an action to the response."""
        self.actions.append(action)

    def unknown(self) -> None:
        """Add an action for an unknown command to the response."""
        self.actions.append(Action("terminal.output", ["Unknown command."]))

    def bad_args(self, arg_len: int, min_args: int, max_args: int = -1) -> None:
        """Add an action for bad arguments to the response."""
        if arg_len < min_args:
            self.actions.append(Action("terminal.output", ["Not enough arguments."]))
        elif max_args != -1 and arg_len > max_args:
            self.actions.append(Action("terminal.output", ["Too many arguments."]))
        else:
            raise ValueError
