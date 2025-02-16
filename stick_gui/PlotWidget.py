from PyQt5.QtWidgets import QHBoxLayout, QWidget
import pyqtgraph as pg
import numpy as np

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(500, 200)

        # Create two PyQtGraph PlotWidgets
        self.plot_widget1 = pg.PlotWidget()
        self.plot_widget2 = pg.PlotWidget()

        # Set background to white
        self.plot_widget1.setBackground("w")
        self.plot_widget2.setBackground("w")

        # Reduce padding around axis labels
        for plot in [self.plot_widget1, self.plot_widget2]:
            plot.getPlotItem().layout.setContentsMargins(5, 5, 5, 5)  # Small margins
            plot.getPlotItem().getAxis('left').setWidth(40)  # Reduce left axis padding
            plot.getPlotItem().getAxis('bottom').setHeight(30)  # Reduce bottom axis padding
            plot.getPlotItem().getViewBox().setDefaultPadding(0.05)  # Add spacing from plot data to border

            plot.getPlotItem().getAxis('left').setStyle(tickLength=-1)  # Tick length reduced
            plot.getPlotItem().getAxis('bottom').setStyle(tickLength=-1)

        # Configure axis labels
        self.plot_widget1.setLabel("left", "Tumor Area")
        self.plot_widget1.setLabel("bottom", "Time")
        self.plot_widget1.addLegend()

        self.plot_widget2.setLabel("left", "Invasion Speed")
        self.plot_widget2.setLabel("bottom", "Time")
        self.plot_widget2.addLegend()

        # Layout to hold the two plot widgets side by side
        layout = QHBoxLayout()
        layout.addWidget(self.plot_widget1)
        layout.addWidget(self.plot_widget2)
        self.setLayout(layout)

    def plot(self):
        """Plots two different random straight lines using PyQtGraph"""
        self.plot_widget1.clear()
        self.plot_widget2.clear()

        # Generate x values
        x = np.linspace(-10, 10, 100)

        # First plot
        m1, b1 = np.random.uniform(-5, 5), np.random.uniform(-10, 10)
        y1 = m1 * x + b1
        self.plot_widget1.plot(x, y1, pen=pg.mkPen("b", width=2), name=f"y = {m1:.2f}x + {b1:.2f}")

        # Second plot
        m2, b2 = np.random.uniform(-5, 5), np.random.uniform(-10, 10)
        y2 = m2 * x + b2
        self.plot_widget2.plot(x, y2, pen=pg.mkPen("r", width=2), name=f"y = {m2:.2f}x + {b2:.2f}")
