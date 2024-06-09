import os.path
import unittest

from src.gui.settings import Settings


class TestSettings(unittest.TestCase):

    filepath = "test_settings.ini"

    def setUp(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

        self.settings = Settings(self.filepath)

    def test_defaults(self):
        assert self.settings.file_data == self.settings.defaults

    def test_update_setting(self):
        self.settings.resolution = 600

        assert self.settings.resolution == 600
        assert self.settings.file_data["resolution"] == 600

    def tearDown(self):
        os.remove(self.filepath)
