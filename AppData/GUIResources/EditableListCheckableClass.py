import os

from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore

path = os.path.dirname(os.path.abspath(__file__))
EditableListCheckableUI, EditableListCheckableBase = uic.loadUiType(os.path.join(path, 'editablelist.ui'))


class EditableListCheckable(EditableListCheckableBase, EditableListCheckableUI):
    def __init__(self, in_list, parent=None):
        EditableListCheckableBase.__init__(self, parent)
        self.setupUi(self)
        self._list = list(in_list)

        for item in self._list:
            if item[0:4] == "[X] ":
                string_item = item[4:]
                add_item = QtWidgets.QListWidgetItem(string_item)
                # add_item.setFlags(QtCore.Qt.ItemIsUserCheckable | add_item.flags())
                add_item.setCheckState(QtCore.Qt.Checked)
            else:
                string_item = item
                add_item = QtWidgets.QListWidgetItem(string_item)
                # add_item.setFlags(QtCore.Qt.ItemIsUserCheckable | add_item.flags())
                add_item.setCheckState(QtCore.Qt.Unchecked)
            # add_item = QtWidgets.QListWidgetItem(string_item)
            add_item.setFlags(QtCore.Qt.ItemIsUserCheckable | add_item.flags())
            add_item.setFlags(QtCore.Qt.ItemIsEnabled | add_item.flags())
            add_item.setFlags(QtCore.Qt.ItemIsDragEnabled | add_item.flags())
            add_item.setFlags(QtCore.Qt.ItemIsDropEnabled | add_item.flags())
            add_item.setFlags(QtCore.Qt.ItemIsEditable | add_item.flags())
            self.listWidget.addItem(add_item)

        self.pushButton_3.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.AddBlank)
        self.listWidget.itemDoubleClicked.connect(self.DoubleClickRemoval)
        self.listWidget.itemPressed.connect(self.RefreshList)
        self.listWidget.itemChanged.connect(self.LengthLabel)

    def get_list(self):
        return self._list

    def AddBlank(self):
        add_item = QtWidgets.QListWidgetItem("BLANK ITEM")
        # new_field.setFont(self._print_font)
        add_item.setFlags(QtCore.Qt.ItemIsUserCheckable | add_item.flags())
        add_item.setFlags(QtCore.Qt.ItemIsEnabled | add_item.flags())
        add_item.setFlags(QtCore.Qt.ItemIsDragEnabled | add_item.flags())
        add_item.setFlags(QtCore.Qt.ItemIsDropEnabled | add_item.flags())
        add_item.setFlags(QtCore.Qt.ItemIsEditable | add_item.flags())
        add_item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(add_item)
        self.listWidget.setCurrentRow(self.listWidget.count()-1)
        self.RefreshList()

    def LengthLabel(self):
        if self.listWidget.count() > 0:
            selected_row = self.listWidget.currentRow()
            selected_item = self.listWidget.item(selected_row)
            selected_text = selected_item.text()
            set_length = len(selected_text)
            self.label_3.setText(str(set_length))
        else:
            self.label_3.setText(str(0))

    def RefreshList(self):
        self._list = list()
        if self.listWidget.count() > 0:
            for i in range(0, self.listWidget.count()):
                if self.listWidget.item(i).checkState() == 2:
                    item = self.listWidget.item(i).text()
                    item = "[X] " + item
                    self._list.append(item)
                # else:
                elif self.listWidget.item(i).checkState() == 0:
                    item = self.listWidget.item(i).text()
                    self._list.append(item)
            self.LengthLabel()

    def DoubleClickRemoval(self):
        pop_row = self.listWidget.currentRow()
        pop_item = self.listWidget.takeItem(pop_row)
        self.RefreshList()

    # def EditItem(self):