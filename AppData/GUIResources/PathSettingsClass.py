import os

from GUIResources.NewPathClass import NewPath
from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore

path = os.path.dirname(os.path.abspath(__file__))
PathSettingsUI, PathSettingsBase = uic.loadUiType(os.path.join(path, 'pathsettings.ui'))


class PathSettings(PathSettingsBase, PathSettingsUI):
    def __init__(self, data, paths_dict, paths_overlay, current_path_name, parent=None):
        PathSettingsBase.__init__(self, parent)
        self.setupUi(self)

        self._data = data
        self._all_paths = paths_dict
        self._paths_overlay = paths_overlay
        self._current_path_name = current_path_name
        self._removed_path_names = list()
        self._removed_paths = dict()

        for path_name in self._all_paths.keys():
            self.comboBox.addItem(path_name)

        current_path_index = self.comboBox.findText(self._current_path_name)
        self.comboBox.setCurrentIndex(current_path_index)

        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.Apply_Changes)
        self.pushButton_4.clicked.connect(self.Set_Current_Path)
        self.pushButton_5.clicked.connect(self.Add_Path_Triggered)
        self.pushButton_6.clicked.connect(self.Set_Path_Data)
        self.pushButton_7.clicked.connect(self.Reset_Data_Display)
        self.listWidget.itemDoubleClicked.connect(self.DoubleClickRemoval)

        self.Reset_Data_Display()


    def DoubleClickRemoval(self):
        pop_row = self.listWidget.currentRow()
        pop_item = self.listWidget.takeItem(pop_row)
        self._removed_path_names.append(pop_item.text())

    def Apply_Changes(self):
        self.Set_Current_Path()
        self.Set_Path_Data()

    def Reset_Data_Display(self):
        item_brush = QtGui.QBrush()
        item_brush.setStyle(QtCore.Qt.SolidPattern)
        self.listWidget.clear()
        for path_name in self._all_paths.keys():
            path_color = self._all_paths[path_name]["Color"]
            path_item = QtWidgets.QListWidgetItem(path_name)
            item_brush.setColor(QtGui.QColor(path_color[0], path_color[1], path_color[2]))
            path_item.setBackground(item_brush)

            path_item.setFlags(QtCore.Qt.ItemIsEnabled | path_item.flags())
            path_item.setFlags(QtCore.Qt.ItemIsUserCheckable | path_item.flags())

            if self._paths_overlay[path_name].isVisible():
                path_item.setCheckState(2)
            else:
                path_item.setCheckState(0)
            self.listWidget.addItem(path_item)

        self.Refresh_Components_Display()

    def Refresh_Components_Display(self):
        current_components = self._all_paths[self._current_path_name]["Data"]
        self.listWidget_2.clear()
        for component in current_components:
            component_dict = self._data.get_item(component)
            component_title = component_dict["title"]
            component_item = QtWidgets.QListWidgetItem(component_title)
            if self._data.get_item(component_title[:6])["completed"]:
                component_item_font = component_item.font()
                component_item_font.setStrikeOut(True)
                component_item.setFont(component_item_font)
            self.listWidget_2.addItem(component_item)

    def Set_Current_Path(self):
        self._current_path_name = self.comboBox.currentText()
        self.Refresh_Components_Display()

    def Set_Path_Data(self):
        keys_list = list(self._all_paths.keys())
        for path_name in keys_list:
            if path_name in self._removed_path_names:
                self._removed_paths[path_name] = self._all_paths[path_name]
                del self._all_paths[path_name]
                del self._paths_overlay[path_name]
                del_path_index = self.comboBox.findText(path_name)
                self.comboBox.removeItem(del_path_index)
                self.Set_Current_Path()

        for i in range(0, self.listWidget.count()):
            items = self.listWidget.item(i)
            item_name = items.text()
            if items.checkState() == 2:
                self._paths_overlay[item_name].setVisible(True)
            elif items.checkState() == 0:
                self._paths_overlay[item_name].setVisible(False)

    def Add_Path_Triggered(self):
        self.add_path_window = NewPath(self._all_paths)
        self.add_path_window.setWindowTitle("New Path Window")
        self.add_path_window.pushButton.clicked.connect(self.Add_Path_ConfirmButton_Clicked)
        self.add_path_window.show()

    def Add_Path_ConfirmButton_Clicked(self):
        new_path_data = list()
        new_path_color = self.add_path_window.get_path_color()
        new_path_name = self.add_path_window.get_path_name()
        self._all_paths[new_path_name] = {"Data": new_path_data, "Color": new_path_color}
        self._paths_overlay[new_path_name] = QtWidgets.QGraphicsPixmapItem()
        self._paths_overlay[new_path_name].setVisible(False)
        self.comboBox.addItem(new_path_name)
        self.add_path_window.close()
        self.Reset_Data_Display()

    def get_paths_data(self):
        return self._all_paths

    def get_paths_overlay(self):
        return self._paths_overlay

    def get_current_paths(self):
        return self._current_path_name

    def get_removed_paths(self):
        return self._removed_paths