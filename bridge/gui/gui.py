"""
UI module
"""


from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QLabel, QWidget, QMainWindow, QGridLayout, QHBoxLayout, QMenu, QToolBar, QPushButton, \
    QLineEdit, QDialog

from bridge.gui.settings import Settings
from bridge.scan.scan import Scanner


class MainWindow(QMainWindow):
    """
    Main GUI Window
    """

    def __init__(self):
        super().__init__()

        self._settings = Settings("settings.ini")

        self._continue_scanning = True
        self._current_popup = None

        self.setWindowTitle("Scanner SANE Bridge")
        self.setGeometry(100, 100, 600, 400)

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

        self._continue_scanning = True
        images = []
        while self._continue_scanning:
            
            skip_path = False
            if self.settings.get("skip_scan"):
                skip_path = "load.png"

            image = scanner.scan_image(resolution=resolution, debug=skip_path)

            # imageLabel = QLabel()
            # imageLabel.setPixmap(QPixmap().fromImage(ImageQt(image)))

            # self._maingrid.addItem(imageLabel, 0, 0)

            images.append(image)

            ask_continue_window = QDialog(self)
            self._current_popup = ask_continue_window
            ask_continue_window.setWindowTitle("Continue Scanning?")

            container = QGridLayout()

            continue_y = QPushButton("Yes")
            continue_n = QPushButton("No")
            contmessag = QLabel("Scan Additional Pages?:")

            container.addWidget(contmessag, 0, 0, 1, 2)
            container.addWidget(continue_n, 1, 0)
            container.addWidget(continue_y, 1, 1)

            continue_n.clicked.connect(self.set_continue_false)
            continue_y.clicked.connect(self.set_continue_true)

            ask_continue_window.setLayout(container)
            ask_continue_window.exec()

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

        print(f"Saving image out to {filename}")
        images[0].save(fp=filename, format="PDF", save_all=True, append_images=images[1:])

    def set_continue_true(self):
        self._continue_scanning = True
        self.close_current_popup()

    def set_continue_false(self):
        self._continue_scanning = False
        self.close_current_popup()
