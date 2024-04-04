"""A terminal emulator."""

from src.modules.Terminal.interpreter import Interpreter
from src.modules.Terminal.locals import Action, Response
from collections.abc import Iterator


class Terminal:
    """A terminal emulator.

    Attributes:
        inp_prefix (str): The prefix of the input.
        inp_text (str): The input text.
        text (list[str]): The text to display.
        inp_history (list[str]): The input history.
        inp_history_pos (int): The input history position.
        cursor_pos (int): The cursor position.
        interpreter (Interpreter): The interpreter.
        autocomplete_idx (int): The autocomplete index.
        completions (list[str]): The available autocompletions.
    """

    def __init__(self) -> None:
        self.inp_prefix: str = "> "
        self.inp_text: str = ""
        self.text: list[str] = []
        self.inp_history: list[str] = []
        self.inp_history_pos: int = 0
        self.cursor_pos: int = 0
        self.interpreter: Interpreter = Interpreter()
        self.autocomplete_idx: int = 0
        self.completions: list[str] = []

    def move_cursor(self, direction: int) -> None:
        """Move the cursor left or right.

        Args:
            direction (int): The direction to move the cursor.
        """
        self.cursor_pos += direction
        self.cursor_pos = max(0, min(self.cursor_pos, len(self.inp_text)))

    def move_cursor_word(self, direction: int) -> None:
        """Move the cursor by one word left or right.

        Args:
            direction (int): The direction to move the cursor.
        """
        if direction == 1:
            text = self.inp_text[self.cursor_pos :] + " "
            offset = 0
            while text.startswith(" "):
                text = text[1:]
                offset += 1
            self.move_cursor(text.find(" ") + offset)
        if direction == -1:
            text = " " + self.inp_text[: self.cursor_pos]
            offset = 0
            while text.endswith(" "):
                text = text[:-1]
                offset += 1
            self.move_cursor(-text[::-1].find(" ") - offset)

    def set_inp(self, inp: str) -> None:
        """Set the input text and cursor position.

        Args:
            inp (str): The text to set.
        """
        if inp != self.inp_text:
            self.inp_text = inp
            self.cursor_pos = len(self.inp_text)

    def write_inp(self, inp: str) -> None:
        """Write to the input text after the cursor.

        Args:
            inp (str): The text to write.
        """
        self.inp_text = (
            self.inp_text[: self.cursor_pos] + inp + self.inp_text[self.cursor_pos :]
        )
        self.move_cursor(len(inp))

    def backspace_inp(self) -> None:
        """Delete the character before the cursor."""
        if self.cursor_pos > 0:
            self.inp_text = (
                self.inp_text[: self.cursor_pos - 1] + self.inp_text[self.cursor_pos :]
            )
            self.move_cursor(-1)

    def delete_inp(self) -> None:
        """Delete the character after the cursor."""
        self.inp_text = (
            self.inp_text[: self.cursor_pos] + self.inp_text[self.cursor_pos + 1 :]
        )

    def clear(self) -> None:
        """Clear the console text."""
        self.text = []

    def move_inp_history(self, direction: int) -> None:
        """Move the input history up or down and set the input text."""
        if self.inp_history:
            self.inp_history_pos += direction
            self.inp_history_pos = max(
                0, min(self.inp_history_pos, len(self.inp_history) - 1)
            )
            self.set_inp(self.inp_history[self.inp_history_pos])

    def autocomplete(self) -> None:
        """Autocomplete the input text."""
        self.write_inp(self.get_current_autocomplete())

    def update_autocomplete(self) -> None:
        """Update the autocomplete list."""
        self.completions = self.interpreter.get_autocompletions(self.inp_text)
        self.autocomplete_idx = 0

    def move_autocomplete(self, direction: int) -> None:
        """Move the autocomplete index up or down."""
        self.autocomplete_idx += direction
        self.autocomplete_idx = max(0, min(self.autocomplete_idx, len(self.completions) - 1))

    def get_current_autocomplete(self) -> str:
        """Get the current autocompletion."""
        if self.completions:
            return self.completions[self.autocomplete_idx]
        return ""

    def run_inp(self) -> Iterator[Action]:
        """Run the input text."""
        self.text.append(self.inp_prefix + self.inp_text)

        response: Response = self.interpreter.run(self.inp_text)

        for action in response.actions:
            model = action.get_model()
            if model[0] == "terminal":
                match model[1]:
                    case "output":
                        if action.arg:
                            self.text.append(action.arg[0])
                    case "cls":
                        self.clear()
            else:
                yield action

        if self.inp_text:
            if self.inp_history:
                if self.inp_history[-1] != self.inp_text:
                    self.inp_history.append(self.inp_text)
            else:
                self.inp_history.append(self.inp_text)
        self.inp_history_pos = len(self.inp_history)
        self.move_cursor(-len(self.inp_text))
        self.inp_text = ""
