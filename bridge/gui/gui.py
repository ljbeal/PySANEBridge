"""
UI module
"""

import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QHBoxLayout, QMenu, QToolBar, QPushButton, \
    QLineEdit

from bridge.gui.settings import Settings
from bridge.scan.scan import Scanner


class MainWindow(QMainWindow):
    """
    Main GUI Window
    """

    def __init__(self):
        super().__init__()

        self._settings = Settings("settings.ini")

        self.setWindowTitle("Scanner SANE Bridge")
        self.setGeometry(100, 100, 600, 400)

        self.UISetup()

        self.show()

    @property
    def settings(self):
        """Returns the internal Settings object"""
        return self._settings

    def UISetup(self):
        """Create the ui elements"""

        self._createToolBar()

        # self.showMaximized()

    def _createToolBar(self):
        scanbutton = QAction("Scan", self)
        scanbutton.setStatusTip("Request a scan from the server")
        scanbutton.triggered.connect(self.perform_scan)

        toolBar = QToolBar()
        toolBar.setMovable(False)

        toolBar.addAction(scanbutton)

        resolutionLabel = QLabel(f"Resolution: {self.settings.get('resolution')} ")
        toolBar.addWidget(resolutionLabel)

        connectionLabel = QLabel(f"Connected: {self.settings.get('userhost')} ")
        toolBar.addWidget(connectionLabel)

        self.addToolBar(toolBar)

    def save_setting(self, name, entry: QLineEdit):
        value = entry.text()
        self.settings.set(name, value)

    def perform_scan(self):
        userhost = self.settings.get("userhost")
        resolution = self.settings.get("resolution")

        print(f"Scanning at {userhost}")

        scanner = Scanner(userhost)

        continue_scanning = True
        images = []
        while continue_scanning:
            image = scanner.scan_image(resolution=resolution)

            images.append(image)

            continue_scanning = False  # popup dialog for continue

        filename = "test.pdf"

        images[0].save(fp=filename, format="PDF", save_all=True, append_images=images[1:])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())
