import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QComboBox, QHBoxLayout, QLabel, QSlider
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
from hydrogen import create_hydrogen


class Window(QDialog):

    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # creating a Vertical Box layout
        layout = QVBoxLayout()

        # adding tool bar to the layout
        layout.addWidget(self.toolbar)

        # adding canvas to the layout
        layout.addWidget(self.canvas)

        lay = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(-100)
        self.slider.setMaximum(95)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.slider_move)
        lay.addWidget(QLabel("Y"))
        lay.addWidget(self.slider)
        layout.addLayout(lay)

        lay, self.n_list = self.create_list("n", [str(x) for x in range(1, 17)])
        self.n_list.currentTextChanged.connect(self.plot)
        layout.addLayout(lay)

        lay, self.l_list = self.create_list("l", ["0"])
        self.l_list.currentTextChanged.connect(self.plot)
        layout.addLayout(lay)

        lay, self.m_list = self.create_list("m", ["0"])
        self.m_list.currentTextChanged.connect(self.plot)
        layout.addLayout(lay)

        # setting layout to the main window
        self.setLayout(layout)

        self.plot()

    def create_list(self, name, init_values):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(name))
        list = QComboBox()
        list.addItems(init_values)
        layout.addWidget(list)
        return layout, list

    def replace_items(self, list, items):
        list.currentTextChanged.disconnect(self.plot)
        list.clear()
        list.addItems(items)
        list.currentTextChanged.connect(self.plot)

    def slider_move(self):
        n = int(self.n_list.currentText())
        l = int(self.l_list.currentText())
        m = int(self.m_list.currentText())
        zmin = -10
        dz = 0.5
        index = int((self.slider.value() / 10 - zmin) / dz)
        self.im.set_data(self.data[index, :, :])
        self.ax.set_title(
            "Hydrogen Orbital xz Slice (y=" + str("%.2f" % (self.slider.value()/10)) + "): n=" + str(n) + ", l=" + str(
                l) + ", m=" + str(m))

        self.canvas.draw()

    def plot(self):
        selected_n = int(self.n_list.currentText())
        if selected_n != self.l_list.count():
            self.replace_items(self.l_list, [str(x) for x in range(selected_n)])

        selected_l = int(self.l_list.currentText())
        if selected_l * 2 + 1 != self.m_list.count():
            self.replace_items(self.m_list, [str(x) for x in range(-selected_l, selected_l + 1)])

        selected_m = int(self.m_list.currentText())

        self.figure.clear()
        self.ax = self.figure.add_subplot(111)

        self.im, self.data = create_hydrogen(selected_n, selected_l, selected_m, self.ax)

        self.slider_move()

        # refresh canvas
        self.canvas.draw()


# driver code
if __name__ == '__main__':
    # creating apyqt5 application
    app = QApplication(sys.argv)

    # creating a window object
    main = Window()

    # showing the window
    main.show()

    # loop
    sys.exit(app.exec_())

