from pathlib import Path
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class VisualizeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(500, 300)

        # Scroll area setup
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Enable horizontal scrolling
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Hide vertical scrollbar

        # Container widget inside scroll area
        self.container = QWidget()
        self.image_layout = QHBoxLayout(self.container)
        self.image_layout.setSpacing(10)  # 10px gap between images
        self.image_layout.setContentsMargins(0, 0, 0, 0)  # No extra padding

        self.scroll_area.setWidget(self.container)

        # Main layout
        layout = QHBoxLayout()
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

        # Image list
        self.image_files = []
        self.image_labels = []
        self.img_height = 250  # Fixed height for consistency

    def visualize_data(self, folder_path):
        """Load .jpeg images from the specified folder."""
        path = Path(folder_path)
        self.image_files = sorted([f for f in path.iterdir() if f.suffix.lower() == ".jpeg"])

        if not self.image_files:
            self.clear_images()
            label = QLabel("No .jpeg images found in the folder.")
            label.setAlignment(Qt.AlignCenter)
            self.image_layout.addWidget(label)
        else:
            self.show_images()

    def clear_images(self):
        """Remove all images from the layout."""
        while self.image_layout.count():
            item = self.image_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.image_labels.clear()

    def show_images(self):
        """Display images in a horizontal row, maintaining aspect ratio."""
        self.clear_images()

        for image_file in self.image_files:
            pixmap = QPixmap(str(image_file))

            # Scale image to maintain aspect ratio while filling height
            scaled_pixmap = pixmap.scaledToHeight(self.img_height, Qt.SmoothTransformation)

            label = QLabel(self)
            label.setPixmap(scaled_pixmap)
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            label.setAlignment(Qt.AlignCenter)

            self.image_layout.addWidget(label)
            self.image_labels.append(label)

        # Ensure the container's minimum width is large enough to fit all images side by side
        total_width = sum(label.pixmap().width() for label in self.image_labels) + (10 * len(self.image_labels))
        self.container.setMinimumWidth(total_width)

