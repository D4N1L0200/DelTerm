"""Manage files."""

import json
from pathlib import Path
from typing import Any
import os


class JSON:
    """A class for managing JSON data."""

    def __init__(self, file_path: str) -> None:
        self._file_path: Path = Path(os.path.join(os.getcwd(), "src/modules/", file_path))
        if not os.path.exists(self._file_path):
            raise FileNotFoundError(f"File '{self._file_path}' not found.")
        self.d: dict[str, Any] = self.load()

    def load(self) -> dict[str, Any]:
        """Load data from a JSON file."""
        with self._file_path.open("r") as file:
            data = json.load(file)
        return data

    def save(self) -> None:
        """Save data to a JSON file."""
        with self._file_path.open("w") as file:
            json.dump(self.d, file, indent=2)
