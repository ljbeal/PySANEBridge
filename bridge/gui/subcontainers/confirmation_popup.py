from bridge.gui.subcontainers.popup import Popup


class ConfirmationWindow(Popup):
    def __init__(self, parent, name: str | None):
        if name is None:
            title = "Confirm?"
        else:
            title = f"Confirm {name}?"

        super().__init__(parent, title=title)
