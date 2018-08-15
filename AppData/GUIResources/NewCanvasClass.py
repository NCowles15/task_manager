import os
from os import listdir
from os.path import isfile, join

from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore
from ClassResources.File_Handler import File_Handler

path = os.path.dirname(os.path.abspath(__file__))
NewCanvasUI, NewCanvasBase = uic.loadUiType(os.path.join(path, 'newcanvas.ui'))

class NewCanvas(NewCanvasBase, NewCanvasUI):
    def __init__(self, parent=None):
        NewCanvasBase.__init__(self, parent)
        self.setupUi(self)
        self._map_data = dict()
        self._file_handler = File_Handler()
        self._classes_dir = os.getcwd()
        self._files_dir = self._maps_dir = os.path.join(self._classes_dir, "MapFiles")
        self._resources_dir = self._maps_dir = os.path.join(self._classes_dir, "MapResources")
        self._canvas_dir = os.path.join(self._resources_dir, "MapCanvas")


        self._file_name = ""
        self._canvas_name = ""
        self._canvas_path = ""
        self._coordinate_template = ""
        self._use_coords = False

        self.checkBox.setCheckState(0)
        onlymapfiles = [f for f in listdir(self._files_dir) if isfile(join(self._files_dir, f))]
        for items in onlymapfiles:
            self.comboBox_2.addItem(items)
        onlycanvasfiles = [f for f in listdir(self._canvas_dir) if isfile(join(self._canvas_dir, f))]
        for items in onlycanvasfiles:
            self.comboBox.addItem(items)
        self.comboBox_2.setEnabled(False)
        self._scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self._scene)

        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_4.clicked.connect(self.Apply_Changes)
        self.pushButton_3.clicked.connect(self.Preview_Canvas)

    def Apply_Changes(self):
        self._canvas_name = self.comboBox.currentText()
        self._file_name = self.lineEdit.text()
        self._canvas_path = os.path.join(self._canvas_dir, self._canvas_name)
        # print(self._canvas_path)
        self._map_data["Canvas Path"] = self._canvas_path
        # print(self._map_data)
        if self.checkBox.checkState() == 2:
            self.comboBox_2.setEnabled(True)
            self._use_coords = True
            self._coordinate_template = self.comboBox_2.currentText()
            # print(self._coordinate_template)
            if self._coordinate_template != "":
                if "." in self._coordinate_template:
                    template_list = self._coordinate_template.split(".")
                    self._coordinate_template = template_list[0]
                self._file_handler.set_title(self._coordinate_template)
                temp_map_dict = self._file_handler.file_MapOpen()
                # print(temp_map_dict)
                self._map_data["Coordinates"] = temp_map_dict["Coordinates"]
            else:
                self._map_data["Coordinates"] = dict()
        else:
            self.comboBox_2.setEnabled(False)
            self._use_coords = False
            self._map_data["Coordinates"] = dict()

    def Preview_Canvas(self):
        self._canvas_name = self.comboBox.currentText()
        self._canvas_path = os.path.join(self._canvas_dir, self._canvas_name)
        canvas_pixmap = QtGui.QPixmap(self._canvas_path)
        canvas_pixmap_item = QtWidgets.QGraphicsPixmapItem(canvas_pixmap)
        canvas_pixmap_item.setScale(1)
        canvas_pixmap_item.setData(1, "Canvas")
        canvas_pixmap_item.setData(2, 1)
        self._scene.addItem(canvas_pixmap_item)
        self.graphicsView.fitInView(canvas_pixmap_item)

        # canvas_pixmap_item.setData(3, (4300.0 / 3100.0))

    def get_map_data(self):
        return self._map_data

    def get_map_name(self):
        return self._file_name
