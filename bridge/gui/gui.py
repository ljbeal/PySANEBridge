"""
UI module
"""


import os

from PIL import Image
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QLabel,
    QMainWindow,
    QGridLayout,
    QToolBar,
    QPushButton,
    QLineEdit, QFileDialog,
)
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

from bridge.gui.subcontainers.popup import Popup
from bridge.gui.settings import Settings
from bridge.gui.subcontainers.pageviewer import PageViewerWidget
from bridge.scan.scan import Scanner
from gui.subcontainers.confirmation_popup import ConfirmationWindow
from gui.subcontainers.question_window import QuestionWindow


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

        # load button
        self.loadbutton = QAction("Load", self)
        self.loadbutton.setStatusTip("Load a document from file")
        self.loadbutton.triggered.connect(self.load_image)

        toolBar.addAction(self.loadbutton)

        # save button
        self.savebutton = QAction("Save", self)
        self.savebutton.setStatusTip("Save the image")
        self.savebutton.triggered.connect(self.save_images)

        toolBar.addAction(self.savebutton)

        # clear button
        self.clearbutton = QAction("Clear", self)
        self.clearbutton.setStatusTip("Clears all pages from storage")
        self.clearbutton.triggered.connect(self.clear_images)

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

        scanner = Scanner(userhost)
        questionwindow = QuestionWindow(self, "Choose DPI", default=str(resolution))

        if not questionwindow.state:
            return
        else:
            dpi = questionwindow.value

            if dpi != "":
                dpi = int(dpi)
            else:
                dpi = resolution

        print(f"Scanning at {userhost} with dpi {dpi}")

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
            self.scanworker = ScanWorker(scanner, dpi)

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

        ask_filename = Popup(self, title="Choose save location")
        self._current_popup = ask_filename

        # just a filename for now
        name_label = QLabel("Filename")
        name_entry = QLineEdit()

        dpi_label = QLabel("Output DPI")
        dpi_entry = QLineEdit()
        dpi_entry.setPlaceholderText("100")

        ok_button = QPushButton("Save")
        ok_button.clicked.connect(self.close_current_popup)

        container = QGridLayout()
        container.addWidget(name_label, 0, 0)
        container.addWidget(dpi_label, 0, 1)
        container.addWidget(name_entry, 1, 0)
        container.addWidget(dpi_entry, 1, 1)
        container.addWidget(ok_button, 1, 2)

        ask_filename.setLayout(container)
        ask_filename.exec()

        filename = name_entry.text()
        if filename == "":
            return

        dpi_target = dpi_entry.text()
        if dpi_target == "":
            dpi_target = 100

        dpi_target = int(dpi_target)
        print(f"saving to file {filename}, with dpi {dpi_target}")

        filename = f"{os.path.splitext(filename)[0]}.pdf"  # force pdf

        self.save_to_file(filename, dpi_target)

    def clear_images(self):
        self._current_popup = ConfirmationWindow(self, "Clear Images")

        state = self._current_popup.state
        if state:
            self.image_widget.remove_all_images()

    def load_image(self):

        load = QFileDialog()
        load.DialogLabel("Choose File to Load")

        load.show()

        if load.exec():
            filenames = load.selectedFiles()

        print(f"loading files:\n{filenames}")

        for file in filenames:
            with Image.open(file) as imgfile:
                image = imgfile.copy().convert("RGB")
            self.scan_complete(image=image)

    def save_to_file(self, filename, dpi_target: int = 100):
        """
        Save the images out to filename

        Args:
            filename: target file, forced .pdf format
            dpi_target: target dpi to aim for
                100 dpi ~140KB per page
                200 dpi ~540KB per page
                300 dpi ~1.3MB per page
                400 dpi ~2.0MB per page
        """
        print(f"Saving image out to {filename}...", end=" ")

        scale = dpi_target / self.settings.get("resolution")
        print(f"Scaling image by {scale}")

        try:
            cache = []
            for image in self.image_widget.images:
                width = int(image.size[0] * scale)
                height = int(image.size[1] * scale)

                cache.append(image.resize((width, height)))

            cache[0].save(fp=filename, format="PDF", save_all=True,
                          append_images=cache[1:])
            print("Done.")
        except Exception as ex:
            print(f"Unhandled exception:\n{ex}")
            raise
