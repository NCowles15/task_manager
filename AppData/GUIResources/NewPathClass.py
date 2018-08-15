import os

from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore

path = os.path.dirname(os.path.abspath(__file__))
NewPathUI, NewPathBase = uic.loadUiType(os.path.join(path, 'newpath.ui'))

class NewPath(NewPathBase, NewPathUI):
    def __init__(self, all_paths, parent=None):
        NewPathBase.__init__(self, parent)
        self.setupUi(self)
        self._path_color = [255, 255, 255]
        self._path_name = "Path Name"

        self._all_paths = all_paths
        self.lineEdit.setText(self._path_name)
        self.spinBox.setValue(self._path_color[0])
        self.spinBox_2.setValue(self._path_color[1])
        self.spinBox_3.setValue(self._path_color[2])
        self._scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self._scene)

        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_4.clicked.connect(self.Apply_Changes)
        self.spinBox.valueChanged.connect(self.Preview_Color)
        self.spinBox_2.valueChanged.connect(self.Preview_Color)
        self.spinBox_3.valueChanged.connect(self.Preview_Color)
        self.pushButton_5.clicked.connect(self.Set_Path_Color)
        self.pushButton_6.clicked.connect(self.Set_Path_Name)

        self.Preview_Color()

    def Apply_Changes(self):
        self.Set_Path_Color()
        self.Set_Path_Name()

    def Set_Path_Name(self):
        if self.lineEdit.text() in self._all_paths:
            self.label_7.setText("Invalid: Name in Use")
        else:
            self.label_7.setText("")
            self._path_name = self.lineEdit.text()

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

    def get_path_name(self):
        return self._path_name

    def get_path_color(self):
        return self._path_color
