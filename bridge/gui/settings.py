"""
Module for a self healing settings file
"""

import os
from typing import Any


class Settings:
    """
    Class for a settings file

    Settings are stored in the file as

    key: value

    and are updated with __setattr__ and __getattr__
    """

    __slots__ = ["_path", "_defaults"]

    def __init__(self, path: str = "settings.ini"):

        self._path = os.path.abspath(path)

        self._defaults = {"userhost": "localhost", "resolution": 300}

        print(f"using settings file at {self.file}")
        current_data = self.file_data
        for k, v in self.defaults.items():
            if k not in current_data:
                current_data[k] = v

        self.dump_data(current_data)

    @property
    def file(self) -> str:
        """Returns file name"""
        return self._path

    @property
    def defaults(self):
        """Returns the stored defaults"""
        return self._defaults

    @property
    def file_data(self) -> dict:
        """Return the file content as a dictionary"""
        data = {}
        try:
            with open(self.file, encoding="UTF-8") as o:
                lines = o.readlines()
        except FileNotFoundError:
            lines = []

        for line in lines:
            key, val = line.split(":")

            val = val.lower().strip()

            try:
                if val.lower() == "true":
                    val = True
                elif val.lower() == "false":
                    val = False
                elif "." in val:
                    val = float(val)
                else:
                    val = int(val)
            except (ValueError, TypeError):
                pass

            data[key.lower().strip()] = val

        return data

    def key_in_data(self, key: str) -> bool:
        """Returns True if the key exists in the file data"""
        return key in self.file_data

    def dump_data(self, data: dict):
        """Dump data to file"""
        with open(self.file, "w+", encoding="UTF-8") as o:
            for k, v in data.items():
                o.write(f"{k}: {v}\n")

    def set(self, key: str, value: Any):
        """
        Set a value

        Args:
            key: key to set
            value: value to set
        """
        data = self.file_data
        data[key] = value

        self.dump_data(data)

    def get(self, item: str) -> Any:
        """
        Get a setting

        Arg:
            item: item to fetch
        """
        return self.file_data.get(item, None)
