"""An interpreter for the terminal emulator."""

from .locals import Response
from .libs.std import commands


class Interpreter:
    """An interpreter for the terminal emulator."""

    def __init__(self):
        self.commands: dict[str, dict] = commands

    def run(self, inp_text: str) -> Response:
        """Parse an input and return the response.

        Args:
            inp_text (str): The input text.

        Returns:
            Response: The response for the input.
        """

        spl_inp = inp_text.split(" ")
        title = spl_inp[0]
        response = Response(title)

        if title not in self.commands:
            response.unknown()
            return response

        args = spl_inp[1:]
        arg_len = len(args)
        command = self.commands[title]

        if arg_len < command["min_args"] or (
            command["max_args"] != -1 and arg_len > command["max_args"]
        ):
            response.bad_args(arg_len, command["min_args"], command["max_args"])
            return response

        if command["pass_args"]:
            actions = command["func"](args)
        else:
            actions = command["func"]()

        for action in actions:
            response.add_action(action)
        return response

    @staticmethod
    def get_auto_completions(inp_text: str) -> list[str]:
        """Autocomplete the input text.

        Args:
            inp_text (str): The input text.

        Returns:
            list[str]: The available completions.
        """
        return ["test", "other", "this", inp_text]
