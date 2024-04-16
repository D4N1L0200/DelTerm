"""A terminal emulator."""

from .interpreter import Interpreter
from .locals import Action, Response
from collections.abc import Iterator
from src.modules.FileManager import JSON


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
        self.inp_text: str = ""
        self.text: list[str] = []
        self.inp_history: list[str] = []
        self.inp_history_pos: int = 0
        self.cursor_pos: int = 0
        self.interpreter: Interpreter = Interpreter()
        self.autocomplete_idx: int = 0
        self.completions: list[str] = []
        self.set: JSON = JSON("Terminal/data/settings.json")
        self.inp_prefix: str = ""
        self.inp_history_size: int = 0
        self.chat_history_size: int = 0
        self.reload_settings()

    def reload_settings(self) -> None:
        """Reload the settings."""
        self.inp_prefix = self.set["terminal"]["prefix"]
        self.inp_history_size = self.set["terminal"]["inp_history_size"]
        self.chat_history_size = self.set["terminal"]["chat_history_size"]

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
        self.completions = self.interpreter.get_auto_completions(self.inp_text)
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
                    case "help":
                        def parse_items(block: dict[str, dict], indent: int = 1) -> None:
                            for name, item in block.items():
                                if name == "type":
                                    continue
                                if item["type"] == "category":
                                    self.text.append(f"{"\t" * indent}{name.title()}:")
                                    parse_items(item, indent + 1)
                                else:
                                    self.text.append(f"{"\t" * indent}{name}: {item['desc']}")

                        for module in self.interpreter.modules:
                            self.text.append(f"{module.title()}:")
                            parse_items(self.interpreter.modules[module])
                            self.text.append("")
                    case "cls":
                        self.clear()
                    case "set":
                        match model[2]:
                            case "get":
                                self.text.append(f"{action.arg[0]}: {self.set["terminal"][action.arg[0]]}\n")
                            case "set":
                                try:
                                    val = int(action.arg[1])
                                except ValueError:
                                    val = " ".join(action.arg[1:])
                                self.set["terminal"][action.arg[0]] = val
                                self.set.save()
                                self.text.append(f"{action.arg[0]}: {self.set["terminal"][action.arg[0]]}\n")
                            case "reload":
                                self.reload_settings()
                                self.text.append("All settings reloaded\n")
                    case "modules":
                        match model[2]:
                            case "get":
                                self.text.append(f"Modules: {self.interpreter.get_modules()}\n")
                            case "load":
                                if action.arg:
                                    self.interpreter.load_modules(action.arg)
                                else:
                                    self.interpreter.load_modules()
                                self.text.append("Modules loaded\n")
                            case "unload":
                                if action.arg:
                                    self.interpreter.unload_modules(action.arg)
                                else:
                                    self.interpreter.unload_modules()
                                self.text.append("Modules unloaded\n")
                            case "reload":
                                if action.arg:
                                    self.interpreter.reload_modules(action.arg)
                                else:
                                    self.interpreter.reload_modules()
                                self.text.append("Modules reloaded\n")
            else:
                yield action

        for idx, line in enumerate(self.text):
            line = line.replace("\t", " " * 4)
            newline = line.find("\n")
            if newline != -1:
                self.text.insert(idx + 1, line[newline + 1 :])
                self.text[idx] = line[:newline]
            else:
                self.text[idx] = line

        if len(self.text) >= self.chat_history_size:
            self.text = self.text[-self.chat_history_size + 1:]

        if self.inp_text:
            if self.inp_history:
                if self.inp_history[-1] != self.inp_text:
                    self.inp_history.append(self.inp_text)
            else:
                self.inp_history.append(self.inp_text)

        if len(self.inp_history) >= self.inp_history_size:
            self.inp_history = self.inp_history[-self.inp_history_size:]

        self.inp_history_pos = len(self.inp_history)
        self.move_cursor(-len(self.inp_text))
        self.inp_text = ""
