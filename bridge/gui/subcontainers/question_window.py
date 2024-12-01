from PyQt6.QtWidgets import QPushButton, QGridLayout, QLabel, QLineEdit

from bridge.gui.subcontainers.popup import Popup


class QuestionWindow(Popup):

    def __init__(self, parent, title: str | None, default: str | None = None):
        super().__init__(parent, title=title)

        self.state = None
        self.value = None
        self.default = default

        userinput_label = QLabel("Filename")
        self.userinput_input = QLineEdit()

        if default is not None:
            self.userinput_input.setPlaceholderText(default)

        ok_button = QPushButton("Accept")
        ok_button.clicked.connect(self.yes)

        no_button = QPushButton("Cancel")
        no_button.clicked.connect(self.no)

        container = QGridLayout()
        container.addWidget(userinput_label, 0, 0)
        container.addWidget(self.userinput_input, 0, 0)
        container.addWidget(ok_button, 1, 0)
        container.addWidget(no_button, 1, 1)

        self.setLayout(container)
        self.exec()

    def yes(self):
        self.close()
        self.state = True
        self.value = self.userinput_input.text()

    def no(self):
        self.close()
        self.state = False
        self.value = self.userinput_input.text()
