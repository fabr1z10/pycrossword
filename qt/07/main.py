import sys
from PySide6.QtWidgets import QApplication
from painter import Pippo

app = QApplication(sys.argv)

window = Pippo()
window.show()

# kickoff the event loop
app.exec()