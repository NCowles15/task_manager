import os

from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore

class MapIcon(QtWidgets.QGraphicsPixmapItem):

    def __init__(self, idx, img_name, comp_path, parent=None, scene=None):
        super().__init__(parent)
        self._img_name = img_name
        self._comps_path = comp_path
        self.idx = idx
        self.itemOpened = QtCore.pyqtBoundSignal
        self.Draw_Icon_Pixmap()


    def mousePressEvent(self, event):
        self.itemSelected(self.idx)

    def itemSelected(self, what):
        self.setZValue(self.zValue()+1)
        self.setSelected(True)
        # print(self.pos())

    def Draw_Icon_Pixmap(self):
        back_paths = list()
        tip_number = self._img_name[1]
        back_number = self._img_name[0]
        if "_" in self._img_name:
            temp_str_list = self._img_name.split('_')
            classes = temp_str_list[0][2:]
            is_completed = True
        else:
            temp_str_list = self._img_name.split('.')
            classes = temp_str_list[0][2:]
            is_completed = False

        if classes[-1] != "W":
            icon_code = classes[-1]
            if len(classes) == 1:
                back_code = ""
                back_paths.append(os.path.join(self._comps_path, "back_{}_{}.png".format(back_code, back_number)))
            else:
                for char in classes[:-1]:
                    back_code = char.lower()
                    back_paths.append(os.path.join(self._comps_path, "back_{}_{}.png".format(back_code, back_number)))

            completed_path = os.path.join(self._comps_path, "_X.png")
            tip_path = os.path.join(self._comps_path, "tip_{}.png".format(tip_number))
            icon_path = os.path.join(self._comps_path, "{}.png".format(icon_code))
            tip_pixmap = QtGui.QPixmap(tip_path)
            icon_pixmap = QtGui.QPixmap(icon_path)
            completed_pixmap = QtGui.QPixmap(completed_path)
            base_back_path = back_paths[0]
            base_back_pixmap = QtGui.QPixmap(base_back_path)
            full_icon_image = base_back_pixmap.copy()
            icon_painter = QtGui.QPainter(full_icon_image)
            if len(back_paths) > 1:
                for j in range(1, len(back_paths)):
                    temp_back_pixmap = QtGui.QPixmap(back_paths[j])
                    icon_painter.drawPixmap(0, 0, temp_back_pixmap)
                icon_painter.drawPixmap(0, 0, tip_pixmap)
                icon_painter.drawPixmap(0, 0, icon_pixmap)
                if is_completed:
                    icon_painter.drawPixmap(0, 0, completed_pixmap)
                self.setPixmap(QtGui.QPixmap(full_icon_image))
                icon_painter.end()
            else:
                icon_painter.drawPixmap(0, 0, tip_pixmap)
                icon_painter.drawPixmap(0, 0, icon_pixmap)
                if is_completed:
                    icon_painter.drawPixmap(0, 0, completed_pixmap)
                self.setPixmap(QtGui.QPixmap(full_icon_image))
                icon_painter.end()

        else:
            icon_code = classes[-2]
            back_code = "w"
            back_paths.append(os.path.join(self._comps_path, "back_{}_{}.png".format(back_code, back_number)))
            if len(classes) > 2:
                for char in classes[:-2]:
                    back_code = char.lower()
                    back_paths.append(os.path.join(self._comps_path, "back_{}_{}.png".format(back_code, back_number)))

                base_back_path = back_paths.pop(1)
            else:
                base_back_path = back_paths.pop(0)

            completed_path = os.path.join(self._comps_path, "_X.png")
            tip_path = os.path.join(self._comps_path, "tip_{}.png".format(tip_number))
            icon_path = os.path.join(self._comps_path, "{}.png".format(icon_code))
            tip_pixmap = QtGui.QPixmap(tip_path)
            icon_pixmap = QtGui.QPixmap(icon_path)
            completed_pixmap = QtGui.QPixmap(completed_path)
            base_back_pixmap = QtGui.QPixmap(base_back_path)
            full_icon_image = base_back_pixmap.copy()
            icon_painter = QtGui.QPainter(full_icon_image)
            if len(back_paths) >= 1:
                for j in range(-1, -len(back_paths) - 1, -1):
                    temp_back_pixmap = QtGui.QPixmap(back_paths[j])
                    icon_painter.drawPixmap(0, 0, temp_back_pixmap)
                icon_painter.drawPixmap(0, 0, tip_pixmap)
                icon_painter.drawPixmap(0, 0, icon_pixmap)
                if is_completed:
                    icon_painter.drawPixmap(0, 0, completed_pixmap)
                self.setPixmap(QtGui.QPixmap(full_icon_image))
                icon_painter.end()
            else:
                icon_painter.drawPixmap(0, 0, tip_pixmap)
                icon_painter.drawPixmap(0, 0, icon_pixmap)
                if is_completed:
                    icon_painter.drawPixmap(0, 0, completed_pixmap)
                self.setPixmap(QtGui.QPixmap(full_icon_image))
                icon_painter.end()

    # def mouseDoubleClickEvent(self, event):
    #     # self.itemOpened.emit(str(self.data(1)))
    #     self.itemOpened.emit()

    # def mouseReleaseEvent(self, event):
    #     self.itemLeave()

    # def itemLeave(self):
    #     print("{} has been left, update coordinates".format(self.data(1)))

    # def itemOpened(self, in_data):
    #     pass
    #     # print("{} has been opened".format(self.data(1)))

