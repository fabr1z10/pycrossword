import sys
from PySide6.QtWidgets import QApplication
from button_holder import ButtonHolder, ButtonHolder2, SliderHolder

app = QApplication(sys.argv)

window = SliderHolder()
window.show()

app.exec()