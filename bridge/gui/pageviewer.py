import os
import sys

import PIL.Image
from PIL.ImageQt import ImageQt
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QMainWindow, QPushButton, QFileDialog, \
    QApplication, QHBoxLayout


class PageViewerWidget(QWidget):
    """
    Display widget for pages

    Modified from ChatGPT 4o output
    """
    def __init__(self):
        super().__init__()
        self.images = []

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        self.update_display()

    def update_display(self):
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        for idx, image in enumerate(self.images):
            image_widget = QWidget()
            image_layout = QHBoxLayout()

            label = QLabel()
            pixmap = QPixmap().fromImage(ImageQt(image))
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            image_layout.addWidget(label)

            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda _, i=idx: self.remove_image(i))
            image_layout.addWidget(remove_button)

            image_widget.setLayout(image_layout)
            self.scroll_layout.addWidget(image_widget)

    def add_image(self, image_path):
        self.images.append(image_path)
        self.update_display()

    def remove_image(self, index):
        if 0 <= index < len(self.images):
            del self.images[index]
            self.update_display()

    def remove_all_images(self):
        self.images = []
        self.update_display()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.image_widget = PageViewerWidget()
        self.setCentralWidget(self.image_widget)

        self.init_ui()

    def init_ui(self):
        self.toolbar = self.addToolBar("Main Toolbar")
        self.add_image_button = QPushButton("Add Image")
        self.add_image_button.clicked.connect(self.add_image)
        self.toolbar.addWidget(self.add_image_button)

    def add_image(self):
        import bridge
        file_path = os.path.join(os.path.split(bridge.__file__)[0], "..", "tests", "load.png")

        image = PIL.Image.open(file_path)

        if file_path:
            self.image_widget.add_image(image)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
