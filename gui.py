import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt
from utils import find_similar_images
import os
from PyQt5.QtGui import QPixmap, QPainter


class FileDragDropLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            self.setText(path)


class ImageWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.setFixedSize(200, 200)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.image_path)
        painter.drawPixmap(self.rect(), pixmap)


class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Matcher")

        # Create layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create widget to contain the scrollable content
        scroll_content = QWidget()
        scroll_content.setLayout(self.main_layout)
        scroll_content.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding
        )
        scroll_area.setWidget(scroll_content)

        # Add scroll area to the main layout
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)

        # Create file upload button
        self.file_upload_button = FileDragDropLineEdit()
        self.main_layout.addWidget(self.file_upload_button)

        # Create submit button
        submit_button = QPushButton("Upload File")
        submit_button.clicked.connect(self.on_submit_clicked)
        self.main_layout.addWidget(submit_button)

    def on_submit_clicked(self):
        for i in range(2, self.main_layout.count()):
            self.main_layout.itemAt(i).widget().deleteLater()

        for label in self.findChildren(QLabel):
            if label.text() not in ["Search Path:", "Image Path:"]:
                label.deleteLater()

        search_path = os.getcwd()
        image_path = self.file_upload_button.text()

        if image_path.endswith("/"):
            if image_path.split("/")[-2].endswith(".jpg"):
                image_path = image_path[:-1]
            else:
                label = QLabel()
                label.setText("Image Path is wrong.")
                self.layout().addWidget(label)
                return

        if not image_path.endswith("/") and not image_path.endswith(".jpg"):
            label = QLabel()
            label.setText("Image Path is wrong.")
            self.layout().addWidget(label)
            return

        if not search_path.endswith("/"):
            search_path = search_path + "/"

        for label in self.layout().findChildren(QLabel):
            label.deleteLater()

        if os.path.exists(image_path) and os.path.exists(search_path):
            # remove all QLabel

            try:
                similar_images = find_similar_images(search_path, image_path)

                if len(similar_images) == 0:
                    label = QLabel()
                    label.setText(f"Not found any matching image at {search_path}")
                    self.layout().addWidget(label)

                # Add labels for each similar image
                for image_data in similar_images:
                    img_file = image_data[0]
                    similarity_percentage = image_data[1]
                    image = ImageWidget(img_file)
                    label = QLabel()
                    label.setText(img_file)
                    percentage_label = QLabel()
                    percentage_label.setText(str(similarity_percentage))
                    self.main_layout.addWidget(image)
                    self.main_layout.addWidget(label)
                    self.main_layout.addWidget(percentage_label)

            except Exception as error:
                label = QLabel()
                label.setText(f"Error: {error}")
                self.layout().addWidget(label)

        else:
            label = QLabel()
            label.setText("Image Path or Search Path is wrong.")
            self.layout().addWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
