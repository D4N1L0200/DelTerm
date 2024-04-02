import json
from pathlib import Path
from typing import Any, Dict


class JSONObj:
    def __init__(self, file_path: str | Path) -> None:
        self._file_path: Path = Path(file_path)
        self._data: Dict[str, Any] = self._load_data()
        self._add_attributes()

    def _load_data(self) -> Dict[str, Any]:
        try:
            with self._file_path.open("r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: File not found at {self._file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Unable to decode JSON from {self._file_path}")
            return {}

    def _add_attributes(self) -> None:
        for key, value in self._data.items():
            setattr(self, key, value)

    def _save_data(self) -> None:
        try:
            with self._file_path.open("w") as file:
                json.dump(self._data, file, indent=2)
        except Exception as e:
            print(f"Error: Unable to save data to {self._file_path}. {e}")

    def __setattr__(self, key: str, value: Any):
        super().__setattr__(key, value)
        if not key.startswith("_"):
            self._data[key] = value
            self._save_data()


class Data(JSONObj):
    def __init__(self, data_path: str, file: str):
        super().__init__(Path(data_path) / file)
