from globals import fontSize,fontName
from PyQt4.QtGui import QColor, QFont

class Style:
    def __init__(self):
        self.color = QColor('#000000')
        self.paper = QColor('#FFFFFF')
        self.caret = QColor('#ffe4e4')
        self.marker = QColor('#ee1111')
        self.margin = QColor('#cccccc')
        self.font = QFont()
        self.font.setFamily(fontName)
        self.font.setFixedPitch(True)
        self.font.setPointSize(fontSize)