import os

from PyQt5 import uic

path = os.path.dirname(os.path.abspath(__file__))
CheckableListUI, CheckableListBase = uic.loadUiType(os.path.join(path, 'checkablelist.ui'))


class CheckableList(CheckableListBase, CheckableListUI):
    def __init__(self, parent=None):
        CheckableListBase.__init__(self, parent)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.ApplySelectAll)

    def ApplySelectAll(self):
        if self.checkBox.checkState() == 2:
            for i in range(0, self.listWidget.count()):
                if self.listWidget.item(i).checkState() == 0:
                    self.listWidget.item(i).setCheckState(2)
        elif self.checkBox.checkState() == 0:
            for i in range(0, self.listWidget.count()):
                if self.listWidget.item(i).checkState() == 2:
                    self.listWidget.item(i).setCheckState(0)