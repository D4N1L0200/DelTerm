"""An interpreter for the terminal emulator."""

import os
import sys
from pathlib import Path
from importlib import import_module

from .locals import Response


class Interpreter:
    """An interpreter for the terminal emulator."""

    def __init__(self):
        self.commands: dict[str, str] = {}
        self.modules: dict[str, dict[str, dict]] = {}

        self.load_modules()

    def get_modules(self) -> list[str]:
        return list(self.modules)

    def load_modules(self, modules=None) -> None:
        def load(mod_name: str) -> None:
            def parse_items(block: dict[str, dict], curr_name: str = "") -> None:
                for name, item in block.items():
                    if name == "type":
                        continue
                    if item["type"] == "category":
                        if curr_name:
                            parse_items(item, f"{curr_name}.{name}")
                        else:
                            parse_items(item, name)
                    else:
                        if curr_name:
                            self.commands[name] = f"{mod_name}.{curr_name}"
                        else:
                            self.commands[name] = mod_name

            module = import_module(f".{mod_name}", "src.modules.Terminal.libs")
            commands: dict[str, dict] = module.commands

            parse_items(commands)

            self.modules[mod_name] = commands

        if modules is None:
            modules = []

        if not modules:
            libs_path: Path = Path(
                os.path.join(os.getcwd(), "src/modules/Terminal/libs")
            )
            for lib_folder in os.scandir(libs_path):
                if not lib_folder.is_dir() or lib_folder.name.startswith("_"):
                    continue

                load(lib_folder.name)
        else:
            for module_name in modules:
                load(module_name)

    def unload_modules(self, modules: list = None, allow_std: bool = False) -> None:
        if modules is None:
            modules = list(self.modules.keys())

        if not allow_std and "std" in modules:
            modules.remove("std")

        for module in modules.copy():
            for command in self.modules[module]:
                del self.commands[command]
            del self.modules[module]

            module = f"src.modules.Terminal.libs.{module}"
            for sys_module in sys.modules.copy():
                if sys_module.startswith(module):
                    del sys.modules[sys_module]

    def reload_modules(self, modules: list = None) -> None:
        if modules is None:
            modules = list(self.modules.keys())

        self.unload_modules(modules, allow_std=True)
        if modules:
            self.load_modules(modules)
        else:
            self.load_modules()

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

        args: list[str] = spl_inp[1:]
        arg_len: int = len(args)
        module: str = self.commands[title]

        mod_path = module.split(".")
        mod: dict = self.modules
        for i in mod_path:
            mod = mod[i]

        command = mod[title]

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
