from PySide6.QtCore import Qt, QRect, QLineF
from PySide6.QtGui import QColor, QPalette, QPainter, QVector2D, QBrush, QFont
from PySide6.QtWidgets import QWidget
import pycrossword


class Crossword(QWidget):
    def __init__(self):
        super().__init__()
        self.pad = 10
        self.blackPad = 2
        self.gridWidth = None
        self.gridHeight = None
        self.highlightedWord = None
        self.bgColor = QColor.fromString("#FBF1C7")
        self.currentWordColor = QColor.fromRgb(192, 192, 192)
        self.cursorColor = QColor.fromRgb(128, 128, 128)
        self.playable = True
        self.grid = None
        self.dict = None
        self.definitionLabel = None

        pal = QPalette()
        pal.setColor(self.backgroundRole(), self.bgColor)
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        self.setFocusPolicy(Qt.ClickFocus)

    def setDictionary(self, file):
        self.dict = pycrossword.Dict(file, 100)

    def mousePressEvent(self, event):
        if not self.gridWidth or not self.playable:
            return
        pos = event.pos()
        if (pos.x() < self.tl.x() or pos.y() < self.tl.y() or pos.x() > self.br.x() or pos.y() > self.br.y()):
            return
        col = int((pos.x() - self.tl.x()) / self.cell_size)
        row = int((pos.y() - self.tl.y()) / self.cell_size)
        self.cursorPos = QVector2D(col, row)
        print('x=', col, 'y=', row)
        acrossClue = self.grid.getAcross(row, col)
        downClue = self.grid.getDown(row, col)
        if acrossClue:
            print('found across: ', acrossClue.id)
        if downClue:
            print('found down: ', downClue.id)
        if acrossClue and downClue:
            if self.highlightedWord and self.highlightedWord[0] == acrossClue.id:
                c = downClue
            else:
                c = acrossClue
        else:
            c = acrossClue if acrossClue else downClue
        if c:
            self.highlightedWord = (c.id, c.x, c.y, c.len)
            self.repaint()
            print('suca:',c.clue)
            if self.definitionLabel:
                self.definitionLabel.setText(c.clue)

    def moveRight(self):
        if 1 + self.cursorPos.x() - self.highlightedWord[1] < self.highlightedWord[3]:
            self.cursorPos.setX(self.cursorPos.x() + 1)

    def moveLeft(self):
        if self.cursorPos.x() - 1 >= self.highlightedWord[1]:
            self.cursorPos.setX(self.cursorPos.x() - 1)

    def moveDown(self):
        if 1 + self.cursorPos.y() - self.highlightedWord[2] < self.highlightedWord[3]:
            self.cursorPos.setY(self.cursorPos.y() + 1)

    def moveUp(self):
        if self.cursorPos.y() - 1 >= self.highlightedWord[2]:
            self.cursorPos.setY(self.cursorPos.y() - 1)

    def keyPressEvent(self, event):
        if not self.playable:
            return
        key = event.key()
        print(f"Found key {key}")
        if self.highlightedWord:
            if key >= 65 and key <= 90:
                self.letters[(self.cursorPos.x(), self.cursorPos.y())] = chr(key)
                if self.highlightedWord[0][-1] == 'a':
                    self.moveRight()
                else:
                    self.moveDown()
                self.repaint()
            elif key == Qt.Key_Left:
                if self.highlightedWord[0][-1] == 'a':
                    self.moveLeft()
                    self.repaint()
            elif key == Qt.Key_Right:
                if self.highlightedWord[0][-1] == 'a':
                    self.moveRight()
                    self.repaint()
            elif key == Qt.Key_Up:
                if self.highlightedWord[0][-1] == 'd':
                    self.moveUp()
                    self.repaint()
            elif key == Qt.Key_Down:
                if self.highlightedWord[0][-1] == 'd':
                    self.moveDown()
                    self.repaint()
            elif key == Qt.Key_Backspace:
                del self.letters[(self.cursorPos.x(), self.cursorPos.y())]
                self.repaint()

    def defineGrid(self, width: int, height: int, black: list):
        self.gridWidth = width
        self.gridHeight = height
        self.blackSquares = black
        self.grid = pycrossword.Grid(self.gridWidth, self.gridHeight, self.blackSquares)
        self.letters = dict()

    def make(self):
        if self.grid and self.dict:
            return pycrossword.make(self.dict, self.grid)
        else:
            return 2

    def paintEvent(self, paintEvent):
        if not self.gridWidth:
            return
        painter = QPainter(self)
        # get widget rectangle
        a = self.rect()
        w1 = (a.width() - 2 * self.pad) / self.gridWidth
        w2 = (a.height() - 2 * self.pad) / self.gridHeight
        cell_size = min(w1, w2)
        grid_width = self.gridWidth * cell_size
        grid_height = self.gridHeight * cell_size
        # now compute top left corner
        if w2 <= w1:
            self.tl = QVector2D((a.width() - grid_width) // 2, self.pad)
        else:
            self.tl = QVector2D(self.pad, (a.height() - grid_height) // 2)
        self.br = self.tl + QVector2D(grid_width, grid_height)
        # painter.drawEllipse(0, 0, a.width(), a.height())
        # draw highlighted word (if any)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        if self.highlightedWord:
            brush.setColor(self.currentWordColor)
            painter.setBrush(brush)
            hw = self.highlightedWord
            if hw[0][-1] == 'a':
                hww = hw[3] * cell_size
                hwh = cell_size
            else:
                hww = cell_size
                hwh = hw[3] * cell_size
            painter.drawRect(self.tl.x() + hw[1] * cell_size, self.tl.y() + hw[2] * cell_size, hww, hwh)
            brush.setColor(self.cursorColor)
            painter.setBrush(brush)
            painter.drawRect(self.tl.x() + self.cursorPos.x() * cell_size, self.tl.y() + self.cursorPos.y() * cell_size,
                             cell_size, cell_size)

        painter.drawLines(
            [QLineF(self.tl.x() + i * cell_size, self.tl.y(), self.tl.x() + i * cell_size, self.tl.y() + grid_height)
             for i in range(0, self.gridWidth + 1)])
        painter.drawLines(
            [QLineF(self.tl.x(), self.tl.y() + i * cell_size, self.tl.x() + grid_width, self.tl.y() + i * cell_size) for
             i in range(0, self.gridHeight + 1)])
        # plot black squares
        brush = QBrush()
        brush.setColor(QColor.fromRgb(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        for i in range(0, len(self.blackSquares), 2):
            painter.drawRect(self.tl.x() + self.blackSquares[i] * cell_size + self.blackPad,
                             self.tl.y() + self.blackSquares[i + 1] * cell_size + self.blackPad,
                             cell_size - 2 * self.blackPad,
                             cell_size - 2 * self.blackPad)

        # place clue numbers
        inc = 1
        painter.setFont(QFont("times", cell_size * 0.25))
        for y in range(0, self.gridHeight):
            for x in range(0, self.gridWidth):
                if not self.grid.isBlack(x, y):
                    if (self.grid.isBlack(x - 1, y) and not self.grid.isBlack(x + 1, y)) or (
                            self.grid.isBlack(x, y - 1) and not self.grid.isBlack(x, y + 1)):
                        painter.drawText(self.tl.x() + x * cell_size + self.blackPad,
                                         self.tl.y() + y * cell_size + self.blackPad + cell_size * 0.25, str(inc))
                        inc += 1
        self.cell_size = cell_size

        # place letters
        painter.setFont(QFont("arial", cell_size * 0.65))
        for pos, letter in self.letters.items():
            qr = QRect(self.tl.x() + pos[0] * cell_size, self.tl.y() + pos[1] * cell_size, cell_size, cell_size)
            painter.drawText(qr, Qt.AlignCenter, letter)