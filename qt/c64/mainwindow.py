from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontDatabase, QKeyEvent, QTextOption
from PySide6.QtWidgets import QMainWindow, QPlainTextEdit, QStatusBar, QLabel, QMessageBox, QFileDialog
from tokenizer import Tokenizer

class C64TextEdit(QPlainTextEdit):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        super().__init__()
        self.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        #self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.modifiers = {


            Qt.ControlModifier: {
                Qt.Key_1: 61136,
                Qt.Key_2: 57925
            },



        }

    def keyPressEvent(self, e):


        print(e.key(), e.modifiers(), e.modifiers() in self.modifiers)
        #print(self.tokenizer.keys, e.modifiers(), e.modifiers().value, e.key())
        if (e.modifiers().value, e.key()) in self.tokenizer.keys:
            print('key found')
            val = self.tokenizer.keys[(e.modifiers().value, e.key())]
            a = QKeyEvent(e.type(), val, Qt.NoModifier, text=chr(val))
            super().keyPressEvent(a)
        else:
            super().keyPressEvent(e)
        # if e.modifiers() in self.modifiers and e.key() in self.modifiers[e.modifiers()]:
        #     key = self.modifiers[e.modifiers()][e.key()]
        #     print('fottimi',key)
        #     a = QKeyEvent(e.type(), key, Qt.NoModifier, text=chr(key))
        #     super().keyPressEvent(a)
        # else:


class MainWindow(QMainWindow):
    
    def __init__(self, app):
        super().__init__()
        self.appName = 'RetroStudio'
        self.tokenizer = Tokenizer('token.yaml', upperCase=True)
        self.app = app  # used to quit the app
        self.file = ''
        self.setWindowTitle(self.appName)

        # Load the custom font
        font_id = QFontDatabase.addApplicationFont("c64.ttf")
        if font_id == -1:
            print("Failed to load custom font.")
            return

        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # Set the custom font
        custom_font = QFont(font_family)
        custom_font.setPointSize(12)    # Set the font size
        custom_font.setBold(True)       # Make the font bold (optional)
        custom_font.setItalic(False)    # Make the font italic (optional)

        # Apply the font to the QPlainTextEdit widget

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        new_action = file_menu.addAction("&New")
        new_action.triggered.connect(self.newCrossword)
        open_action = file_menu.addAction("&Open")
        open_action.triggered.connect(self.openFile)
        save_action = file_menu.addAction("&Save")
        save_action.triggered.connect(self.save)
        saveas_action = file_menu.addAction("Save as")
        saveas_action.triggered.connect(self.saveas)
        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit)

        menu_bar.addMenu("&Help")

        sb = QStatusBar(self)
        self.setStatusBar(sb)
        self.dictLabel = QLabel("ciao")
        self.gridStatusLabel = QLabel("Empty")
        sb.addPermanentWidget(self.dictLabel)
        sb.addWidget(self.gridStatusLabel)

        self.main = C64TextEdit(self.tokenizer)
        self.main.setFont(custom_font)

        self.setCentralWidget(self.main)

    def quit(self):
        self.app.quit()

    def newCrossword(self):
        ret = QMessageBox.question(self, "New file", "Are you sure?", QMessageBox.Ok | QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            self.main.clear()
            self.setWindowTitle(self.appName)
            print("User chose ok")

    def openFile(self):
        path = QFileDialog.getOpenFileName(self, "Open file", "", "Prg files (*.prg)")
        if not path:
            return
        else:
            self.file = path[0]
            self.setWindowTitle(self.file + ' - ' + self.appName)
            instructions = self.tokenizer.readBasicFile(path[0])
            self.main.clear()
            for key, value in instructions.items():
                self.main.insertPlainText(value+'\n')


    def _save(self):
        print(' -- file: ', self.file)
        # address of next instruction
        address = 0x0801
        instructions = dict()
        
        lines = self.main.toPlainText().split('\n')
        m = bytearray()
        m += address.to_bytes(2, 'little')
        i = 0
        while i < len(lines):
            cl = lines[i]
            i += 1
            if not cl:
                continue
            lc = 0
            while cl[lc].isnumeric():
                lc += 1
            print('line number ends @ ', lc, ': ',cl[:lc])
            inst = self.tokenizer.tokenize(cl[lc:].lstrip())
            print(' # bytes:', len(inst))
            # 4 bytes are occupied to hold address of next BASIC instruction and the line number
            # 1 byte is the 0 at the end of inst
            address += len(inst) + 4 + 1
            ln = int(cl[:lc])
            line_number = ln.to_bytes(2, 'little')
            next_inst = address.to_bytes(2, 'little')
            instruction = bytearray()
            instruction += next_inst
            instruction += line_number
            instruction += inst
            instruction.append(0)
            print(' '.join(f'{x:02x}' for x in instruction))
            instructions[ln] = instruction
            # f.write(instruction)
        sorted_instructions = sorted(instructions)  # [x[1] for x in sorted(instructions.items())]
        for s in sorted_instructions:
            print(int(s), ': ', ' '.join(f'{x:02x}' for x in instructions[s]))
        # print(sorted_instructions)
        # do the proper writing
        with open(self.file, 'wb') as f:
            address = 0x0801
            m = address.to_bytes(2, 'little')
            f.write(m)
            for s in sorted_instructions:
                f.write(instructions[s])
            m = bytearray()
            m.append(0)
            m.append(0)
            f.write(m)

    def saveas(self):
        path = QFileDialog.getSaveFileName(self, "Save file", "", "Prg files (*.prg)")
        if not path:
            return
        self.file = path[0]
        self.setWindowTitle(self.file + ' - ' + self.appName)
        self._save()  # <-- here!

    def save(self):
        if self.file:
            self._save()
        else:
            self.saveas()