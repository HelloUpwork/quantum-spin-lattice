import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
                             QLabel, QLineEdit, QGridLayout, QSlider, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pickle

def load_results(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super(PlotCanvas, self).__init__(fig)
        self.setParent(parent)

    def plot_data(self, data):
        self.ax.clear()
        self.ax.plot(data)
        self.ax.set_title('Quantum State Energies')
        self.draw()

class SliderGroup(QWidget):
    def __init__(self, label):
        super().__init__()
        self.initUI(label)

    def initUI(self, label):
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(-32)
        self.slider.setMaximum(32)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)

        self.lineEdit = QLineEdit()
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setText("0.00")

        self.slider.valueChanged.connect(self.updateLineEdit)

        layout.addWidget(QLabel(label))
        layout.addWidget(self.slider)
        layout.addWidget(self.lineEdit)

    def updateLineEdit(self):
        self.lineEdit.setText(f"{self.slider.value() / 32:.2f}")

    def value(self):
        return self.slider.value()

    def set_value(self, value):
        self.slider.setValue(value)

class QuantumSimApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Quantum Simulation Viewer'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.filename = 'output/simulation_results.pkl'
        self.result_handler = ResultHandler(self.filename)
        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.sweep_step)
        self.current_j2_value = -1.0

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)
        
        # Layout and widgets
        layout = QGridLayout(mainWidget)

        self.slider_j1 = SliderGroup('j1')
        self.slider_j2 = SliderGroup('j2')

        plotButton = QPushButton('Plot Eigenvalues', self)
        plotButton.clicked.connect(self.plot)

        self.plotCanvas = PlotCanvas(self, width=5, height=4)

        self.sweepButton = QPushButton('Sweep j2', self)
        self.sweepButton.clicked.connect(self.start_sweep)

        layout.addWidget(self.slider_j1, 0, 0, 1, 2)
        layout.addWidget(self.slider_j2, 1, 0, 1, 2)
        layout.addWidget(plotButton, 2, 0, 1, 2)
        layout.addWidget(self.plotCanvas, 3, 0, 1, 2)
        layout.addWidget(self.sweepButton, 1, 3)

    def plot(self):
        j1 = self.slider_j1.value()
        j2 = self.slider_j2.value()

        key = (j1+32, j2+32)
        data = self.result_handler.get_data(key)
        if data:
            self.plotCanvas.plot_data(data[1])
        else:
            print(f"No results available for j1={j1}, j2={j2}")

    def start_sweep(self):
        self.current_j2_value = -32
        self.timer.start(200)  # Adjust the interval for sweep speed

    def sweep_step(self):
        if self.current_j2_value > 32:
            self.timer.stop()
            return
        self.current_j2_value += 1
        self.slider_j2.set_value(self.current_j2_value)
        self.plot()

class ResultHandler:
    def __init__(self, filename):
        self.data = self.load_results(filename)

    @staticmethod
    def load_results(filename):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        return data

    def get_data(self, key):
        return self.data.get(key, None)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QuantumSimApp()
    ex.show()
    sys.exit(app.exec_())