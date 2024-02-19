import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel)
from a import find_similar_images


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Matcher")

        # Create layout
        main_layout = QVBoxLayout()

        # Create horizontal layout for each input row
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
        # Get the text from input boxes
        search_path = self.input_search_path.text()
        image_path = self.input_image_path.text()
        if not search_path.ends_with("/"):
            search_path.append("/")
        similar_images = find_similar_images(search_path, image_path)

        for i in reversed(range(self.layout().count())):
            item = self.layout().itemAt(i)
            if isinstance(item, QLabel):
                item.widget().deleteLater()

        # Add labels for each similar image
        for img_file in similar_images:
            label = QLabel()
            label.setText(img_file)
            self.layout().addWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
