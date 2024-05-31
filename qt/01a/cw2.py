from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton

import sys

app = QApplication(sys.argv)



window = QMainWindow()
window.setWindowTitle('Our first MainWindow App!')

button = QPushButton()
button.setText('Press me')
window.setCentralWidget(button)

window.show()

app.exec_()