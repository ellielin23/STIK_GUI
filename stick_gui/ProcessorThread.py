import time
from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path
from ultralytics import YOLO
import shutil
import numpy as np

from PyQt5.QtWidgets import (
    QMessageBox,
)

class ProcessWorker(QThread):
    """
    This class is used to process the images, used on a separate QThread than the main loop.
    Communicates through signals to be thread-safe
    """
    dataGenerated = pyqtSignal(Path, np.ndarray)  # Signal to send experiment data
    finished = pyqtSignal()

    def __init__(self, dataset_path, config, parent=None):
        super().__init__()
        self.config = config
        self.dataset_path = dataset_path  # This is already instantiated
        self.running = True
        self.model = YOLO("best.pt")
        self.output_dir = "./output"

    def run(self):
        if self.dataset_path is None:
            QMessageBox.critical(None, "Error", "No valid Dataset selected.")
            return
        print(self.config)

        if self.running:
            shutil.rmtree(self.output_dir)

            results = self.model.predict(source=self.dataset_path, project=self.output_dir, save=True)
            areas = []

            # Iterate through the results
            for result in results:
                if result.masks is not None:  # Ensure masks exist
                    masks = result.masks.data.cpu().numpy()  # Convert to numpy array (shape: [num_masks, H, W])

                    for mask in masks:
                        area = np.sum(mask > 0)  # Count nonzero pixels in mask
                        areas.append(area)

            print("Segmentation Areas:", areas)

            self.dataGenerated.emit(Path(self.output_dir + "/predict"), np.array(areas))
            self.finished.emit()
            print("finished process")

    def stop(self):
        print("Stopping process")
        self.running = False
        self.quit()