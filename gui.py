import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel)
from utils import find_similar_images
import os


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Matcher")
        self.setFixedWidth(1080)

        # Create layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        row1_layout = QHBoxLayout()
        row2_layout = QHBoxLayout()
        # Create labels
        label_search_path = QLabel("Search Path:")
        label_image_path = QLabel("Image Path:")

        # Create input boxes
        self.input_search_path = QLineEdit()
        self.input_image_path = QLineEdit()

        # Add labels and input boxes to rows
        row1_layout.addWidget(label_search_path)
        row1_layout.addWidget(self.input_search_path)
        row2_layout.addWidget(label_image_path)
        row2_layout.addWidget(self.input_image_path)

        # Add rows to main layout
        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)

        # Create submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.on_submit_clicked)

        # Add button to main layout
        main_layout.addWidget(submit_button)

        # Set the main layout for the window
        self.setLayout(main_layout)

    def on_submit_clicked(self):
        for label in self.findChildren(QLabel):
            if label.text() not in ["Search Path:", "Image Path:"]:
                label.deleteLater()

        search_path = self.input_search_path.text()
        image_path = self.input_image_path.text()

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
                for img_file in similar_images:
                    label = QLabel()
                    label.setText(img_file)
                    self.layout().addWidget(label)

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
