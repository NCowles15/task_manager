import os

from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore

path = os.path.dirname(os.path.abspath(__file__))
PrinterSettingsUI, PrinterSettingsBase = uic.loadUiType(os.path.join(path, 'printersettings.ui'))


class PrinterSettings(PrinterSettingsBase, PrinterSettingsUI):
    def __init__(self, data, print_font, arrange_type, parent=None):
        PrinterSettingsBase.__init__(self, parent)
        self.setupUi(self)
        self._arrangement = arrange_type
        self._print_font = print_font
        self._data = data

        arrangement_list = self._data.get_arrangement()
        for item in arrangement_list:
            item_data = self._data.get_item(item)
            item_title = item_data["title"]
            add_item = QtWidgets.QListWidgetItem(item_title)
            add_item.setFont(self._print_font)
            add_item.setFlags(QtCore.Qt.ItemIsUserCheckable | add_item.flags())
            if item_data["display"]:
                add_item.setCheckState(2)
            else:
                add_item.setCheckState(0)
            # add_field.setFlags(QtCore.Qt.ItemIsEnabled | add_field.flags())
            self.listWidget.addItem(add_item)

        max_fields = self._data.get_fields_max()
        for item in max_fields:
            self.comboBox.addItem(item)

        initial_fields = list(self._data.get_fields())
        for element in initial_fields:
            add_field = QtWidgets.QListWidgetItem(element)
            add_field.setFont(self._print_font)
            add_field.setFlags(QtCore.Qt.ItemIsEnabled | add_field.flags())
            add_field.setFlags(QtCore.Qt.ItemIsDragEnabled |add_field.flags())
            add_field.setFlags(QtCore.Qt.ItemIsDropEnabled | add_field.flags())
            self.listWidget_2.addItem(add_field)

        current_arrange_index = self.comboBox_2.findText(self._arrangement)
        self.comboBox_2.setCurrentIndex(current_arrange_index)


        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_4.clicked.connect(self.AddFieldItem)
        self.pushButton_3.clicked.connect(self.SetArrangement)
        self.listWidget_2.itemSelectionChanged.connect(self.RefreshFields)
        self.listWidget_2.itemDoubleClicked.connect(self.DoubleClickRemoval)

    def DoubleClickRemoval(self):
        pop_row = self.listWidget_2.currentRow()
        pop_item = self.listWidget_2.takeItem(pop_row)
        self.RefreshFields()

    def SetArrangement(self):
        self._arrangement = self.comboBox_2.currentText()

    def RefreshFields(self):
        self._data.reset_fields()
        for i in range(0, self.listWidget_2.count()):
            field = self.listWidget_2.item(i).text()
            self._data.add_field(field)

    def AddFieldItem(self):
        selected_field = self.comboBox.currentText()
        new_field = QtWidgets.QListWidgetItem(selected_field)
        new_field.setFont(self._print_font)
        new_field.setFlags(QtCore.Qt.ItemIsEnabled | new_field.flags())
        new_field.setFlags(QtCore.Qt.ItemIsDragEnabled | new_field.flags())
        new_field.setFlags(QtCore.Qt.ItemIsDropEnabled | new_field.flags())
        self.listWidget_2.addItem(new_field)
        self._data.add_field(selected_field)

    def get_data(self):
        return self._data

    def get_arrangement(self):
        return self._arrangement