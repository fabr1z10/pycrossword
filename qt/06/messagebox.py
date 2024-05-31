from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox

class MessageBoxWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Message Box Demo")
        button_layout = QVBoxLayout()

        button1 = QPushButton("Hard")
        button1.clicked.connect(self.hard)
        button_layout.addWidget(button1)

        button2 = QPushButton("Critical")
        button2.clicked.connect(self.critical)
        button_layout.addWidget(button2)

        button3 = QPushButton("Question")
        button3.clicked.connect(self.question)
        button_layout.addWidget(button3)

        button4 = QPushButton("Information")
        button4.clicked.connect(self.information)
        button_layout.addWidget(button4)

        button5 = QPushButton("Warning")
        button5.clicked.connect(self.warning)
        button_layout.addWidget(button5)

        button6 = QPushButton("About")
        button6.clicked.connect(self.about)
        button_layout.addWidget(button6)

        self.setLayout(button_layout)

    def hard(self):
        message = QMessageBox()
        message.setMinimumSize(700, 200)
        message.setWindowTitle("Message Title")
        message.setText("Something happened")
        message.setInformativeText("Do you want to do something about it?")
        message.setIcon(QMessageBox.Critical)
        message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        message.setDefaultButton(QMessageBox.Ok)
        ret = message.exec()
        if ret == QMessageBox.Ok:
            print ("User chose ok")
        else:
            print("User chose cancel") 

    def critical(self):
        ret = QMessageBox.critical(self, "Message Title", "Critical Message!", QMessageBox.Ok | QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            print ("User chose ok")
        else:
            print("User chose cancel")

    def question(self):
        ret = QMessageBox.question(self, "Message Title", "Asking a question?", QMessageBox.Ok | QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            print("User chose ok")
        else:
            print("User chose cancel")

    def information(self):
        ret = QMessageBox.information(self, "Message Title", "Critical Message!", QMessageBox.Ok | QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            print("User chose ok")
        else:
            print("User chose cancel")

    def warning(self):
        ret = QMessageBox.warning(self, "Message Title", "Warning Message!", QMessageBox.Ok | QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            print("User chose ok")
        else:
            print("User chose cancel")

    def about(self):
        ret = QMessageBox.about(self, "Message Title", "Critical Message!")
        if ret == QMessageBox.Ok:
            print("User chose ok")
        else:
            print("User chose cancel")
