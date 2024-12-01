from PyQt6.QtWidgets import QPushButton, QGridLayout

from bridge.gui.subcontainers.popup import Popup


class ConfirmationWindow(Popup):

    def __init__(self, parent, name: str | None):
        if name is None:
            title = "Confirm?"
        else:
            title = f"Confirm {name}?"

        super().__init__(parent, title=title)

        # just a filename for now

        self.state = None

        ok_button = QPushButton("Yes")
        ok_button.clicked.connect(self.yes)

        no_button = QPushButton("No")
        no_button.clicked.connect(self.no)

        container = QGridLayout()
        container.addWidget(ok_button, 0, 0)
        container.addWidget(no_button, 0, 1)

        self.setLayout(container)
        self.exec()

    def yes(self):
        self.state = True
        self.close()

    def no(self):
        self.state = False
        self.close()
