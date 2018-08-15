import os

from PyQt5 import uic

path = os.path.dirname(os.path.abspath(__file__))
CheckableLinksListUI, CheckableLinksListBase = uic.loadUiType(os.path.join(path, 'checkablelinkslist.ui'))


class CheckableLinksList(CheckableLinksListBase, CheckableLinksListUI):
    def __init__(self, checked_titles, parent=None):
        CheckableLinksListBase.__init__(self, parent)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.RefreshList)

        self._checked_list = list(checked_titles)
        # self.RefreshList()

    def get_list(self):
        return self._checked_list

    def RefreshList(self):
        self._checked_list = list()
        if self.listWidget.count() > 0:
            for i in range(0, self.listWidget.count()):
                if self.listWidget.item(i).checkState() == 2:
                    item = self.listWidget.item(i).text()
                    self._checked_list.append(item)
