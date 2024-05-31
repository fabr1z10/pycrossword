from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QSlider

class ButtonHolder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Holder App")
        button = QPushButton("Press me!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    # The slot: responds when something happens
    def button_clicked(self):
        print('You clicked the button.')

class ButtonHolder2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Button Holder App")
        button = QPushButton("Press me!")
        # makes the button checkable.It's unchecked by default; further clicks toggle between checked and unchecked
        button.setCheckable(True)
        # clicked is a signal of QPushButton. You can wire a slot to the signal using the syntax below :
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    # The slot: responds when something happens
    def button_clicked(self, data):
        print('You clicked the button. checked: ', data)

class SliderHolder(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("Slider Holder App")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(100)
        slider.setValue(25)
        slider.valueChanged.connect(self.respond_to_slider)
        self.setCentralWidget(slider)

    # The slot: responds when something happens
    def respond_to_slider(self, value):
        print('slider moved to:',value)
