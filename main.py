#!/usr/bin/env python

import sys
import json
import numpy as np
# import pyqtgraph as pg
# import pyqtgraph.examples as pge

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# from pyqtgraph import *
# import pyqtgraph.Qt
# import pyqtgraph as pg
# from pyqtgraph.Qt import QtC


class Fractal:
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules

    def get_rule(self):
        rand = np.random.rand()
        for rule in self.rules:
            if rand < rule['weight']:
                return rule
            rand -= rule['weight']


class FractalGenerator(QWidget):
    def __init__(self, fractal):
        super().__init__()
        # self.activated = False
        self.activated = True
        self.fractal = fractal
        self.x = np.random.rand()
        self.y = np.random.rand()
        self.width = 800
        self.height = 800
        self.setFixedSize(self.width, self.height)
        # rec = QApplication.desktop().availableGeometry()
        # r = QDesktopWidget.size()
        self.image = QImage(self.width, self.height, QImage.Format_Mono)
        self.image.fill(1)
        self.painter = QPainter(self)
        # self.scene = QGraphicsScene()
        # self.view = QGraphicsView()
        # self.view.setScene(self.scene)
        # self.view.setViewport(QOpenGLWidget())

        # self.painter.begin(self)
        # self.painter.fillRect(self.rect(), QBrush(QColor(255, 255, 255)))
        # self.painter.end()
        self.show()
        # self.painter.setRenderHint(QPainter.Antialiasing, False)

    def set_activated(self, value):
        self.activated = value

    def iterate(self):
        # print("iter")
        # self.u
        # self.painter.save()
        for i in range(0, 100):
        # for i in range(0, 1):
            rule = self.fractal.get_rule()
            x = self.x * rule['a'] + self.y * rule['b'] + rule['tx']
            y = self.x * rule['c'] + self.y * rule['d'] + rule['ty']
            self.x = x
            self.y = y
            self.plot(i)
        # self.painter.drawPixmap(self.rect(), QPixmap(self.image))
        # if not self.activated:
        #     # self.image.fill(1)
        #     return
        # self.update()
        # self.iterate()
        # self.painter.restore()
        # QTimer.singleShot(100, self.iterate)

    def plot(self, i):
        # x = int(self.x)
        x2 = int(self.x * 350) + int(self.width / 2)
        # x = int(self.x * 350)
        # y = int(self.y)
        y2 = int(-self.y * 350) + self.height
        # y = int(-self.y * 350)
        # print(str(i) + ': (' + str(x) + ', ' + str(y) + ')')
        # self.painter.drawPoint(x2, y2)
        # self.scene.addRect().drawPoint(x2, y2)
        # self.image.d
        self.image.setPixel(x2, y2, 0)
        # self.image.setPixel(200, 200, 0)
        # self.painter.drawPoint(200, 200)
        # self.image.setPixel(201, 200, 0)
        # self.painter.drawPoint(201, 200)
        # self.image.setPixel(202, 200, 0)
        # self.painter.drawPoint(202, 200)
        # self.image
        # self.painter.drawPixmap(self.rect(), QPixmap(self.image))

    def paintEvent(self, event):
        # if not self.activated:
        #     self.image.fill(1)
        #     return

        self.painter.begin(self)
        # self.painter.translate(self.width / 2, self.height / 2)
        # self.painter.begin(self.image)
        # self.image.fill(0)
        # self.painter.fillRect(self.rect(), QBrush(QColor(255, 255, 255)))
        # self.painter.setPen(QColor(0, 0, 0))
        # self.painter.restore()
        if self.activated:
            # self.image.fill(1)
            self.iterate()
            self.painter.drawPixmap(self.rect(), QPixmap(self.image))
            self.update()
        else:
            self.image.fill(1)
            self.painter.drawPixmap(self.rect(), QPixmap(self.image))
        # self.plot()
        # self.painter.restore()
        self.painter.end()
        # self.update()
        # self.painter.drawPixmap(self.rect(), QPixmap.fromImage(QImage('newton.png')))
        # img = QImage('newton.png')
        # i2 = QImage(400,400, QImage.Format_Mono)
        # i2.fill(0)
        # painter = QPainter(self)
        # painter.begin(img)
        # painter.setRenderHint(QPainter.Antialiasing, False)

        # painter.drawPixmap(self.rect(), QPixmap(i2))
        # painter.end()


def get_fractals(input_file):
    result = []

    with open(input_file) as file:
        fractals = json.loads(file.read())

    for fractal in fractals:
        name = fractal['name']
        rules = fractal['rules']
        result.append(Fractal(name, rules))

    return result

class IFSFractals(QMainWindow):
    def __init__(self, input_file, parent=None):
        super(IFSFractals, self).__init__(parent)

        self.fractals = get_fractals(input_file)
        self.drawings = QStackedWidget()
        self.drawings.setFixedSize(800, 800)
        # self.drawings.show()
        #
        for fractal in self.fractals:
            drawing = FractalGenerator(fractal)
            drawing.activated = True
            self.drawings.addWidget(drawing)

        app_layout = QHBoxLayout()

        panel = QDockWidget("Fractals")

        options_widget = QWidget()
        options_layout = QVBoxLayout()
        options_layout.setAlignment(Qt.AlignTop)

        # combo_box, stacked_widget = parse_json('data.json')
        self.combo_box, self.stacked_widget = self.get_widgets()
        self.combo_box.activated.connect(self.stacked_widget.setCurrentIndex)
        # self.combo_box.activated.connect(self.handle_switch)
        self.combo_box.activated.connect(self.drawings.setCurrentIndex)

        options_layout.addWidget(self.combo_box)
        options_layout.addWidget(self.stacked_widget)
        options_widget.setLayout(options_layout)

        panel.setWidget(options_widget)

        # self.setCentralWidget(QTextEdit())
        self.setCentralWidget(self.drawings)
        # f = FractalGenerator(self.fractals[0])
        # f.show()
        # self.setCentralWidget(f)
        self.addDockWidget(Qt.RightDockWidgetArea, panel)
        self.setLayout(app_layout)

    def handle_switch(self, index):
        self.drawings[index].activated = True
        self.stacked_widget.setCurrentIndex(index)
        for i in range(len(self.drawings)):
            if i != index:
                self.drawings[i].activated = False

    def get_widgets(self):
        stacked_widget = QStackedWidget()
        combo_box = QComboBox()

        for fractal in self.fractals:
            fractal_widget = QWidget()
            # fractal_name = fractal.name
            fractal_layout = QVBoxLayout()

            for rule in fractal.rules:
                rule_box = QGroupBox()
                rule_layout = QHBoxLayout()

                rule_layout.setAlignment(Qt.AlignJustify)

                for key, value in rule.items():
                    widget = get_parameter_widget(key, value)
                    rule_layout.addWidget(widget)

                rule_box.setLayout(rule_layout)
                fractal_layout.addWidget(rule_box)

            fractal_widget.setLayout(fractal_layout)
            stacked_widget.addWidget(fractal_widget)
            combo_box.addItem(fractal.name)

        # combo_box.activated.connect(stacked_widget.setCurrentIndex)
        # combo_box.activated.connect(self.drawings.setCurrentIndex)
        return combo_box, stacked_widget


def get_parameter_widget(key, value):
    precision = 100

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)

    label = QLabel(key)
    label.setAlignment(Qt.AlignCenter)

    slider = QSlider(Qt.Vertical)
    slider.setMinimum(0)
    slider.setMaximum(max(value, 2) * precision)
    slider.setTickInterval(1)
    slider.setValue(value * precision)
    slider.setTickPosition(QSlider.TicksRight)

    layout.addWidget(label)
    layout.addWidget(slider)

    widget = QWidget()
    widget.setLayout(layout)

    return widget


def parse_json(input_file):
    stacked_widget = QStackedWidget()
    combo_box = QComboBox()

    with open(input_file) as file:
        fractals = json.loads(file.read())

    # print(content)
    for fractal in fractals:


        fractal_widget = QWidget()
        fractal_name = fractal['name']
        fractal_layout = QVBoxLayout()

        for rule in fractal['rules']:
            rule_box = QGroupBox()
            rule_layout = QHBoxLayout()

            rule_layout.setAlignment(Qt.AlignJustify)

            for key, value in rule.items():
                widget = get_parameter_widget(key, value)
                rule_layout.addWidget(widget)

            rule_box.setLayout(rule_layout)
            fractal_layout.addWidget(rule_box)

        fractal_widget.setLayout(fractal_layout)
        stacked_widget.addWidget(fractal_widget)
        combo_box.addItem(fractal_name)

    combo_box.activated.connect(stacked_widget.setCurrentIndex)
    return combo_box, stacked_widget


# class FractalCanvas()


class Demo2(QMainWindow):
    def __init__(self, parent=None):
        super(Demo2, self).__init__(parent)

        app_layout = QHBoxLayout()

        panel = QDockWidget("Fractals")

        options_widget = QWidget()
        options_layout = QVBoxLayout()
        options_layout.setAlignment(Qt.AlignTop)

        combo_box, stacked_widget = parse_json('data.json')
        options_layout.addWidget(combo_box)
        options_layout.addWidget(stacked_widget)
        options_widget.setLayout(options_layout)

        panel.setWidget(options_widget)

        self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea, panel)
        self.setLayout(app_layout)


class Demo(QMainWindow):
    def __init__(self, parent=None):
        super(Demo, self).__init__(parent)

        layout = QHBoxLayout()
        panel = QDockWidget("Sliders")
        cb = QComboBox()
        cb.addItem("Barnsley fern")
        cb.addItem("Sierpinski triangle")
        # cb.currentIndexChange
        list_widget = QWidget()

        f1 = QGroupBox()
        f1_layout = QHBoxLayout()
        sl = QSlider(Qt.Vertical)
        label = QLabel('aa')
        # f1_layout.setAlignment(Qt.AlignCenter)
        # label.setAlignment(Qt.AlignCenter)
        sl.setMinimum(10)
        sl.setMaximum(30)
        sl.setTickInterval(5)
        sl.setTickPosition(QSlider.TicksRight)

        f1_layout.addWidget(label)
        f1_layout.addWidget(sl)

        sl2 = QSlider(Qt.Vertical)
        label2 = QLabel('aa')
        # f1_layout.setAlignment(Qt.AlignJustify)
        # label.setAlignment(Qt.AlignCenter)
        sl2.setMinimum(10)
        sl2.setMaximum(30)
        sl2.setTickInterval(5)
        sl2.setTickPosition(QSlider.TicksRight)

        f1_layout.addWidget(label2)
        f1_layout.addWidget(sl2)

        f1_layout.setAlignment(Qt.AlignJustify)
        f1.setLayout(f1_layout)

        f2 = QGroupBox()
        # f1.
        lw_layout = QVBoxLayout()
        lw_layout.setAlignment(Qt.AlignTop)
        lw_layout.addWidget(cb)
        lw_layout.addWidget(f1)
        lw_layout.addWidget(f2)
        list_widget.setLayout(lw_layout)

        panel.setWidget(list_widget)
        # layout.addWidget(cb)
        self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea, panel)
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    ex = IFSFractals('data.json')
    ex.show()
    # fractals = get_fractals('data.json')
    # f = FractalGenerator(fractals[0])
    # f.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    # pge.run()
    # plot([1, 2, 3])
