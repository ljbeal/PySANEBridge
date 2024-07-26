"""
UI module
"""


import os

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import (
    QLabel,
    QMainWindow,
    QGridLayout,
    QVBoxLayout,
    QToolBar,
    QPushButton,
    QLineEdit,
    QDialog,
    QScrollArea
)
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

from bridge.gui.settings import Settings
from bridge.gui.pageviewer import PageViewerWidget
from bridge.scan.scan import Scanner


class ScanWorker(QThread):
    finished = pyqtSignal()

    def __init__(self, scanner, resolution):
        super().__init__()
        print(f"scanner created with resolution {resolution}")
        self.scanner = scanner
        self.resolution = resolution

        self.image = None

    @pyqtSlot()
    def run(self):
        """request a scan"""
        print("scanning...")
        self.image = self.scanner.scan_image(self.resolution)
        self.finished.emit()


class MainWindow(QMainWindow):
    """
    Main GUI Window
    """

    def __init__(self):
        super().__init__()

        self._settings = Settings("settings.ini")

        self._current_popup = None

        self.setWindowTitle("Scanner SANE Bridge")
        self.setGeometry(100, 100, 600, 400)

        self.image_widget = PageViewerWidget()
        self.setCentralWidget(self.image_widget)

        self._waiting_for_scan = False

        self.UISetup()

        self.show()

    def close_current_popup(self):
        if self._current_popup is not None:
            self._current_popup.close()

    @property
    def settings(self):
        """Returns the internal Settings object"""
        return self._settings

    def UISetup(self):
        """Create the ui elements"""

        self._createToolBar()

        # self.showMaximized()

    def _createToolBar(self):

        toolBar = QToolBar()
        toolBar.setMovable(False)
        # scan button
        self.scanbutton = QAction("Scan", self)
        self.scanbutton.setStatusTip("Request a scan from the server")
        self.scanbutton.triggered.connect(self.perform_scan)

        toolBar.addAction(self.scanbutton)

        # save button
        self.savebutton = QAction("Save", self)
        self.savebutton.setStatusTip("Save the image")
        self.savebutton.triggered.connect(self.save_images)

        toolBar.addAction(self.savebutton)

        # clear button
        self.clearbutton = QAction("Clear", self)
        self.clearbutton.setStatusTip("Clears all pages from storage")
        self.clearbutton.triggered.connect(self.image_widget.remove_all_images)

        toolBar.addAction(self.clearbutton)

        resolutionLabel = QLabel(f"Resolution: {self.settings.get('resolution')} ")
        toolBar.addWidget(resolutionLabel)

        connectionLabel = QLabel(f"Connected: {self.settings.get('userhost')} ")
        toolBar.addWidget(connectionLabel)

        self.statuslabel = QLabel(f"Ready")
        toolBar.addWidget(self.statuslabel)

        self.addToolBar(toolBar)

    def save_setting(self, name, entry: QLineEdit):
        value = entry.text()
        self.settings.set(name, value)

    def perform_scan(self):
        userhost = self.settings.get("userhost")
        resolution = self.settings.get("resolution")

        print(f"Scanning at {userhost}")

        scanner = Scanner(userhost)

        skip_path = None
        skip = self.settings.get("skip_scan")
        if skip is not None and skip:
            import bridge
            skip_path = os.path.join(os.path.split(bridge.__file__)[0], "..", "tests", "load.png")

            print(f"skipping scan, loading {skip_path}")
            with Image.open(skip_path) as imgfile:
                image = imgfile.copy().convert("RGB")
            self.scan_complete(image=image)

        else:
            print("creating connection to scanner")
            self.scanworker = ScanWorker(scanner, resolution)

            self.scanworker.finished.connect(self.scan_complete)
            self.scanworker.start()
            self.waiting_for_scan = True

    @property
    def waiting_for_scan(self):
        return self._waiting_for_scan

    @waiting_for_scan.setter
    def waiting_for_scan(self, wait: bool):
        self.scanbutton.setEnabled(not wait)
        self.clearbutton.setEnabled(not wait)
        self.savebutton.setEnabled(not wait)

        if wait:
            self.statuslabel.setText("Scanning...")
        else:
            self.statuslabel.setText("Ready")

    def scan_complete(self, image=None):
        print("scan complete")
        self.waiting_for_scan = False

        if image is None:
            print("retrieving image")
            image = self.scanworker.image

        print("adding image to canvas")
        self.image_widget.add_image(image)

    def save_images(self):

        ask_filename = QDialog(self)
        self._current_popup = ask_filename
        ask_filename.setWindowTitle("Choose where to save the file")

        # just a filename for now
        name_entry = QLineEdit()
        ok_button = QPushButton("Save")
        ok_button.clicked.connect(self.close_current_popup)

        container = QGridLayout()
        container.addWidget(name_entry, 0, 0)
        container.addWidget(ok_button, 0, 1)

        ask_filename.setLayout(container)
        ask_filename.exec()

        filename = name_entry.text()
        if filename == "": 
            return

        filename = f"{os.path.splitext(filename)[0]}.pdf"  # force pdf

        print(f"Saving image out to {filename}...", end = " ")
        try:
            self.image_widget.images[0].save(fp=filename, format="PDF", save_all=True,
                                             append_images=self.image_widget.images[1:])
            print("Done.")
        except Exception as ex:
            print(f"Unhandled exception:\n{ex}")
            raise

        self.image_widget.remove_all_images()
