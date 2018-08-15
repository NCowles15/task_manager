import os
import numpy as np
from datetime import date
from datetime import datetime

from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore
from ClassResources.File_Handler import File_Handler
from GUIResources.MapIconClass import MapIcon
from GUIResources.OpenFileDialogClass import OpenFileDialog
from GUIResources.NewCanvasClass import NewCanvas
from GUIResources.SwapCanvasClass import SwapCanvas
from GUIResources.FilterSettingsClass import FilterSettings
from GUIResources.ItemEditorClass import ItemEditor
from GUIResources.NewPathClass import NewPath
from GUIResources.PathSettingsClass import PathSettings
from GUIResources.EditPathClass import EditPath
from GUIResources.JsonFileDialogClass import JsonFileDialog
from GUIResources.CalendarMapWindowClass import CalendarMapWindow

path = os.path.dirname(os.path.abspath(__file__))
MapMainWindowUI, MapMainWindowBase = uic.loadUiType(os.path.join(path, 'mapmainwindow.ui'))

class MapMainWindow(MapMainWindowBase, MapMainWindowUI):
    def __init__(self, data, filters, data_file, recycler, cal_ids, print_font, parent=None):
        MapMainWindowBase.__init__(self, parent)
        self.setupUi(self)
        self._data = data
        self._filters = filters
        self._recycler = recycler
        self._data_file = data_file
        self._calID_dict = cal_ids
        self._print_font = print_font
        self._zoom_factor = 1.0

        self._map_data = dict()
        self._map_file = File_Handler()
        self._paths_data = dict()
        self._paths_file = File_Handler()
        self._icon_items_dict = dict()
        self._scene = QtWidgets.QGraphicsScene()
        self._arrow_overlay_item = QtWidgets.QGraphicsPixmapItem()
        self._canvas_item = QtWidgets.QGraphicsPixmapItem()
        self._paths_overlay_items = dict()
        self._current_path_name = ""
        self._arrow_overlay_on = False
        self._classes_dir = os.getcwd()
        self._maps_dir = os.path.join(self._classes_dir, "MapResources")
        self._prints_path = os.path.join(self._classes_dir, "MapPrintouts")
        # self._icons_dir = os.path.join(self._maps_dir, "MapIcons")
        self._icons_components_dir = os.path.join(self._maps_dir, "MapComponents")
        self._canvas_dir = os.path.join(self._maps_dir, "MapCanvas")
        self.actionToggle_Priority_Scales.setChecked(False)
        self._icon_priority_scales = self.actionToggle_Priority_Scales.isChecked()


        self.graphicsView.setScene(self._scene)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setMinimum(30)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setToolTip(str(self.horizontalSlider.value()))

        self.actionLoad_Canvas.triggered.connect(self.Load_Canvas_Triggered)
        self.actionNew_Canvas.triggered.connect(self.New_Canvas_Triggered)
        self.actionSave_Map_Data.triggered.connect(self.Save_Map_File)
        self.actionLock_Current_Coords.triggered.connect(self.Lock_Coordinates)
        self.actionFilter_Settings.triggered.connect(self.Filter_Settings_Triggered)
        self.actionSwap_Canvas.triggered.connect(self.Swap_Canvas_Triggered)
        self.actionClear_Selected.triggered.connect(self.Clear_Selections)
        self.actionDuplicate_Item.triggered.connect(self.Duplicate_Selected_Triggered)
        self.actionEdit_Item.triggered.connect(self.Edit_Item_Triggered)
        self.actionAdd_Item.triggered.connect(self.Add_Item_Triggered)
        self.actionExport_Screenshot.triggered.connect(self.Full_Screenshot)
        self.actionToggle_Arrows.triggered.connect(self.Toggle_Arrows)
        self.actionDelete_Selected.triggered.connect(self.Delete_Selected)
        self.actionLink_Selected.triggered.connect(self.Link_Selected)
        self.actionDelink_Selected.triggered.connect(self.DeLink_Selected)
        self.actionSave_Exit.triggered.connect(self.Save_Exit)
        self.actionFull_Save.triggered.connect(self.Full_Save)
        self.actionClear_Links.triggered.connect(self.Clear_Links)
        self.actionNew_Path.triggered.connect(self.New_Path)
        self.actionImport_Path.triggered.connect(self.Import_Paths_Triggered)
        self.actionSave_Paths.triggered.connect(self.Save_Paths)
        self.actionPath_Settings.triggered.connect(self.Path_Settings_Triggered)
        self.actionEdit_Current_Path.triggered.connect(self.Edit_Current_Path_Triggered)
        self.actionExport_Paths.triggered.connect(self.Export_Paths_Triggered)
        self.actionCalendar_View.triggered.connect(self.Calendar_View_Triggered)
        self.actionToggle_Priority_Scales.triggered.connect(self.Update_Priority_Scales)
        # self.actionExport_Selection.triggered.connect(self.New_Canvas_Triggered)

        self.horizontalSlider.valueChanged.connect(self.ZoomChange)
        # self._scene.selectionChanged.connect(self.Update_Selection)

        self.pushButton_2.clicked.connect(self.close)

    def Calendar_View_Triggered(self):
        self.calendar_window = CalendarMapWindow(self._data, self._map_data, self._paths_data, self._filters, self._data_file, self._recycler, self._calID_dict, self._current_path_name)
        # self.calendar_window = CalendarMapWindow()
        self.calendar_window.setWindowTitle("Calendar View Window")
        self.calendar_window.pushButton.clicked.connect(self.Calendar_View_ConfirmButton_Clicked)
        self.calendar_window.show()

    def Calendar_View_ConfirmButton_Clicked(self):
        self._data = self.calendar_window.get_data()
        self._filters = self.calendar_window.get_filters()
        # print(self._map_data)
        self._map_data = self.calendar_window.get_map()
        # print(self._map_data)
        self._paths_data = self.calendar_window.get_paths()

        self.calendar_window.close()
        self.Refresh_Triggered()

    def Full_Save(self):
        self._data_file.file_DataSave(self._data.get_data())
        # print("full save")

    def Save_Exit(self):
        self.Save_Map_File()
        self.pushButton.click()

    def get_data(self):
        return self._data

    def get_map_filters(self):
        return self._filters

    def New_Canvas_Triggered(self):
        self.new_map_window = NewCanvas()
        self.new_map_window.setWindowTitle("New Map File")
        self.new_map_window.pushButton.clicked.connect(self.New_Canvas_ConfirmButton_Clicked)
        self.new_map_window.show()

    def New_Canvas_ConfirmButton_Clicked(self):
        new_map_data = self.new_map_window.get_map_data()
        map_name = self.new_map_window.get_map_name()

        if new_map_data["Canvas Path"] == "":
            pass
        elif new_map_data["Coordinates"] == dict():
            #initialize to zero
            count = 0.0
            for obs in self._data.get_arrangement():
                x_y_floats = list()
                x_y_floats.append(count)
                x_y_floats.append(0.0)
                new_map_data["Coordinates"][obs] = x_y_floats
                count += 30.0

        self._map_data = new_map_data
        self._map_file.set_title(map_name)
        self._map_file.file_MapOut(self._map_data, map_name)

        self.new_map_window.close()
        self.Render_Map()

    def Swap_Canvas_Triggered(self):
        self.swap_canvas_window = SwapCanvas()
        self.swap_canvas_window.setWindowTitle("Swap Map Canvas")
        self.swap_canvas_window.pushButton.clicked.connect(self.Swap_Canvas_ConfirmButton_Clicked)
        self.swap_canvas_window.show()

    def Swap_Canvas_ConfirmButton_Clicked(self):
        new_canvas_path = self.swap_canvas_window.get_canvas_name()
        self._map_data["Canvas Path"] = new_canvas_path
        self.swap_canvas_window.close()
        self.Render_Map()

    def Load_Canvas_Triggered(self):
        self.load_map_window = OpenFileDialog("MapFiles")
        self.load_map_window.setWindowTitle("Open Map File")
        self.load_map_window.pushButton_2.clicked.connect(self.Load_Canvas_ConfirmButton_Clicked)
        self.load_map_window.show()

    def Load_Canvas_ConfirmButton_Clicked(self):
        map_name_raw = self.load_map_window.comboBox.currentText()
        if "." in map_name_raw:
            map_name_list = map_name_raw.split('.')
            map_name = map_name_list[0]
        else:
            map_name = map_name_raw
        self._map_file.set_title(map_name)
        # need exceptions handling, or do I?
        self._map_data = self._map_file.file_MapOpen()
        # print(self._data.get_data().keys())
        for keys in list(self._data.get_data().keys()):
            # print("keys: {}".format(keys))
            if keys not in self._map_data["Coordinates"]:
                # print("{} not in map_data, initializing".format(keys))
                self._map_data["Coordinates"][keys] = [0,0]

        # print(self._map_data["Coordinates"].keys())
        for keys2 in list(self._map_data["Coordinates"].keys()):
            # print(self._map_data["Coordinates"])
            # print("keys2: {}".format(keys2))
            if keys2 not in self._data.get_data():
                # print("{} not in data, deleting".format(keys2))
                del self._map_data["Coordinates"][keys2]
                # print(self._map_data["Coordinates"])
        self.load_map_window.close()
        # print("Rendering Map")
        self.Render_Map()
        self.Import_Paths_Triggered()

    def Filter_Settings_Triggered(self):
        self.filter_settings = FilterSettings(self._data, self._filters, self._calID_dict, self._print_font)
        self.filter_settings.setWindowTitle("Map Filter Settings")
        self.filter_settings.pushButton.clicked.connect(self.Filter_Settings_ConfirmButton_Clicked)
        self.filter_settings.show()

    def Filter_Settings_ConfirmButton_Clicked(self):
        self.filter_settings.ApplyChanges()
        self._filters = self.filter_settings.get_filters()
        self._data.main_filter(self._filters)
        self.filter_settings.close()
        self.Refresh_Triggered()

    def Update_Priority_Scales(self):
        self._icon_priority_scales = self._icon_priority_scales = self.actionToggle_Priority_Scales.isChecked()
        self.Refresh_Triggered()

    def Refresh_Triggered(self):

        self.Refresh_Icons()

        self.Render_Arrows()

        self.Render_Paths()

    def Refresh_Icons(self):
        for icon_item_key in self._icon_items_dict:
            icon_item = self._icon_items_dict[icon_item_key]
            self._scene.removeItem(icon_item)
        self._icon_items_dict = dict()
        for obs in self._data.get_arrangement():
            self.Render_Icon(obs)

        self._data.set_printables()
        printables_list = list(self._data.get_printables())
        all_items = self._scene.items()
        for item in all_items:
            if (item.data(1) != "Canvas") and (item.data(1) != "Arrows Overlay") and (item.data(1) != "Path Overlay"):
                item_number = item.data(1)[:6]
                if item_number in printables_list:
                    item.setVisible(True)
                else:
                    item.setVisible(False)

    def Save_Map_File(self):
        self._map_file.file_MapSave(self._map_data)

    def Lock_Coordinates(self):
        all_items = self._scene.items()
        for items in all_items:
            if (items.data(1) != "Canvas") and (items.data(1) != "Arrows Overlay") and (items.data(1) != "Path Overlay"):
                #if at full original scale, then can save current coords
                real_x_pos = items.pos().x()/self._zoom_factor
                real_y_pos = items.pos().y()/self._zoom_factor
                items.setData(3, QtCore.QPointF(real_x_pos, real_y_pos))
                item_number = items.data(1)[:6]
                self._map_data["Coordinates"][item_number][0] = real_x_pos
                self._map_data["Coordinates"][item_number][1] = real_y_pos
        self.Render_Arrows()
        self.Render_Paths()

    def Render_Map(self):
        self._scene.clear()
        self.graphicsView.viewport().update()
        if self._map_data != dict():
            canvas_path = os.path.join(self._canvas_dir, self._map_data["Canvas Path"])
            canvas_pixmap = QtGui.QPixmap(canvas_path)
            canvas_pixmap_item = QtWidgets.QGraphicsPixmapItem(canvas_pixmap)
            canvas_pixmap_item.setScale(1)
            self._scene.addItem(canvas_pixmap_item)
            canvas_pixmap_item.setData(1, "Canvas")
            canvas_pixmap_item.setData(2, 1)
            canvas_pixmap_item.setData(3, canvas_pixmap_item.boundingRect())
            canvas_pixmap_item.setZValue(-3)
            self._canvas_item = canvas_pixmap_item
            # canvas_pixmap_item.setData(3, (4300.0 / 3100.0))

            for obs in self._data.get_arrangement():
                # print("rendering {}".format(obs))
                self.Render_Icon(obs)
            # print("Rendering Arrows")
            self.Render_Arrows()

    def Clear_Selections(self):
        all_items = self._scene.items()
        for items in all_items:
            if (items.data(1) != "Canvas") and (items.data(1) != "Arrows Overlay") and (items.data(1) != "Path Overlay"):
                items.setSelected(False)
                items.setZValue(0.0)

    def ZoomChange(self):
        self.horizontalSlider.setToolTip(str(self.horizontalSlider.value()))
        zoom_value_base = self.horizontalSlider.value()
        zoom_value = zoom_value_base/100.0
        self._zoom_factor = zoom_value
        for items in self._scene.items():
            base_item_scale = items.data(2)
            new_scale = base_item_scale * zoom_value
            items.setScale(new_scale)
            if (items.data(1) != "Canvas") and (items.data(1) != "Arrows Overlay") and (items.data(1) != "Path Overlay"):
                # print(items.data(1), items.pos())
                item_x_pos = items.data(3).x()
                item_y_pos = items.data(3).y()
                new_x_pos = item_x_pos * zoom_value
                new_y_pos = item_y_pos * zoom_value
                items.setPos(new_x_pos, new_y_pos)
                # print(items.data(1), items.pos())
        self._scene.setSceneRect(self._canvas_item.sceneBoundingRect())
        self.graphicsView.viewport().update()

    def Edit_Item_Triggered(self):
        selected_items = self._scene.selectedItems()
        if len(selected_items) == 1:
            temp_item = selected_items[0]
            item_dict = self._data.get_item(temp_item.data(1)[:6])
            self.item_editor = ItemEditor(item_dict, self._calID_dict, self._data)
            self.item_editor.pushButton_3.clicked.connect(self.ItemEditor_ConfirmButton_Clicked)
            self.item_editor.show()

    def Add_Item_Triggered(self):
        default_item = dict()
        self._data.make_valid_item(default_item, "000.00")
        self.item_editor = ItemEditor(default_item, self._calID_dict, self._data)
        self.item_editor.setWindowTitle("Item Editor")
        self.item_editor.pushButton_3.clicked.connect(self.ItemEditor_ConfirmButton_Clicked)
        self.item_editor.show()

    def ItemEditor_ConfirmButton_Clicked(self):
        temp_num = self.item_editor.get_number()
        temp_data = self.item_editor.get_data()
        selected_items = self._scene.selectedItems()
        if len(selected_items) == 1:
            old_item_num = selected_items[0].data(1)[:6]
            selected_item = selected_items[0]
            selected_item_pos = selected_item.pos()
            self._scene.removeItem(selected_item)
            if temp_num != old_item_num:
                # old item has been REPLACED. deleter references to old Item
                self._data.remove_item(old_item_num)
                del self._map_data["Coordinates"][old_item_num]
        else:
            selected_item_pos = QtCore.QPointF(0.0,0.0)

        if temp_num not in self._map_data["Coordinates"]:
            pos_list = [selected_item_pos.x(), selected_item_pos.y()]
            self._map_data["Coordinates"][temp_num] = pos_list

        self._data.set_item(temp_num, temp_data)
        self._data.reset_links()
        # for from_item in temp_data["from-links"]:
        #     temp_from_number = from_item[0:6]
        #     temp_from_item = self._data.get_item(temp_from_number)
        #     if temp_data["title"] not in temp_from_item["to-links"]:
        #         temp_from_item["to-links"].append(temp_data["title"])
        #     self._data.set_item(temp_from_number,temp_from_item)
        #
        # for to_item in temp_data["to-links"]:
        #     temp_to_number = to_item[0:6]
        #     temp_to_item = self._data.get_item(temp_to_number)
        #     if temp_data["title"] not in temp_to_item["from-links"]:
        #         temp_to_item["from-links"].append(temp_data["title"])
        #     self._data.set_item(temp_to_number,temp_to_item)


        self.Render_Icon(temp_num)

        new_item = None
        for scene_items in self._scene.items():
            if scene_items.data(1)[:6] == temp_num:
                new_item = scene_items
        new_item.setScale(new_item.data(2) * self._zoom_factor)

        new_item.setPos(QtCore.QPointF(new_item.pos().x() * self._zoom_factor, new_item.pos().y() * self._zoom_factor))
        self.item_editor.close()
        self.Refresh_Triggered()

    def Duplicate_Selected_Triggered(self):
        selected_items = self._scene.selectedItems()
        for items in selected_items:
            # get item to duplicate
            item_number = items.data(1)[:6]
            item = dict(self._data.get_item(item_number))
            old_title = item["title"]
            item_number1 = item_number[0:3]
            item_number2 = int(item_number[4:])

            for keys in self._data.get_data():
                if (keys[0:3] == item_number1) and (int(keys[4:]) > item_number2):
                    item_number2 = int(keys[4:])

            item_number2 += 1

            new_item_number = "{}.{:0>2}".format(item_number1, item_number2)
            new_title = new_item_number + old_title[6:]
            item["title"] = new_title
            item["from-links"] = list()
            item["to-links"] = list(item["to-links"])
            self._data.set_item(new_item_number, item)

            #render duplicate item offset from map_data["coordinates"]["item_number"]

            pos_list = [items.pos().x()+10.0, items.pos().y()]
            self._map_data["Coordinates"][new_item_number] = pos_list
            self.Render_Icon(new_item_number)

            new_item = None
            for scene_items in self._scene.items():
                if scene_items.data(1)[:6] == new_item_number:
                    new_item = scene_items
            new_item.setScale(new_item.data(2) * self._zoom_factor)

            self._map_data["Coordinates"][new_item_number] = [new_item.pos().x()/self._zoom_factor, new_item.pos().y()/self._zoom_factor]
            new_item.setData(3, QtCore.QPointF(new_item.pos().x()/self._zoom_factor, new_item.pos().y()/self._zoom_factor))

        # print(self._data.get_item(new_item_number))
        # print(self._map_data["Coordinates"][new_item_number])
            self._filters["manual"].append(new_item_number)
        self.Refresh_Triggered()

    def Render_Icon(self, obs):
        self._data.main_filter(self._filters)
        self._data.set_printables()
        temp_dict = self._data.get_item(obs)
        file_nums = obs[:2]
        file_class = temp_dict["classification"]
        if temp_dict["completed"]:
            file_name = file_nums + file_class + "_X.png"
        else:
            file_name = file_nums + file_class + ".png"
        # file_name = file_nums + file_class + ".png"
        if self._icon_priority_scales:
            scale_seed = temp_dict["priority number"]
            scale_var = 1 / (np.exp(scale_seed)) + 0.5
            if scale_var > 1.0:
                scale_var = 1.0
        else:
            scale_var = 0.5
        # icon_path = os.path.join(self._icons_dir, file_name)
        # map_icon_item = MapIcon(0, icon_path, None, self._scene)
        map_icon_item = MapIcon(0, file_name, self._icons_components_dir, None, self._scene)
        map_icon_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        map_icon_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        map_icon_item.setScale(scale_var)
        map_icon_item.setPos(self._map_data["Coordinates"][obs][0], self._map_data["Coordinates"][obs][1])
        map_icon_item.setData(1, temp_dict["title"])
        map_icon_item.setData(2, scale_var)
        map_icon_item.setData(3, map_icon_item.pos())
        map_icon_item.setData(4, map_icon_item.sceneBoundingRect())
        map_icon_item.setToolTip("{} \nSet for {}".format(temp_dict["title"], temp_dict["due date"]))
        if temp_dict["completed"]:
            map_icon_item.setScale(0.5)
            map_icon_item.setData(2, 0.5)
            map_icon_item.setData(4, map_icon_item.sceneBoundingRect())
            map_icon_item.setOpacity(0.4)
        else:
            map_icon_item.setOpacity(0.9)

        if obs in self._data.get_printables():
            map_icon_item.setVisible(True)
        else:
            map_icon_item.setVisible(False)
        self._icon_items_dict[obs] = map_icon_item
        self._scene.addItem(map_icon_item)

    def Full_Screenshot(self):

        canvas_image = QtGui.QImage(self._map_data["Canvas Path"])
        new_canvas = canvas_image.copy()
        new_canvas_painting = QtGui.QPainter(new_canvas)

        if self._arrow_overlay_on:
            arrows_pixmap = self._arrow_overlay_item.pixmap()
            new_canvas_painting.drawPixmap(0, 0, arrows_pixmap)

        for items in self._scene.items():
            if (items.data(1) != "Canvas") and (items.data(1) != "Arrows Overlay"):
                if items.data(1)[:6] in self._data.get_printables():
                    obs = items.data(1)[:6]
                    temp_dict = self._data.get_item(obs)
                    resized_icon_width = items.sceneBoundingRect().width()
                    resized_icon_height = items.sceneBoundingRect().height()

                    icon_pixmap = items.pixmap()
                    new_icon_pixmap = icon_pixmap.scaled(int(resized_icon_width), int(resized_icon_height))

                    if temp_dict["completed"]:
                        new_canvas_painting.setOpacity(0.4)
                    else:
                        new_canvas_painting.setOpacity(0.9)
                    new_canvas_painting.drawPixmap(self._map_data["Coordinates"][obs][0], self._map_data["Coordinates"][obs][1], new_icon_pixmap)
                    new_canvas_painting.setOpacity(1)

        screen_path = os.path.join(self._prints_path, "{} {}_({}.{}.{}).png".format(self._map_file.get_title(), date.today(), datetime.today().hour, datetime.today().minute, datetime.today().second))
        new_canvas.save(screen_path)
        # print(screen_path)
        new_canvas_painting.end()

    def Delete_Selected(self):
        recycle_dict = dict()
        if len(self._scene.selectedItems()) > 0:
            for items in self._scene.selectedItems():
                if items.data(1)[:6] in self._data.get_arrangement():
                    # print("deleting ", items.data(1))
                    recycle_dict[items.data(1)[:6]] = self._data.remove_item(items.data(1)[:6])
                    # self._data.remove_item(items.data(1)[:6])
                    self._scene.removeItem(items)
                    del self._map_data["Coordinates"][items.data(1)[:6]]
        self._recycler.file_Recycle(recycle_dict)
        self.Refresh_Triggered()

    def Link_Selected(self):
        if len(self._scene.selectedItems()) == 2:
            if self._scene.selectedItems()[0].zValue() <= self._scene.selectedItems()[1].zValue():
                from_item = self._scene.selectedItems()[1]
                to_item = self._scene.selectedItems()[0]
            else:
                from_item = self._scene.selectedItems()[0]
                to_item = self._scene.selectedItems()[1]
            from_dict = self._data.get_item(from_item.data(1)[:6])
            to_dict = self._data.get_item(to_item.data(1)[:6])
            if from_item.data(1) not in to_dict["from-links"] or to_item.data(1) not in from_dict["to-links"]:
                to_dict["from-links"].append(from_item.data(1))
                from_dict["to-links"].append(to_item.data(1))
                self._data.set_item(from_item.data(1)[:6], from_dict)
                self._data.set_item(to_item.data(1)[:6], to_dict)
        self.Refresh_Triggered()

    def DeLink_Selected(self):
        if len(self._scene.selectedItems()) == 2:
            if self._scene.selectedItems()[0].zValue() <= self._scene.selectedItems()[1].zValue():
                from_item = self._scene.selectedItems()[1]
                to_item = self._scene.selectedItems()[0]
            else:
                from_item = self._scene.selectedItems()[0]
                to_item = self._scene.selectedItems()[1]
            from_dict = self._data.get_item(from_item.data(1)[:6])
            to_dict = self._data.get_item(to_item.data(1)[:6])
            if from_item.data(1) in to_dict["from-links"] and to_item.data(1) in from_dict["to-links"]:
                # print("delinking {} and {}".format(from_item.data(1), to_item.data(1)))
                to_index = to_dict["from-links"].index(from_item.data(1))
                del to_dict["from-links"][to_index]
                from_index = from_dict["to-links"].index(to_item.data(1))
                del from_dict["to-links"][from_index]
                self._data.set_item(to_item.data(1)[:6], to_dict)
                self._data.set_item(from_item.data(1)[:6], from_dict)
        self.Refresh_Triggered()

    def Clear_Links(self):
        for items in self._scene.selectedItems():
            item_num = items.data(1)[:6]
            item_dict = self._data.get_item(item_num)
            item_dict["from-links"] = list()
            item_dict["to-links"] = list()
            self._data.set_item(item_num, item_dict)

    def Render_Arrows(self):
        self._data.reset_links()
        blank_overlay_dimensions = self._canvas_item.data(3)
        blank_overlay_image = QtGui.QPixmap(int(blank_overlay_dimensions.width()), int(blank_overlay_dimensions.height()))
        blank_overlay_image.fill(QtGui.QColor("transparent"))
        overlay_painter = QtGui.QPainter(blank_overlay_image)
        black_pen5 = QtGui.QPen()
        black_pen5.setColor(QtGui.QColor(0, 0, 0))
        black_pen5.setWidth(5)
        black_pen2 = QtGui.QPen()
        black_pen2.setColor(QtGui.QColor(0, 0, 0))
        black_pen2.setWidth(2)
        white_pen = QtGui.QPen()
        white_pen.setColor(QtGui.QColor(255, 255, 255))
        white_pen.setWidth(2)
        white_brush = QtGui.QBrush()
        white_brush.setColor(QtGui.QColor(255, 255, 255))
        white_brush.setStyle(QtCore.Qt.SolidPattern)

        printables_list = self._data.get_printables()
        for items in printables_list:
            to_links = self._data.get_item(items)["to-links"]
            for link in to_links:
                # if self._data.get_item(items)["title"] not in self._data.get_item(link[:6])["from-links"]:
                #     from_dict = self._data.get_item(link[:6])
                #     from_dict["from-links"].append(self._data.get_item(items)["title"])
                #     self._data.set_item(link[:6], from_dict)

                if link[:6] in printables_list:
                    # print("drawing {} to {}".format(items, link))
                    from_item = None
                    to_item = None
                    for scene_items in self._scene.items():
                        if scene_items.data(1)[:6] == items:
                            from_item = scene_items
                        elif scene_items.data(1)[:6] == link[:6]:
                            to_item = scene_items

                    from_point = QtCore.QPointF(self._map_data["Coordinates"][from_item.data(1)[:6]][0]+(from_item.data(4).width())/2, self._map_data["Coordinates"][from_item.data(1)[:6]][1]+from_item.data(4).height())
                    to_point = QtCore.QPointF(self._map_data["Coordinates"][to_item.data(1)[:6]][0]+(to_item.data(4).width())/2, self._map_data["Coordinates"][to_item.data(1)[:6]][1]+to_item.data(4).height())
                    # from_point = QtCore.QPointF(self._map_data["Coordinates"][from_item.data(1)[:6]][0]*from_item.data(2)+(from_item.boundingRect().width())/2, self._map_data["Coordinates"][from_item.data(1)[:6]][1]+from_item.boundingRect().height())
                    # to_point = QtCore.QPointF(self._map_data["Coordinates"][to_item.data(1)[:6]][0]+(to_item.boundingRect().width())/2, self._map_data["Coordinates"][to_item.data(1)[:6]][1]+to_item.boundingRect().height())
                    # from_point = QtCore.QPointF(from_item.pos().x()+(from_item.sceneBoundingRect().width())/2, from_item.pos().y()+from_item.sceneBoundingRect().height())
                    # to_point = QtCore.QPointF(to_item.pos().x()+(to_item.sceneBoundingRect().width())/2, to_item.pos().y()+to_item.sceneBoundingRect().height())

                    to_line = QtCore.QLineF(from_point, to_point)
                    angle = np.arctan2(-to_line.dy(), to_line.dx())
                    arrow_head_size = 15
                    # to_head1 = QtCore.QPointF
                    to_head2 = QtCore.QPointF(to_point.x() - arrow_head_size*np.sin(angle + np.pi/3), to_point.y() - arrow_head_size*np.cos(angle + np.pi/3))
                    to_head3 = QtCore.QPointF(to_point.x() - arrow_head_size*np.sin(angle + np.pi - (np.pi/3)), to_point.y() - arrow_head_size*np.cos(angle + np.pi - (np.pi/3)))


                    # print("triangle points: ", [to_point, to_head1, to_head2])
                    head_triangle = QtGui.QPolygonF([to_point, to_head2, to_head3])

                    overlay_painter.setPen(black_pen5)
                    overlay_painter.drawLine(to_line)
                    overlay_painter.setBrush(white_brush)
                    overlay_painter.setPen(black_pen2)
                    overlay_painter.drawPolygon(head_triangle)
                    overlay_painter.drawEllipse(from_point, 5, 5)
                    overlay_painter.setPen(white_pen)
                    overlay_painter.drawLine(from_point, to_point)
                    # print("{} to {} drawn".format(from_item.data(1), to_item.data(1)))

        if self._arrow_overlay_item in self._scene.items():
            self._scene.removeItem(self._arrow_overlay_item)
        self._arrow_overlay_item = QtWidgets.QGraphicsPixmapItem(blank_overlay_image)
        self._arrow_overlay_item.setData(1, "Arrows Overlay")
        self._arrow_overlay_item.setData(2, 1)
        self._arrow_overlay_item.setScale(self._zoom_factor)
        self._arrow_overlay_item.setZValue(-2)

        if self._arrow_overlay_on:
            self._arrow_overlay_item.setVisible(True)
        else:
            self._arrow_overlay_item.setVisible(False)
        self._scene.addItem(self._arrow_overlay_item)
        overlay_painter.end()

    def Toggle_Arrows(self):
        if not (self._arrow_overlay_on):
            self._arrow_overlay_item.setVisible(True)
            self._arrow_overlay_on = True
        else:
            self._arrow_overlay_item.setVisible(False)
            self._arrow_overlay_on = False

    def Import_Paths_Triggered(self):
        self.load_path_window = OpenFileDialog("PathsFiles")
        self.load_path_window.setWindowTitle("Open Path File")
        self.load_path_window.pushButton_2.clicked.connect(self.Import_Paths_ConfirmButton_Clicked)
        self.load_path_window.show()

    def Import_Paths_ConfirmButton_Clicked(self):
        path_name_raw = self.load_path_window.comboBox.currentText()
        if path_name_raw != "":
            if "." in path_name_raw:
                path_name_list = path_name_raw.split('.')
                path_name = path_name_list[0]
            else:
                path_name = path_name_raw
            self._paths_file.set_title(path_name)
            # need exceptions handling, or do I?
            self._paths_data = self._paths_file.file_PathsOpen()
            for keys in self._paths_data:
                self._paths_overlay_items[keys] = QtWidgets.QGraphicsPixmapItem()
                self._paths_overlay_items[keys].setVisible(False)
                self._paths_overlay_items[keys].setData(1, "Path Overlay")
                self._scene.addItem(self._paths_overlay_items[keys])
                self._current_path_name = keys
            self.load_path_window.close()
            self.Render_Paths()

    def New_Path(self):
        self.new_path_window = NewPath(self._paths_data)
        self.new_path_window.setWindowTitle("New Path Window")
        self.new_path_window.pushButton.clicked.connect(self.New_Path_ConfirmButton_Clicked)
        self.new_path_window.show()

    def New_Path_ConfirmButton_Clicked(self):
        new_path_data = list()
        new_path_color = self.new_path_window.get_path_color()
        new_path_name = self.new_path_window.get_path_name()
        self._paths_data[new_path_name] = {"Data": new_path_data, "Color": new_path_color}
        self._paths_overlay_items[new_path_name] = QtWidgets.QGraphicsPixmapItem()
        self._paths_overlay_items[new_path_name].setVisible(False)
        self._current_path_name = new_path_name
        self.new_path_window.close()
        self.Render_Paths()

    def Save_Paths(self):
        self._paths_file.file_PathsSave(self._paths_data)

    def Export_Paths_Triggered(self):
        self.path_file_finder = JsonFileDialog()
        self.path_file_finder.setWindowTitle("Save Path File As")
        self.path_file_finder.pushButton.clicked.connect(self.Export_Paths_ConfirmButton_Clicked)
        self.path_file_finder.show()

    def Export_Paths_ConfirmButton_Clicked(self):
        file_name = self.path_file_finder.lineEdit.text()
        self._paths_file.file_PathsOut(self._paths_data, file_name)
        self.path_file_finder.close()

    def Path_Settings_Triggered(self):
        self.path_settings_window = PathSettings(self._data, self._paths_data, self._paths_overlay_items, self._current_path_name)
        self.path_settings_window.setWindowTitle("Path Settings")
        self.path_settings_window.pushButton.clicked.connect(self.Path_Settings_ConfirmButton_Clicked)
        self.path_settings_window.show()

    def Path_Settings_ConfirmButton_Clicked(self):
        self._paths_data = self.path_settings_window.get_paths_data()
        self._paths_overlay_items = self.path_settings_window.get_paths_overlay()
        self._current_path_name = self.path_settings_window.get_current_paths()
        deleted_paths = self.path_settings_window.get_removed_paths()
        self._recycler.file_Recycle(deleted_paths)
        self.path_settings_window.close()
        self.Render_Paths()

    def Edit_Current_Path_Triggered(self):
        current_path = {self._current_path_name: self._paths_data[self._current_path_name]}
        selecteds = list()
        for selected_items in self._scene.selectedItems():
            selecteds.append(selected_items.data(1)[:6])
        self.edit_path_window = EditPath(self._data, current_path, selecteds)
        self.edit_path_window.setWindowTitle("Edit Current Path")
        self.edit_path_window.pushButton.clicked.connect(self.Edit_Current_Path_ConfirmButton_Clicked)
        self.edit_path_window.show()

    def Edit_Current_Path_ConfirmButton_Clicked(self):
        current_path = self.edit_path_window.get_current_path()

        old_graphic = self._paths_overlay_items[self._current_path_name]
        del self._paths_data[self._current_path_name]
        del self._paths_overlay_items[self._current_path_name]

        self._current_path_name = list(current_path.keys())[0]
        self._paths_data[self._current_path_name] = current_path[self._current_path_name]
        self._paths_overlay_items[self._current_path_name] = old_graphic
        self.edit_path_window.close()

        self.Render_Paths()

    def Render_Paths(self):
        for paths in self._paths_data:

            blank_overlay_dimensions = self._canvas_item.data(3)
            blank_overlay_image = QtGui.QPixmap(int(blank_overlay_dimensions.width()),
                                                int(blank_overlay_dimensions.height()))
            blank_overlay_image.fill(QtGui.QColor("transparent"))
            overlay_painter = QtGui.QPainter(blank_overlay_image)
            path_color = QtGui.QColor(self._paths_data[paths]["Color"][0], self._paths_data[paths]["Color"][1],
                                      self._paths_data[paths]["Color"][2])
            black_pen5 = QtGui.QPen()
            black_pen5.setColor(QtGui.QColor(0, 0, 0))
            black_pen5.setWidth(5)
            black_pen2 = QtGui.QPen()
            black_pen2.setColor(QtGui.QColor(0, 0, 0))
            black_pen2.setWidth(2)
            colored_pen = QtGui.QPen()
            colored_pen.setColor(path_color)
            colored_pen.setWidth(2)
            colored_brush = QtGui.QBrush()
            colored_brush.setColor(path_color)
            colored_brush.setStyle(QtCore.Qt.SolidPattern)

            for check_item in self._paths_data[paths]["Data"]:
                if check_item not in self._data.get_data():
                    check_index = self._paths_data[paths]["Data"].index(check_item)
                    del self._paths_data[paths]["Data"][check_index]

            for i in range(0, len(self._paths_data[paths]["Data"])-1):
                from_link = self._paths_data[paths]["Data"][i]
                to_link = self._paths_data[paths]["Data"][i+1]
                # if (from_link in self._data.get_data()) and (to_link in self._data.get_data()):
                from_item = None
                to_item = None
                for scene_items in self._scene.items():
                    if scene_items.data(1)[:6] == from_link:
                        from_item = scene_items
                    elif scene_items.data(1)[:6] == to_link:
                        to_item = scene_items

                from_point = QtCore.QPointF(
                    self._map_data["Coordinates"][from_item.data(1)[:6]][0] + (from_item.data(4).width()) / 2,
                    self._map_data["Coordinates"][from_item.data(1)[:6]][1] + from_item.data(4).height())
                to_point = QtCore.QPointF(
                    self._map_data["Coordinates"][to_item.data(1)[:6]][0] + (to_item.data(4).width()) / 2,
                    self._map_data["Coordinates"][to_item.data(1)[:6]][1] + to_item.data(4).height())

                to_line = QtCore.QLineF(from_point, to_point)
                angle = np.arctan2(-to_line.dy(), to_line.dx())
                arrow_head_size = 15
                # to_head1 = QtCore.QPointF
                to_head2 = QtCore.QPointF(to_point.x() - arrow_head_size * np.sin(angle + np.pi / 3),
                                          to_point.y() - arrow_head_size * np.cos(angle + np.pi / 3))
                to_head3 = QtCore.QPointF(to_point.x() - arrow_head_size * np.sin(angle + np.pi - (np.pi / 3)),
                                          to_point.y() - arrow_head_size * np.cos(angle + np.pi - (np.pi / 3)))

                # print("triangle points: ", [to_point, to_head1, to_head2])
                head_triangle = QtGui.QPolygonF([to_point, to_head2, to_head3])

                overlay_painter.setPen(black_pen5)
                overlay_painter.drawLine(to_line)
                overlay_painter.setBrush(colored_brush)
                overlay_painter.setPen(black_pen2)
                overlay_painter.drawPolygon(head_triangle)
                overlay_painter.drawEllipse(from_point, 5, 5)
                overlay_painter.setPen(colored_pen)
                overlay_painter.drawLine(from_point, to_point)
                # print("{} to {} drawn".format(from_item.data(1), to_item.data(1)))

                # elif (from_link not in self._data.get_data()) and (to_link in self._data.get_data()):
                #     del self._paths_data[paths]["Data"][i]
                #     i -= 1
                #     continue
                #
                # elif (from_link in self._data.get_data()) and (to_link not in self._data.get_data()):
                #
                #     del self._paths_data[paths]["Data"][i + 1]
                #     i -= 1
                #     continue
                #
                # elif (from_link not in self._data.get_data()) and (to_link not in self._data.get_data()):
                #     del self._paths_data[paths]["Data"][i]
                #     del self._paths_data[paths]["Data"][i + 1]
                #     i -= 1
                #     continue

            path_overlay_item = QtWidgets.QGraphicsPixmapItem(blank_overlay_image)
            path_overlay_item.setData(1, "Path Overlay")
            path_overlay_item.setData(2, 1)
            path_overlay_item.setScale(self._zoom_factor)
            path_overlay_item.setZValue(-1)
            self._scene.removeItem(self._paths_overlay_items[paths])

            self._scene.addItem(path_overlay_item)
            if self._paths_overlay_items[paths].isVisible():
                path_overlay_item.setVisible(True)
                self._paths_overlay_items[paths] = path_overlay_item
            else:
                path_overlay_item.setVisible(False)
                self._paths_overlay_items[paths] = path_overlay_item

            overlay_painter.end()
