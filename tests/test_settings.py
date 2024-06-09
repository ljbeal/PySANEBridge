"""
Test the settings module
"""

import os.path
import unittest

from src.gui.settings import Settings


class TestSettings(unittest.TestCase):
    """Test case for Settings"""

    filepath = "test_settings.ini"

    def setUp(self):
        """Set up testing"""
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

        self.settings = Settings(self.filepath)

    def test_defaults(self):
        """Check that the defaults line up"""
        assert self.settings.file_data == self.settings.defaults

    def test_update_setting(self):
        """Update a setting and ensure it sticks"""
        self.settings.set("resolution", 600)

        assert self.settings.get('resolution') == 600
        assert self.settings.file_data["resolution"] == 600

    def tearDown(self):
        """Tear down test structures"""
        os.remove(self.filepath)
