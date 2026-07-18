"""
JSON Storage Module

Purpose
-------
Provides low-level JSON file persistence.

Responsibilities
----------------
- Manage a JSON file path.
- Save JSON-compatible data.
- Load JSON-compatible data.
- Create parent directories when required.

Does Not
--------
- Know about Employee objects.
- Know about Department objects.
- Know about Company objects.
- Apply HR business rules.
- Convert domain objects into dictionaries.
"""

# ============================================================
# Standard Library Imports
# ============================================================

import json
from pathlib import Path
from typing import Any


class JsonStorage:
    """
    Provides low-level persistence for JSON-compatible data.

    JsonStorage reads and writes ordinary Python data structures
    without knowing anything about the application's domain models.
    """

    def __init__(self, file_path: str | Path):
        self._file_path = Path(file_path)

    @property
    def file_path(self) -> Path:
        """
        Returns the storage file path.

        The storage path is read-only and cannot be modified
        after the JsonStorage object has been created.

        Returns:
            Path:
                The path used for JSON persistence.
        """
        return self._file_path
    
    
    def save(self, data: dict | list) -> None:
        """
        Saves company data to JSON file.

        Args:
            data:
                JSON-compatible data to save.
        Raises:
            ValueError:
                If there is no data to save.
        """
        if data is None:
            raise ValueError("Nothing to save")
        
        self.file_path.parent.mkdir(parents=True,exist_ok=True,)
        with self.file_path.open("w", encoding="utf-8",) as json_file:
            json.dump(data,json_file,indent=4,ensure_ascii=False,)

        return None
    
    def load(self) -> dict | list:
        """
            Loads data from the JSON file.

        Returns:
            dict | list:
                The Python data loaded from the JSON file.

        Raises:
            FileNotFoundError:
                If the JSON file does not exist.
        """

        if not self.file_path.is_file():
            raise FileNotFoundError(
                f"JSON file '{self.file_path}' does not exist."
            )

        with self.file_path.open("r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        return data