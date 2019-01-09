import sys
import json

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


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
    ex = Demo2()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
