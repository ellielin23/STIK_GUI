from PyQt5.QtWidgets import QVBoxLayout, QWidget
import pyqtgraph as pg
import numpy as np

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(500, 200)

        # Create a PyQtGraph PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("w")  # Set background to white

        # Configure axis labels
        self.plot_widget.setLabel("left", "Y-axis")
        self.plot_widget.setLabel("bottom", "X-axis")
        self.plot_widget.addLegend()

        # Layout to hold the PyQtGraph widget
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def plot(self):
        """Plots a random straight line using PyQtGraph"""
        self.plot_widget.clear()  # Clear previous plots

        # Generate random slope and intercept
        m = np.random.uniform(-5, 5)  # Random slope
        b = np.random.uniform(-10, 10)  # Random intercept

        # Generate x values and corresponding y values for a straight line
        x = np.linspace(-10, 10, 100)  # X values from -10 to 10
        y = m * x + b  # Linear equation: y = mx + b

        # Plot the line with PyQtGraph
        self.plot_widget.plot(x, y, pen=pg.mkPen("b", width=2), name=f"y = {m:.2f}x + {b:.2f}")

