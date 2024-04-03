"""An interpreter for the terminal emulator."""

from src.modules.Terminal.locals import Response


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
        spl_inp = inp_text.split(" ")
        title = spl_inp[0]
        args = spl_inp[1:]

        match title:
            case "len":
                output = str(len(inp_text[4:]))
                response = Response(title).add_action("terminal.output", output)
            case "echo":
                output = " ".join(args)
                response = Response(title).add_action("terminal.output", output)
            case "cls":
                response = Response(title).add_action("terminal.cls")
            case "resize":
                response = Response(title).add_action("terminal_screen.resize", *args)
            case "rescale":
                response = Response(title).add_action("terminal_screen.rescale", *args)
            case _:
                output = "Unknown command."
                response = Response(title).add_action("terminal.output", output)
        return response
