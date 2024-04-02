"""An interpreter for the terminal emulator."""

from modules.Terminal.locals import Response


class Interpreter:
    """An interpreter for the terminal emulator."""

    def __init__(self):
        pass

    @staticmethod
    def run(inp_text: str) -> Response:
        """Run a command.

        Args:
            command (str): The command to run.

        Returns:
            str: The output of the command.
        """
        if inp_text[:3] == "len":
            output = str(len(inp_text[4:]))
            response = Response(output)
        elif inp_text == "cls":
            output = ""
            response = Response(output)
        else:
            output = "-1"
            response = Response(output)
        return response
