from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout

class RockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rock Widget")
        button1 = QPushButton("Button1")
        button1.clicked.connect(self.button1_clicked)

        button2 = QPushButton("Button2")
        button2.clicked.connect(self.button2_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        self.setLayout(button_layout)

    def button1_clicked(self):
        print("Button 1 clicked.")

    def button2_clicked(self):
        print("Button 2 clicked.")
