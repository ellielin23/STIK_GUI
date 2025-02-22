import os
import cv2
import time
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
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
    dataGenerated = pyqtSignal(np.ndarray, float)  # Signal to send experiment data
    finished = pyqtSignal()
    updateProgress = pyqtSignal(int, int)

    def __init__(self, dataset_path, config, output_path, parent=None):
        super().__init__()
        self.config = config
        self.dataset_path = dataset_path  # This is already instantiated
        self.running = True
        self.output_dir = Path(output_path + "/segmentations")

        # self.model = YOLO(os.path.abspath("stick_gui/best.pt"))
        # self.model = YOLO(os.path.abspath("best.pt"))
        self.model = None
        try:
            self.model = YOLO(os.path.abspath("best.pt"))
        except:
            self.model = YOLO(os.path.abspath("stick_gui/best.pt"))

    def run(self):
        if self.model is None:
            QMessageBox.critical(None, "Error", "No model exists.")
            return
        if self.dataset_path is None:
            QMessageBox.critical(None, "Error", "No valid Dataset selected.")
            return
        print(self.config)

        os.makedirs(self.output_dir, exist_ok=True)

        path = Path(self.dataset_path)
        image_files = sorted([f for f in path.iterdir() if f.suffix.lower() in [".jpeg", ".jpg"]])

        areas = []

        for image_file in image_files:
            if self.running:
                result = self.model.predict(source=image_file)
                if result[0].masks is not None:  # Ensure masks exist
                    masks = result[0].masks.data.cpu().numpy()  # Convert to numpy array (shape: [num_masks, H, W])

                    for mask in masks:
                        area = np.sum(mask > 0)  # Count nonzero pixels in mask
                        areas.append(area)

                    predicted_image = result[0].plot()
                    cv2.imwrite(os.path.join(self.output_dir, image_file.name), predicted_image)
                    self.dataGenerated.emit(predicted_image, area)
                    self.updateProgress.emit(len(areas), len(image_files))
                
        print("Segmentation Areas:", areas)

        self.finished.emit()
        print("finished process")

    def stop(self):
        print("Stopping process")
        self.running = False
        self.quit()