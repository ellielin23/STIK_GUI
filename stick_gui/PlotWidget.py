from PyQt5.QtWidgets import QHBoxLayout, QWidget
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

        # Reduce padding around axis labels
        # for plot in [self.plot_widget1, self.plot_widget2]:
        #     plot.getPlotItem().layout.setContentsMargins(5, 5, 5, 5)  # Small margins
        #     plot.getPlotItem().getAxis('left').setWidth(40)  # Reduce left axis padding
        #     plot.getPlotItem().getAxis('bottom').setHeight(30)  # Reduce bottom axis padding
        #     plot.getPlotItem().getViewBox().setDefaultPadding(0.05)  # Add spacing from plot data to border
        #
        #     plot.getPlotItem().getAxis('left').setStyle(tickLength=-1)  # Tick length reduced
        #     plot.getPlotItem().getAxis('bottom').setStyle(tickLength=-1)

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

    def plot(self, areas):
        """Plots area vs time on plot_widget1 and the derivative of area vs time on plot_widget2"""
        self.plot_widget1.clear()
        self.plot_widget2.clear()

        # Time is just the index of areas
        time = np.arange(len(areas))

        # Plot area vs time
        self.plot_widget1.plot(time, areas, pen=pg.mkPen("b", width=2), name="Area vs Time")
        for i, a in enumerate(areas):
            self.plot_widget1.plot([i], [a], pen=None, symbol='o', symbolBrush='g', symbolSize=10)

        # Calculate the line of best fit for area vs time
        slope_area, intercept_area = np.polyfit(time, areas, 1)  # 1 is for linear fit
        best_fit_line_area = slope_area * time + intercept_area
        self.plot_widget1.plot(time, best_fit_line_area, pen=pg.mkPen("y", width=2), name="Best Fit Line")

        # Display the best fit equation as a label on the plot
        best_fit_eq_area = f"y = {slope_area:.2f}x + {intercept_area:.2f}"
        self.plot_widget1.addItem(pg.TextItem(text=best_fit_eq_area, color='y', anchor=(0.5, 0.5), border='w'))

        # Auto scale the plot to fit the data
        self.plot_widget1.autoRange()

        # Calculate the derivative (change in area with respect to time)
        area_derivative = np.diff(areas)

        # Time for the derivative plot is shorter by one step because diff reduces the size by 1
        time_derivative = time[:-1]  # Align time with the derivative data

        # Plot derivative on plot_widget2
        self.plot_widget2.plot(time_derivative, area_derivative, pen=pg.mkPen("r", width=2), name="d(area)/dt")
        for i, d in enumerate(area_derivative):
            self.plot_widget2.plot([i], [d], pen=None, symbol='o', symbolBrush='r', symbolSize=10)

        # # Calculate the line of best fit for the derivative
        # slope_derivative, intercept_derivative = np.polyfit(time_derivative, area_derivative, 1)  # Linear fit
        # best_fit_line_derivative = slope_derivative * time_derivative + intercept_derivative
        # self.plot_widget2.plot(time_derivative, best_fit_line_derivative, pen=pg.mkPen("g", width=2),
        #                        name="Best Fit Line")
        #
        # # Display the best fit equation for the derivative as a label on the plot
        # best_fit_eq_derivative = f"y = {slope_derivative:.2f}x + {intercept_derivative:.2f}"
        # self.plot_widget2.addItem(pg.TextItem(text=best_fit_eq_derivative, color='g', anchor=(0.5, 0.5), border='w'))

        # Auto scale the plot to fit the data
        self.plot_widget2.autoRange()
