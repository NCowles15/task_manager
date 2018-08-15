import os

from PyQt5 import uic

path = os.path.dirname(os.path.abspath(__file__))
TextFileDialogUI, TextFileDialogBase = uic.loadUiType(os.path.join(path, 'textfiledialog.ui'))


class TextFileDialog(TextFileDialogBase, TextFileDialogUI):
    def __init__(self, parent=None):
        TextFileDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.close)