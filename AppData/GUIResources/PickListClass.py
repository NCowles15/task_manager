import os

from PyQt5 import uic

path = os.path.dirname(os.path.abspath(__file__))
PickListUI, PickListBase = uic.loadUiType(os.path.join(path, 'picklist.ui'))


class PickList(PickListBase, PickListUI):
    def __init__(self, parent=None):
        PickListBase.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)
        # self._data = in_data