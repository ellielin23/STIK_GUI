from PyQt5.QtWidgets import QHBoxLayout, QWidget
from PyQt5.QtGui import QFont
import pyqtgraph as pg
import numpy as np

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(500, 150)

        # Create two PyQtGraph PlotWidgets
        self.plot_widget1 = pg.PlotWidget()
        self.plot_widget2 = pg.PlotWidget()

        # Set background to white
        self.plot_widget1.setBackground("w")
        self.plot_widget2.setBackground("w")

        # Configure axis labels
        self.plot_widget1.setLabel("left", "Tumor Area")
        self.plot_widget1.setLabel("bottom", "Time")
        self.plot_widget1.addLegend()

        self.plot_widget2.setLabel("left", "Invasion Speed")
        self.plot_widget2.setLabel("bottom", "Time")
        self.plot_widget2.addLegend()

        # Reduce padding around axis labels
        for plot in [self.plot_widget1, self.plot_widget2]:
            plot_item = plot.getPlotItem()
            plot_item.layout.setContentsMargins(5, 5, 5, 5)  # Small margins
            plot_item.getAxis('left').setWidth(30)  # Reduce left axis padding
            plot_item.getAxis('bottom').setHeight(25)  # Reduce bottom axis padding
            plot_item.getViewBox().setDefaultPadding(0.1)  # Add spacing from plot data to border

            # Set axis label font size
            axis_style = {'tickFont': QFont('Arial', 6)}
            plot_item.getAxis('left').setStyle(**axis_style)
            plot_item.getAxis('bottom').setStyle(**axis_style)

        # Layout to hold the two plot widgets side by side
        layout = QHBoxLayout()
        layout.addWidget(self.plot_widget1)
        layout.addWidget(self.plot_widget2)
        self.setLayout(layout)
    
        self.areas = []
        
    def collect(self, area):
        self.areas.append(area)

    def plot(self):
        """Plots area vs time on plot_widget1 and the derivative of area vs time on plot_widget2"""
        self.plot_widget1.clear()
        self.plot_widget2.clear()

        # Time is just the index of areas
        time = np.arange(len(self.areas))

        # Plot area vs time
        self.plot_widget1.plot(time, self.areas, pen=pg.mkPen("b", width=2), name="Area vs Time")
        for i, a in enumerate(self.areas):
            self.plot_widget1.plot([i], [a], pen=None, symbol='o', symbolBrush='g', symbolSize=10)

        # Auto scale the plot to fit the data
        self.plot_widget1.autoRange()

        # Calculate the derivative (change in area with respect to time)
        area_derivative = np.diff(self.areas)

        # Time for the derivative plot is shorter by one step because diff reduces the size by 1
        time_derivative = time[:-1]  # Align time with the derivative data

        # Plot derivative on plot_widget2
        self.plot_widget2.plot(time_derivative, area_derivative, pen=pg.mkPen("r", width=2), name="d(area)/dt")
        for i, d in enumerate(area_derivative):
            self.plot_widget2.plot([i], [d], pen=None, symbol='o', symbolBrush='r', symbolSize=10)

        # Auto scale the plot to fit the data
        self.plot_widget2.autoRange()
