import os
from os import listdir
from os.path import isfile, join

from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore

path = os.path.dirname(os.path.abspath(__file__))
SwapCanvasUI, SwapCanvasBase = uic.loadUiType(os.path.join(path, 'swapcanvas.ui'))

class SwapCanvas(SwapCanvasBase, SwapCanvasUI):
    def __init__(self, parent=None):
        SwapCanvasBase.__init__(self, parent)
        self.setupUi(self)
        self._classes_dir = os.getcwd()
        self._resources_dir = self._maps_dir = os.path.join(self._classes_dir, "MapResources")
        self._canvas_dir = os.path.join(self._resources_dir, "MapCanvas")

        self._canvas_name = ""
        self._canvas_path = ""

        onlycanvasfiles = [f for f in listdir(self._canvas_dir) if isfile(join(self._canvas_dir, f))]
        for items in onlycanvasfiles:
            self.comboBox.addItem(items)

        self._scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self._scene)

        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_4.clicked.connect(self.Apply_Changes)
        self.pushButton_3.clicked.connect(self.Preview_Canvas)

    def Apply_Changes(self):
        self._canvas_name = self.comboBox.currentText()
        self._canvas_path = os.path.join(self._canvas_dir, self._canvas_name)

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

    def get_canvas_path(self):
        return self._canvas_path

    def get_canvas_name(self):
        return self._canvas_name
