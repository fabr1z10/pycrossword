import sys
from PySide6.QtWidgets import QApplication
from messagebox import MessageBoxWidget

app = QApplication(sys.argv)

window = MessageBoxWidget()
window.show()

# kickoff the event loop
app.exec()