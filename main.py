###########################################################################
################################# IMPORTS #################################
###########################################################################

# conda create --name STIK_GUI python=3.12
# conda activate STIK_GUI
# conda install --file requirements.txt
# make sure you install pyqt and matplotlib
# conda deactivate

import sys, os, inspect
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSplitter,
    QMessageBox,
    QFileDialog
)
from PyQt5.QtCore import Qt, QSize

from ProcessorThread import ProcessWorker
from Visualizer import VisualizeWidget
from ConfigEdit import QDictEdit
from init.initialize import BaseConfig

path = os.getcwd()
try:
    os.add_dll_directory(os.path.dirname(path) + '\\PythonDrivers')
except AttributeError:
    os.environ["PATH"] = os.path.dirname(path) + '\\PythonDrivers' + ";" + os.environ["PATH"]

###########################################################################
############################### MAIN WINDOW ###############################
###########################################################################
class GUI(QMainWindow):
    """
    This class represents the main application window of the GUI.
    """

    def __init__(self):
        """ Initializer with experiment and data processor threads. """
        super().__init__()

        ### Threads ###
        self.processor_worker = None  # Experiment Run Worker thread

        self.dataset_path = None
        self.dataset_name = "None"

        self.init_ui()

    def init_ui(self):
        """ Set up the UI Layout """
        ### Central Widget ###
        self.setWindowTitle("Spheriod Tumor Invasion Kinetics")
        self.resize(800, 500) # finicky between mac and windows
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        ### Start Process Button ###
        self.start_process_button = QPushButton("Process", self)
        self.start_process_button.clicked.connect(self.toggle_process)

        ### Plot Widget ###
        self.visualizeWidget = VisualizeWidget(parent=self)

        ### Progres Bar ###
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setMaximumSize(QSize(400, 40))

        ### Load Data, Load Experiment, and Load Config button ###
        load_dataset_button = QPushButton("Load Dataset", self)
        load_dataset_button.setObjectName("load_dataset_button")
        load_dataset_button.clicked.connect(self.load_dataset_folder)

        ### Experiment Name ###
        self.dataset_status_label = QLabel(self)
        self.dataset_status_label.setText('<html><b>Unprocessed</b></html>')

        ### Config Dictionary ###
        # create the dictionary editor
        self.configUpdate = {"Dataset Config": {
            "Time Interval": 0,
            "Scale": 0,
        }, "Base Config": BaseConfig}
        self.configEdit = QDictEdit(self.configUpdate)
        self.configEdit.resize(500, 500)

        ### Adding all Components ###
        layout = QVBoxLayout()
        topButtonsLayout = QHBoxLayout()
        topButtonsLayout.addWidget(self.start_process_button)
        topButtonsLayout.addWidget(self.dataset_status_label)
        topButtonsLayout.addWidget(self.progress_bar)
        topButtonsLayout.addWidget(load_dataset_button)

        ### Add splitter between plot and dict ###
        layout_plot = QHBoxLayout()
        plotSplitter = QSplitter()
        plotSplitter.addWidget(self.visualizeWidget)
        plotSplitter.addWidget(self.configEdit)
        plotSplitter.setStretchFactor(0, 5)
        plotSplitter.setStretchFactor(1, 1)

        layout_plot.addWidget(plotSplitter)
        layout.addLayout(topButtonsLayout)
        layout.addLayout(layout_plot)

        self.centralWidget.setLayout(layout)

    def toggle_process(self):
        """ Start or stop the experiment. """
        if self.processor_worker and self.processor_worker.isRunning():
            self.stop_process()
        else:
            self.start_process()

    def load_dataset_folder(self):
        """ Load a dataset folder that contains ONLY .jpeg files """
        options = QFileDialog.Options()
        folder = QFileDialog.getExistingDirectory(self, "Select Dataset Folder", "..\\", options=options)

        if not folder:
            return

        path = Path(folder)
        all_files = list(path.iterdir())  # Get all files in the folder
        jpeg_files = [f for f in all_files if f.suffix.lower() == ".jpeg"]  # Filter for .jpeg files
        # Get total size (only for .jpeg files)
        dataset_size = self.format_size(sum(f.stat().st_size for f in jpeg_files))

        if not jpeg_files:
            QMessageBox.warning(self, "Invalid Folder", "The selected folder does not contain any .jpeg files.")
            return
        if len(jpeg_files) != len(all_files):  # Ensure all files are .jpeg
            QMessageBox.warning(self, "Invalid Folder", "The selected folder contains non-.jpeg files.")
            return

        print(path)
        self.dataset_path = path
        self.dataset_name = path.name  # Use the folder name as the dataset name
        self.visualizeWidget.visualize_data(self.dataset_path)
        self.configEdit.update_basic_configs(self.dataset_name, dataset_size, len(all_files))

    def start_process(self):
        """ Start the experiment (experiment and data worker). """
        if self.dataset_path is None:
            QMessageBox.critical(None, "Error", "No Dataset Loaded.")
            return
        self.start_process_button.setText("Stop Process")

        ### Handle Updating the Config ###
        UpdateConfig = self.configEdit.config["Dataset Config"]
        BaseConfig = self.configEdit.config["Base Config"]
        self.config = BaseConfig | UpdateConfig

        ### Create Threads and Connections ###
        self.processor_worker = ProcessWorker(self.dataset_path, self.config)
        # Connect processor -> visualizer
        self.processor_worker.dataGenerated.connect(self.visualizeWidget.visualize_data)
        # Connect processor finished -> finish_process
        self.processor_worker.finished.connect(self.finish_process)
        self.processor_worker.start() # begin process

    def stop_process(self):
        """ Stop an Experiment and all threads."""
        if self.processor_worker:
            self.processor_worker.stop()
            self.processor_worker.wait() # allows for "graceful" termination before continuing
            self.processor_worker = None

        self.start_process_button.setText("Process")

    def finish_process(self):
        self.dataset_status_label.setText('<html><b>Processed</b></html>')
        self.stop_process()

    def closeEvent(self, event):
        """ Ensure all threads stop before closing. """
        self.stop_process()
        event.accept()

    def format_size(self, size_in_bytes):
        """ Formats size in bytes to a human readable format"""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024
        return f"{size_in_bytes:.2f} PB"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    ex.show()
    sys.exit(app.exec_())
