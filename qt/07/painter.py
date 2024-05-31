
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QFont
from PySide6.QtWidgets import QWidget

class Pippo(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        painter.drawEllipse(0,0,256,128)
