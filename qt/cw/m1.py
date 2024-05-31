import sys
from PySide6.QtWidgets import QApplication
from gamewindow import GameWindow

app = QApplication(sys.argv)

#window = GridSelect('/home/fabrizio/pycrossword/cwgui/schemi.yaml')
window = GameWindow(app)
window.show()

# kickoff the event loop
app.exec()