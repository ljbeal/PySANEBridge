"""
Module for a self healing settings file
"""
import re


class Settings:
    """
    Class for a settings file

    Settings are stored in the file as

    key: value

    and are updated with __setattr__ and __getattr__
    """

    __slots__ = ["_path", "_defaults"]

    def __init__(self, path: str = "settings.ini"):

        self._path = path

        self._defaults = {
            "userhost": "localhost",
            "resolution": 300
        }

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
            with open(self.file) as o:
                lines = o.readlines()
        except FileNotFoundError:
            lines = []

        for line in lines:
            key, val = line.split(":")

            val = val.lower().strip()

            try:
                if "." in val:
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
        with open(self.file, "w+") as o:
            for k, v in data.items():
                o.write(f"{k}: {v}\n")

    def __setattr__(self, key, value):
        if key in Settings.__slots__:
            object.__setattr__(self, key, value)
            return

        data = self.file_data
        data[key] = value

        self.dump_data(data)

    def __getattr__(self, item):
        if item in Settings.__slots__:
            return object.__getattribute__(self, item)

        return self.file_data[item]
