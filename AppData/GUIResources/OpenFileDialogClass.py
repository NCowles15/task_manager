import os
from os import listdir
from os.path import isfile, join

from PyQt5 import uic

path = os.path.dirname(os.path.abspath(__file__))
OpenFileDialogUI, OpenFileDialogBase = uic.loadUiType(os.path.join(path, 'openfiledialog.ui'))


class OpenFileDialog(OpenFileDialogBase, OpenFileDialogUI):
    def __init__(self, folder, parent=None):
        OpenFileDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)
        file_path = os.path.join(os.getcwd(), folder)
        onlyfiles = [f for f in listdir(file_path) if isfile(join(file_path, f))]
        for items in onlyfiles:
            self.comboBox.addItem(items)