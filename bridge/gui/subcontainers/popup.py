"""
Subclass for a popup dialog box
"""
from PyQt6.QtWidgets import QDialog


class Popup(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
