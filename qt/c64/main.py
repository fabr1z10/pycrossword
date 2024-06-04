import sys
from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow

app = QApplication(sys.argv)

#window = GridSelect('/home/fabrizio/pycrossword/cwgui/schemi.yaml')
window = MainWindow(app)
window.show()

# kickoff the event loop
app.exec()