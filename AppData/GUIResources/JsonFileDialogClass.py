import os

from PyQt5 import uic

path = os.path.dirname(os.path.abspath(__file__))
JsonFileDialogUI, JsonFileDialogBase = uic.loadUiType(os.path.join(path, 'jsonfiledialog.ui'))


class JsonFileDialog(JsonFileDialogBase, JsonFileDialogUI):
    def __init__(self, parent=None):
        JsonFileDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.close)