from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDialog, QListWidget, QHBoxLayout, QVBoxLayout, QDialogButtonBox
from crossword import Crossword
import yaml




            
class GridSelect(QDialog):
    def __init__(self, gridFile: str):
        super().__init__()

        self.setMinimumSize(640,400)
        self.setWindowTitle("Scegli uno schema")
        layout = QHBoxLayout()
        self.preview_widget = Crossword()
        self.preview_widget.playable = False
        self.li = QListWidget()
        self.li.currentItemChanged.connect(self.item_changed)    
        with open(gridFile) as stream:
            try:
                self.schemi = yaml.safe_load(stream)
                for s in self.schemi:
                    self.li.addItem(s)
                    #print(s)
            except yaml.YAMLError as exc:
                print(exc)
        #ci = li.currentItem().text()
        #self.preview_widget.defineGrid(self.schemi[ci]['size'][0], self.schemi[ci]['size'][1])
        layout.addWidget(self.preview_widget, 2)
        self.li.setCurrentRow(0)
        rhs = QWidget()
        vl = QVBoxLayout()
        rhs.setLayout(vl)
        vl.addWidget(self.li)
        okbtn = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        okbtn.accepted.connect(self.accept)
        okbtn.rejected.connect(self.reject)

        vl.addWidget(okbtn)
        layout.addWidget(rhs, 1)
        self.setLayout(layout)

    def item_changed(self, item):
        grid = self.schemi[item.text()]
        self.preview_widget.defineGrid(grid['size'][0], grid['size'][1], grid['black'])
        self.preview_widget.repaint()

    def getValue(self):
        if self.li.currentItem():
            return self.schemi[self.li.currentItem().text()]
        return None