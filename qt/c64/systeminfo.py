import yaml
from PySide6.QtGui import QFont, QFontDatabase
from pathlib import Path
from tokenizer import Tokenizer, C64Tokenizer, SpeccyTokenizer

class SystemInfo:
    def __init__(self, fontDirectory):
        self.path = Path(fontDirectory)
        with open(self.path / 'main.yaml', 'r') as file:
            data = yaml.safe_load(file)
            self.fontFile = data['font']
            upper = data['upper_case']
            self.fontId = QFontDatabase.addApplicationFont(str(self.path / self.fontFile))
            if self.fontId == -1:
                print("Failed to load custom font.", fontFile)
                exit(1)
            font_family = QFontDatabase.applicationFontFamilies(self.fontId)[0]
            # Set the custom font
            self.font = QFont(font_family)
            self.font.setPointSize(12)  # Set the font size
            self.font.setBold(True)  # Make the font bold (optional)
            self.font.setItalic(False)  # Make the font italic (optional)
            # load tokenizer
            self.tokenizer = globals()[data['class_name']](str(self.path / 'token.yaml'), upperCase=upper)