"""An interpreter for the terminal emulator."""


class Interpreter:
    """An interpreter for the terminal emulator."""

    def __init__(self) -> None:
        pass

    @staticmethod
    def run(command: str) -> str:
        """Run a command.

        Args:
            command (str): The command to run.

        Returns:
            str: The output of the command.
        """
        return str(len(command))
