from pathlib import Path
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class VisualizeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(500, 300)  # Set a reasonable size for embedding

        self.image_label = QLabel(self)  # Label to display the image
        self.image_label.setAlignment(Qt.AlignCenter)

        # Navigation buttons
        self.prev_button = QPushButton("Previous", self)
        self.next_button = QPushButton("Next", self)

        # Layout setup
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Image list and index
        self.image_files = []
        self.current_index = 0

        # Button signals
        self.prev_button.clicked.connect(self.show_previous_image)
        self.next_button.clicked.connect(self.show_next_image)

        # Initially disable buttons until images are loaded
        self.prev_button.setDisabled(True)
        self.next_button.setDisabled(True)

    def visualize_data(self, folder_path):
        """Load .jpeg images from the specified folder."""
        path = Path(folder_path)
        self.image_files = sorted([f for f in path.iterdir() if f.suffix.lower() == ".jpeg"])

        if not self.image_files:
            self.image_label.setText("No .jpeg images found in the folder.")
            self.prev_button.setDisabled(True)
            self.next_button.setDisabled(True)
        else:
            self.current_index = 0
            self.show_image()
            self.prev_button.setDisabled(False)
            self.next_button.setDisabled(False)

    def show_image(self):
        """Display the current image."""
        if self.image_files:
            pixmap = QPixmap(str(self.image_files[self.current_index]))
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            # Enable/disable buttons based on index
            self.prev_button.setDisabled(self.current_index == 0)
            self.next_button.setDisabled(self.current_index == len(self.image_files) - 1)

    def show_previous_image(self):
        """Go to the previous image."""
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()

    def show_next_image(self):
        """Go to the next image."""
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.show_image()
