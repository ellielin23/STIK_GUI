import time
from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path

from PyQt5.QtWidgets import (
    QMessageBox,
)

class ProcessWorker(QThread):
    """
    This class is used to process the images, used on a separate QThread than the main loop.
    Communicates through signals to be thread-safe
    """
    dataGenerated = pyqtSignal(Path)  # Signal to send experiment data
    finished = pyqtSignal()

    def __init__(self, dataset_path, config, parent=None):
        super().__init__()
        self.config = config
        self.dataset_path = dataset_path  # This is already instantiated
        self.running = True

    def run(self):
        if self.dataset_path is None:
            QMessageBox.critical(None, "Error", "No valid Dataset selected.")
            return

        print(self.config)

        if self.running:
            self.dataGenerated.emit(self.dataset_path)
            self.finished.emit()
            print("finished process")

    def stop(self):
        print("Stopping process")
        self.running = False
        self.quit()