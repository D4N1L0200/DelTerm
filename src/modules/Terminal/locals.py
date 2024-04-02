from typing import Self


class Action:
    def __init__(self, model: str, arg: tuple) -> None:
        self.model: str = model
        self.arg: tuple = arg

    def get_model(self) -> list[str]:
        return self.model.split(".")


class Response:
    def __init__(self, title: str) -> None:
        self.title: str = title
        self.actions: list[Action] = []

    def add_action(self, model_name: str, *args) -> Self:
        self.actions.append(Action(model_name, args))
        return self
