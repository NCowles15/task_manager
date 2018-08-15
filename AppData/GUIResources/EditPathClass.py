import os
from os import listdir
from os.path import isfile, join

from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore
from ClassResources.File_Handler import File_Handler

path = os.path.dirname(os.path.abspath(__file__))
EditPathUI, EditPathBase = uic.loadUiType(os.path.join(path, 'editpath.ui'))

class EditPath(EditPathBase, EditPathUI):
    def __init__(self, data,  current_path_dict, selecteds, parent=None):
        EditPathBase.__init__(self, parent)
        self.setupUi(self)

        self._data = data
        self._potential_items = selecteds
        self._path_name = list(current_path_dict.keys())[0]
        self._path_color = current_path_dict[self._path_name]["Color"]
        self._path_data = current_path_dict[self._path_name]["Data"]

        self.lineEdit_2.setText(self._path_name)
        self.spinBox.setValue(self._path_color[0])
        self.spinBox_2.setValue(self._path_color[1])
        self.spinBox_3.setValue(self._path_color[2])
        self._scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self._scene)

        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.Apply_Changes)
        self.pushButton_4.clicked.connect(self.Set_Path_Data)
        self.spinBox.valueChanged.connect(self.Preview_Color)
        self.spinBox_2.valueChanged.connect(self.Preview_Color)
        self.spinBox_3.valueChanged.connect(self.Preview_Color)
        self.pushButton_5.clicked.connect(self.Set_Path_Name)
        self.pushButton_6.clicked.connect(self.Set_Path_Color)
        self.pushButton_7.clicked.connect(self.Reset_Data_Display)

        self.Preview_Color()
        self.Reset_Data_Display()


    def Apply_Changes(self):
        self.Set_Path_Name()
        self.Set_Path_Color()
        self.Set_Path_Data()

    def Reset_Data_Display(self):
        for existings in self._path_data:
            existing_dict = self._data.get_item(existings)
            existing_title = existing_dict["title"]
            existing_item = QtWidgets.QListWidgetItem(existing_title)
            existing_item.setFlags(QtCore.Qt.ItemIsEnabled | existing_item.flags())
            existing_item.setFlags(QtCore.Qt.ItemIsDragEnabled | existing_item.flags())
            existing_item.setFlags(QtCore.Qt.ItemIsDropEnabled | existing_item.flags())
            if self._data.get_item(existing_title[:6])["completed"]:
                existing_item_font = existing_item.font()
                existing_item_font.setStrikeOut(True)
                existing_item.setFont(existing_item_font)
            self.listWidget.addItem(existing_item)

        for potentials in self._potential_items:
            potential_dict = self._data.get_item(potentials)
            potential_title = potential_dict["title"]
            potential_item = QtWidgets.QListWidgetItem(potential_title)
            potential_item.setFlags(QtCore.Qt.ItemIsEnabled | potential_item.flags())
            potential_item.setFlags(QtCore.Qt.ItemIsDragEnabled | potential_item.flags())
            potential_item.setFlags(QtCore.Qt.ItemIsDropEnabled | potential_item.flags())
            if self._data.get_item(potential_title[:6])["completed"]:
                potential_item_font = potential_item.font()
                potential_item_font.setStrikeOut(True)
                potential_item.setFont(potential_item_font)

            self.listWidget_2.addItem(potential_item)

    def Set_Path_Data(self):
        existing_list = list()
        for i in range(0, self.listWidget.count()):
            existings = self.listWidget.item(i)
            existing_list.append(existings.text()[:6])
            self._path_data = existing_list

        potential_list = list()
        for j in range(0, self.listWidget_2.count()):
            potentials = self.listWidget_2.item(j)
            potential_list.append(potentials.text()[:6])
            self._potential_items = potential_list

    def Set_Path_Name(self):
        self._path_name = self.lineEdit_2.text()

    def Set_Path_Color(self):
        self._path_color = [self.spinBox.value(), self.spinBox_2.value(), self.spinBox_3.value()]

    def Preview_Color(self):
        preview_R = self.spinBox.value()
        preview_G = self.spinBox_2.value()
        preview_B = self.spinBox_3.value()
        color_pixmap = QtGui.QPixmap(100, 100)
        color_pixmap.fill(QtGui.QColor(preview_R, preview_G, preview_B))
        color_pixmap_item = QtWidgets.QGraphicsPixmapItem(color_pixmap)
        color_pixmap_item.setScale(1)
        self._scene.addItem(color_pixmap_item)
        self.graphicsView.fitInView(color_pixmap_item)

    def get_current_path(self):
        out_dict = dict()
        out_dict[self._path_name] = {"Data": self._path_data, "Color": self._path_color}
        return out_dict
