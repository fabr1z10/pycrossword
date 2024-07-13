from threading import Thread
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QWidget, QMainWindow, QStatusBar, QPushButton, QToolBar, QMessageBox, QDialog, QLabel, QProgressDialog, QVBoxLayout
from gridselect import GridSelect
from crossword import Crossword
from conf import Configuration
from os.path import basename
import sre_yield
class GameWindow(QMainWindow):

    def loadDictionary(self):

        self.cw.setDictionary(self.config.dictionary_file)
        self.dictLabel.setText(basename(self.config.dictionary_file) + ' (' + str(self.cw.dict.word_count) + ')' )
        
    def __init__(self, app):
        super().__init__()
        self.app = app  # used to quit the app
        self.config = Configuration()
        print(self.config)
        self.setWindowTitle("Cruciverba")

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        new_action = file_menu.addAction("&New")
        new_action.triggered.connect(self.newCrossword)
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit)

        edit_menu = menu_bar.addMenu("&Edit")
        gen_action = edit_menu.addAction("&Generate")
        gen_action.triggered.connect(self.generateCrossword)

        menu_bar.addMenu("&Help")

        sb = QStatusBar(self)
        self.setStatusBar(sb)
        self.dictLabel = QLabel("ciao")
        self.gridStatusLabel = QLabel("Empty")
        sb.addPermanentWidget(self.dictLabel)
        sb.addWidget(self.gridStatusLabel)

        main = QWidget()
        main_layout = QVBoxLayout()
        main.setLayout(main_layout)

        self.cw = Crossword()
        self.currentDefinition = QLabel()
        self.currentDefinition.setMaximumHeight(32)
        #button1.clicked.connect(self.button1_clicked)
        main_layout.addWidget(self.cw)
        main_layout.addWidget(self.currentDefinition)
        self.cw.definitionLabel = self.currentDefinition
        self.setCentralWidget(main)
        self.loadDictionary()

    def quit(self):
        self.app.quit()

    def innerGenerate(self):
        self.status = 2
        self.status = self.cw.make()

    def perform(self, qd, t):
        def f():
            if qd.getValue() < qd.maximum():
                qd.setValue(qd.getValue() + 1)
            if self.status != 2:
                t.stop()

    def generateCrossword(self):
        self.currentDefinition.clear()
        self.gridStatusLabel.setText("Working ...")
        self.app.processEvents()

        result = self.cw.make()
        if result == 2:
            self.gridStatusLabel.setText("Schema o dizionario non settato.")
        elif result == 0:
            self.gridStatusLabel.setText("OK.")
        else:
            self.gridStatusLabel.setText("Non sono riuscito. Riprova.")


    def newCrossword(self):
        c = GridSelect('/home/fabrizio/pycrossword/cwgui/schemi.yaml')
        if c.exec() == QDialog.Accepted:
            val = c.getValue()
            size = val['size']
            black = val['black']
            self.cw.defineGrid(size[0], size[1], black)
        #self.subWindow = GridSelect('/home/fabrizio/pycrossword/cwgui/schemi.yaml')
        #self.subWindow.setWindowModality(Qt.ApplicationModal)
        #self.subWindow.move(20, 20)
        #self.subWindow.show()
        #self.subWindow.raise_()

    def toolbar_button_click(self):
        self.statusBar().showMessage("Message from my app", 3000)

    def button1_clicked(self):
        message = QMessageBox()
        message.setMinimumSize(700, 200)
        message.setWindowTitle("ABC")
        message.setText("Something happened.")
        message.setInformativeText("Do you want to do something about it?")
        message.setIcon(QMessageBox.Critical)
        message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        message.setDefaultButton(QMessageBox.Ok)
        ret = message.exec()
        if ret == QMessageBox.Ok:
            print("user chose ok")
        else:
            print("user chose cancel")