import os
import numpy as np
import calendar
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

path = os.path.dirname(os.path.abspath(__file__))
CalendarMapWindowUI, CalendarMapWindowBase = uic.loadUiType(os.path.join(path, 'calendarmapwindow.ui'))

class CalendarMapWindow(CalendarMapWindowBase, CalendarMapWindowUI):
    # def __init__(self, parent=None):
    def __init__(self, data, map_data, paths_data, filters, data_file, recycler, cal_ids, current_path_name, parent=None):
    # def __init__(self, data, filters, data_file, parent=None):
        CalendarMapWindowBase.__init__(self, parent)
        self.setupUi(self)
        self._data = data
        self._filters = filters
        self._recycler = recycler
        self._data_file = data_file
        self._calID_dict = cal_ids
        self._zoom_factor = 1.0
        self._map_data = map_data
        self._paths_data = paths_data
        self._paths_overlay_items = dict()
        self._paths_visibilities = dict()
        self._current_path_name = current_path_name

        self._date_buckets = dict()
        self.Fill_Date_Buckets()
        self.Set_Max_Daterange()

        self._months_dict = dict()
        self._icon_items_dict = dict()
        self._months_strings = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                                "October", "November", "December"]

        self.doubleSpinBox.setValue(0.5)
        self._icon_base_scale = self.doubleSpinBox.value()
        self._pen_width = 3
        self._grid_pen = QtGui.QPen()
        self._grid_pen.setColor(QtGui.QColor(0, 0, 0))
        self._grid_pen.setWidth(self._pen_width)
        self._grid_pen_grey = QtGui.QPen()
        self._grid_pen_grey.setColor(QtGui.QColor(211, 211, 211))
        self._grid_pen_grey.setWidth(self._pen_width)
        self._month_title_x = self.spinBox_5.value()
        self._month_title_y = self.spinBox_6.value()
        self._date_box_x = self.spinBox_3.value()
        self._date_box_y = self.spinBox_4.value()
        self._cell_width = self.spinBox.value()
        self._cell_height = self.spinBox_2.value()
        self._buffer_height = self.spinBox_9.value()
        self._title_font = self.fontComboBox_2.currentFont()
        self._title_font.setPointSize(self.spinBox_8.value())
        self._date_font = self.fontComboBox.currentFont()
        self._date_font.setPointSize(self.spinBox_7.value())

        self._scene_width = self._cell_width*7
        self._scene_height = self.sum_current_grid_heights()

        self._classes_dir = os.getcwd()
        self._maps_dir = os.path.join(self._classes_dir, "MapResources")
        # self._icons_dir = os.path.join(self._maps_dir, "MapIcons")
        self._icons_components_dir = os.path.join(self._maps_dir, "MapComponents")

        self._scene = QtWidgets.QGraphicsScene()
        self._arrow_overlay_item = QtWidgets.QGraphicsPixmapItem()
        self._arrow_overlay_on = False
        self.graphicsView.setScene(self._scene)

        for keys in self._paths_data:
            self._paths_overlay_items[keys] = QtWidgets.QGraphicsPixmapItem()
            self._paths_overlay_items[keys].setVisible(False)
            self._paths_visibilities[keys] = self._paths_overlay_items[keys].isVisible()
            # self._scene.addItem(self._paths_overlay_items[keys])

        test_item_number = self._data.get_printables()[0]
        temp_dict = self._data.get_item(test_item_number)
        file_nums = test_item_number[:2]
        file_class = temp_dict["classification"]
        file_name = file_nums + file_class + ".png"
        # icon_path = os.path.join(self._icons_dir, file_name)
        # temp_icon_item = MapIcon(0, icon_path, None, self._scene)
        temp_icon_item = MapIcon(0, file_name, self._icons_components_dir, None, self._scene)
        self._icon_width = temp_icon_item.boundingRect().width()
        self._icon_height = temp_icon_item.boundingRect().height()
        self._icon_offset = 3*(self._icon_width*self._icon_base_scale)/4


        self.pushButton_2.clicked.connect(self.close)
        # self.pushButton_8.clicked.connect(self.Apply_Layout_Changes)

        self.dateEdit.editingFinished.connect(self.Apply_Layout_Changes)
        self.dateEdit_2.editingFinished.connect(self.Apply_Layout_Changes)
        self.doubleSpinBox.editingFinished.connect(self.Apply_Layout_Changes)
        self.spinBox_5.editingFinished.connect(self.Apply_Layout_Changes)
        self.spinBox_6.editingFinished.connect(self.Apply_Layout_Changes)
        self.spinBox_3.editingFinished.connect(self.Apply_Layout_Changes)
        self.spinBox_4.editingFinished.connect(self.Apply_Layout_Changes)
        self.spinBox.editingFinished.connect(self.Apply_Layout_Changes)
        self.spinBox_2.editingFinished.connect(self.Apply_Layout_Changes)
        self.spinBox_9.editingFinished.connect(self.Apply_Layout_Changes)
        self.fontComboBox_2.currentFontChanged.connect(self.Apply_Layout_Changes)
        self.spinBox_8.editingFinished.connect(self.Apply_Layout_Changes)
        self.fontComboBox.currentFontChanged.connect(self.Apply_Layout_Changes)
        self.spinBox_7.editingFinished.connect(self.Apply_Layout_Changes)

        self.actionClear_Selected.triggered.connect(self.Clear_Selections)
        self.actionToggle_Arrows.triggered.connect(self.Toggle_Arrows)
        self.actionClear_Links.triggered.connect(self.Clear_Links)
        self.actionFilter_Settings.triggered.connect(self.Filter_Settings_Triggered)
        self.actionLink_Selected.triggered.connect(self.Link_Selected)
        self.actionDelink_Selected.triggered.connect(self.DeLink_Selected)
        self.actionClear_Links.triggered.connect(self.Clear_Links)
        self.actionEdit_Item.triggered.connect(self.Edit_Item_Triggered)
        # self.actionAdd_Item.triggered.connect(self.Add_Item_Triggered)
        self.actionDelete_Selected.triggered.connect(self.Delete_Selected)
        self.actionDuplicate_Item.triggered.connect(self.Duplicate_Selected_Triggered)
        self.actionSnap_Date.triggered.connect(self.snap_to_date)

        self.actionSave_Exit.triggered.connect(self.Save_Exit)
        self.actionFull_Save.triggered.connect(self.Full_Save)
        self.actionNew_Path.triggered.connect(self.New_Path)
        self.actionPath_Settings.triggered.connect(self.Path_Settings_Triggered)
        self.actionEdit_Current_Path.triggered.connect(self.Edit_Current_Path_Triggered)

        # print("first rendering")
        self.Refresh_Triggered()

    def Full_Save(self):
        self._data_file.file_DataSave(self._data.get_data())

    def Save_Exit(self):
        self.pushButton.click()

    def Set_Layout_To_Fit(self):
        pass

    def Apply_Layout_Changes(self):
        self._start_date = date(self.dateEdit.date().year(), self.dateEdit.date().month(), self.dateEdit.date().day())
        self._end_date = date(self.dateEdit_2.date().year(), self.dateEdit_2.date().month(), self.dateEdit_2.date().day())
        self._icon_base_scale = self.doubleSpinBox.value()
        self._month_title_x = self.spinBox_5.value()
        self._month_title_y = self.spinBox_6.value()
        self._date_box_x = self.spinBox_3.value()
        self._date_box_y = self.spinBox_4.value()
        self._cell_width = self.spinBox.value()
        self._cell_height = self.spinBox_2.value()
        self._buffer_height = self.spinBox_9.value()
        self._title_font = self.fontComboBox_2.currentFont()
        self._title_font.setPointSize(self.spinBox_8.value())
        self._date_font = self.fontComboBox.currentFont()
        self._date_font.setPointSize(self.spinBox_7.value())
        self._icon_offset = 3*(self._icon_width*self._icon_base_scale)/4

        self.Refresh_Triggered()

    def Set_Max_Daterange(self):
        days_list = list(self._date_buckets.keys())
        dates_list = list()
        for days in days_list:
            day_split = days.split('-')
            day_date = date(int(day_split[0]), int(day_split[1]), int(day_split[2]))
            dates_list.append(day_date)
        dates_list = sorted(dates_list)

        self._start_date = dates_list[0]
        self._end_date = dates_list[-1]
        start_date = QtCore.QDate(self._start_date.year, self._start_date.month, self._start_date.day)
        self.dateEdit.setDate(start_date)
        end_date = QtCore.QDate(self._end_date.year, self._end_date.month, self._end_date.day)
        self.dateEdit_2.setDate(end_date)

    def Fill_Date_Buckets(self):
        self._date_buckets = dict()
        for items in self._data.get_data():
            temp_dict = self._data.get_item(items)
            # date_list = temp_dict["due date"].split('-')
            # due = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
            if temp_dict["due date"] in self._date_buckets:
                self._date_buckets[temp_dict["due date"]].append(temp_dict["title"])
            else:
                self._date_buckets[temp_dict["due date"]] = list()
                self._date_buckets[temp_dict["due date"]].append(temp_dict["title"])

    def Render_Items(self):
        # print(self._date_buckets)
        self._data.set_printables()
        for days in self._date_buckets:
            days_list = days.split("-")
            due = date(int(days_list[0]), int(days_list[1]), int(days_list[2]))
            if (due < self._start_date) or (due > self._end_date):
                continue
            else:
                # print("Rendering all items for day: {}".format(days))
                items_list = self._date_buckets[days]
                horizontal_spacing = 0
                vertical_spacing = 0
                overlap_index = 0
                cell_coords = self.date_to_coords_absolute(days)
                for items in items_list:
                    if items[:6] in self._data.get_printables():
                        position_x = cell_coords[0] + horizontal_spacing
                        position_y = cell_coords[1] + vertical_spacing
                        # print("initial coords({}, {})".format(position_x, position_y))

                        if (position_x + self._icon_width*self._icon_base_scale > cell_coords[0] + self._cell_width) or \
                                ((position_x + self._icon_width*self._icon_base_scale > (cell_coords[0] + self._cell_width)-self._date_box_x)
                                 and (position_y < cell_coords[1] + self._date_box_y)):
                            #new line trigger
                            horizontal_spacing = 0
                            vertical_spacing += self._icon_height*self._icon_base_scale
                            position_x = cell_coords[0] + horizontal_spacing
                            position_y = cell_coords[1] + vertical_spacing

                        if position_y + self._icon_height*self._icon_base_scale > cell_coords[1] + self._cell_height:
                            overlap_index += 1
                            horizontal_spacing = overlap_index*self._icon_offset
                            vertical_spacing = 0
                            position_x = cell_coords[0] + horizontal_spacing
                            position_y = cell_coords[1] + vertical_spacing
                            # diff = (cell_coords[1] + self._cell_height) - (position_y + self._icon_height*self._icon_base_scale)
                            # position_y -= diff

                        # print("final coords ({}, {})".format(position_x, position_y))

                        number = items[:6]
                        # print(number)
                        # print("Preparing to render {} icon at ({}, {})".format(items["title"], position_x, position_y))
                        self.Render_Icon(number, position_x, position_y)
                        horizontal_spacing += self._icon_offset

    def Render_Icon(self, obs, pos_x, pos_y):
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
        # icon_path = os.path.join(self._icons_dir, file_name)
        # map_icon_item = MapIcon(0, icon_path, None, self._scene)
        map_icon_item = MapIcon(0, file_name, self._icons_components_dir, None, self._scene)
        map_icon_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        map_icon_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        map_icon_item.setScale(self._icon_base_scale)
        map_icon_item.setPos(pos_x, pos_y)
        map_icon_item.setData(1, temp_dict["title"])
        map_icon_item.setData(2, self._icon_base_scale)
        map_icon_item.setData(3, map_icon_item.pos())
        map_icon_item.setData(4, map_icon_item.sceneBoundingRect())
        map_icon_item.setToolTip("{} \nSet for {}".format(temp_dict["title"], temp_dict["due date"]))
        if temp_dict["completed"]:
            map_icon_item.setScale(self._icon_base_scale*.5)
            map_icon_item.setData(2, self._icon_base_scale*.5)
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

    def sum_current_grid_heights(self):
        total_month_heights = 0
        for keys in self._months_dict:
            total_month_heights += self._months_dict[keys].data(3)
        return total_month_heights

    def date_to_cell(self, due_date):
        date_list = due_date.split('-')
        due = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        due_column = ((due.weekday()) + 1)%7
        month_origin = ((date(due.year, due.month, 1).weekday())+1) % 7
        due_row = ((due.day-(due_column+1))+month_origin)//7
        # print("Date {} is located in cell ({}, {})".format(due_date, due_row, due_column))
        return [due_row, due_column]

    def date_to_coords_absolute(self, due_date):
        due_cell_coords = self.date_to_cell(due_date)
        date_list = due_date.split('-')
        due = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        month_string = self._months_strings[due.month-1]
        grid_item = self._months_dict["{} {}".format(month_string, due.year)]
        grid_item_depth = grid_item.data(4)
        due_cell_absolute_x = grid_item.pos().x() + (self._cell_width * due_cell_coords[1])
        due_cell_absolute_y = grid_item.pos().y() + self._month_title_y + (self._cell_height * due_cell_coords[0])
        # print("Date {} is located at coords ({}, {})".format(due_date, due_cell_absolute_x, due_cell_absolute_y))
        return [due_cell_absolute_x, due_cell_absolute_y]

    def cell_to_date(self, month, year, rows, row, column):
        month_origin = ((date(year, month, 1).weekday())+1) % 7

        max_row = rows - 1
        month_max_date = calendar.monthrange(year, month)[1]
        month_max_index = ((date(year, month, month_max_date).weekday())+1) % 7

        if (row == max_row) and (column > month_max_index):
            diff = column - month_max_index
            if month == 12:
                new_month = 1
                new_year = year + 1
            else:
                new_month = month + 1
                new_year = year
            day = diff
        elif (row == 0) and (column < month_origin):
            diff = month_origin - column
            if month == 1:
                new_month = 12
                new_year = year - 1
            else:
                new_month = month - 1
                new_year = year
            new_month_max_date = calendar.monthrange(new_year, new_month)[1]
            day = (new_month_max_date - diff) + 1
        else:
            day = (7*row) + (column+1) - month_origin
            new_month = month
            new_year = year

        return date(new_year, new_month, day)

    def calculate_month_rows(self, month, year):
        month_origin = ((date(year, month, 1).weekday())+1) % 7

        month_max_date = calendar.monthrange(year, month)[1]
        month_max_index = ((date(year, month, month_max_date).weekday())+1) % 7

        max_row = ((month_max_date-(month_max_index + 1))+month_origin)//7
        # print("{} = (({}-({}+1))+{})//7".format(max_row, month_max_date, month_max_index, month_origin))
        row_count = max_row + 1
        return row_count

    def draw_grid(self, month_grid, rows):
        grid_painter = QtGui.QPainter(month_grid)
        grid_painter.setPen(self._grid_pen)
        horizontal_count = rows + 1
        vertical_count = 8
        for i in range(0, horizontal_count):
            grid_painter.drawLine(QtCore.QPoint(0, (i*self._cell_height)+self._month_title_y),
                                  QtCore.QPoint(7*self._cell_width, (i*self._cell_height)+self._month_title_y))

        for j in range(0, vertical_count):
            grid_painter.drawLine(QtCore.QPoint(j*self._cell_width, self._month_title_y),
                                  QtCore.QPoint(j*self._cell_width, rows*self._cell_height+self._month_title_y))

        grid_painter.end()

    def draw_title_box(self, month_grid, title):
        title_box_painter = QtGui.QPainter(month_grid)
        title_box_painter.setPen(self._grid_pen)
        title_box_painter.setFont(self._title_font)
        title_box_painter.drawRect(0, 0, self._month_title_x, self._month_title_y)
        title_box_painter.drawText(QtCore.QRect(0, 0, self._month_title_x, self._month_title_y), QtCore.Qt.AlignCenter,
                                   title)
        title_box_painter.end()

    def draw_date_boxes(self, month, year, rows, month_grid):
        date_box_painter = QtGui.QPainter(month_grid)
        date_box_painter.setFont(self._date_font)
        max_rows = rows
        for i in range(0, max_rows):
            for j in range(0, 7):
                check_date = self.cell_to_date(month, year, max_rows, i, j)
                # print("cell ({}, {}) of month {} is day {}".format(i, j, check_date.month, check_date.day))
                if check_date.month != month:
                    date_box_painter.setPen(self._grid_pen_grey)
                else:
                    date_box_painter.setPen(self._grid_pen)

                start_box_x = j*self._cell_width + (self._cell_width - self._date_box_x)
                start_box_y = i*self._cell_height + self._month_title_y
                date_box_painter.drawRect(start_box_x, start_box_y, self._date_box_x, self._date_box_y)
                date_box_painter.drawText(QtCore.QRect(start_box_x, start_box_y, self._date_box_x, self._date_box_y), QtCore.Qt.AlignCenter, str(check_date.day))
        date_box_painter.end()

    def draw_month_grid(self, month, year):
        month_string = self._months_strings[month-1]
        month_columns = 7
        month_rows = self.calculate_month_rows(month, year)
        cell_size_x = self._cell_width
        cell_size_y = self._cell_height
        month_title_y = self._month_title_y
        grid_size_x = cell_size_x*month_columns
        grid_size_y = cell_size_y*month_rows
        month_pixmap = QtGui.QPixmap(grid_size_x, month_title_y+grid_size_y+self._buffer_height)
        month_pixmap.fill(QtGui.QColor(255, 255, 255))
        self.draw_date_boxes(month, year, month_rows, month_pixmap)
        self.draw_grid(month_pixmap, month_rows)
        self.draw_title_box(month_pixmap, "{} {}".format(month_string, year))
        month_grid_item = QtWidgets.QGraphicsPixmapItem(month_pixmap)
        self._scene.addItem(month_grid_item)
        month_index = len(self._months_dict)
        month_grid_item.setData(1, month_index)
        month_grid_item.setData(2, "{} {}".format(month_string, year))
        month_grid_item.setData(3,  month_title_y+grid_size_y+self._buffer_height)
        month_grid_item.setZValue(-3)
        grids_sum_y = self.sum_current_grid_heights()
        month_grid_item.setPos(0, grids_sum_y)
        month_grid_item.setData(4, grids_sum_y)
        self._months_dict["{} {}".format(month_string, year)] = month_grid_item

    def Render_Calendar(self):
        temp_date = self._start_date
        # temp_date.day = 1
        while (self._end_date-temp_date).days > -1:
            year = temp_date.year
            month = temp_date.month
            self.draw_month_grid(month, year)
            # print("{} {} grid drawn".format(month, year))
            if month < 12:
                month += 1
            else:
                month = 1
                year += 1
            temp_date = date(year, month, 1)
        self.Update_Scene()

    def Update_Scene(self):
        self._scene_width = self._cell_width*7
        self._scene_height = self.sum_current_grid_heights()
        self._scene.setSceneRect(QtCore.QRectF(0.0, 0.0, self._scene_width, self._scene_height))
        self.graphicsView.viewport().update()

    def Refresh_Triggered(self):
        self._data.set_printables()
        # printables_list = list(self._data.get_printables())
        self._months_dict = dict()
        self._icon_items_dict = dict()
        self._scene.clear()

        self.Render_Calendar()
        self.Render_Items()
        # print("preparing to refresh arrows")
        self.Render_Arrows()
        # print("preparing to refresh paths")
        self.Render_Paths()
        # self.Render_Paths()

    def Clear_Selections(self):
        for numbers in self._icon_items_dict.keys():
            item = self._icon_items_dict[numbers]
            item.setSelected(False)
            item.setZValue(0.0)

    def get_data(self):
        return self._data

    def get_filters(self):
        return self._filters

    def get_paths(self):
        return self._paths_data

    def get_map(self):
        return self._map_data

    def Filter_Settings_Triggered(self):
        print_font = self._date_font
        self.filter_settings = FilterSettings(self._data, self._filters, self._calID_dict, print_font)
        self.filter_settings.setWindowTitle("Filter Settings")
        self.filter_settings.pushButton.clicked.connect(self.Filter_Settings_ConfirmButton_Clicked)
        self.filter_settings.show()

    def Filter_Settings_ConfirmButton_Clicked(self):
        self.filter_settings.ApplyChanges()
        self._filters = self.filter_settings.get_filters()
        self._data.main_filter(self._filters)
        self.filter_settings.close()
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
        blank_overlay_dimensions = QtCore.QRectF(0.0, 0.0, self._scene_width, self._scene_height)
        blank_overlay_image = QtGui.QPixmap(int(blank_overlay_dimensions.width()), int(blank_overlay_dimensions.height()))
        blank_overlay_image.fill(QtGui.QColor("transparent"))
        overlay_painter = QtGui.QPainter(blank_overlay_image)
        black_pen5 = QtGui.QPen()
        black_pen5.setColor(QtGui.QColor(0, 0, 0))
        black_pen5.setWidth(3)
        black_pen2 = QtGui.QPen()
        black_pen2.setColor(QtGui.QColor(0, 0, 0))
        black_pen2.setWidth(1)
        white_pen = QtGui.QPen()
        white_pen.setColor(QtGui.QColor(255, 255, 255))
        white_pen.setWidth(1)
        white_brush = QtGui.QBrush()
        white_brush.setColor(QtGui.QColor(255, 255, 255))
        white_brush.setStyle(QtCore.Qt.SolidPattern)

        printables_list = self._data.get_printables()
        for items in printables_list:
            to_links = self._data.get_item(items)["to-links"]
            for link in to_links:

                if link[:6] in printables_list:
                    if (link[:6] in self._icon_items_dict) and (items in self._icon_items_dict):
                        # print("from {} to {}".format(items, link[:6]))
                        from_item = None
                        to_item = None
                        for keys in self._icon_items_dict.keys():
                            if self._icon_items_dict[keys].data(1)[:6] == items:
                                from_item = self._icon_items_dict[keys]
                            elif self._icon_items_dict[keys].data(1)[:6] == link[:6]:
                                to_item = self._icon_items_dict[keys]

                        # print("drawing {} to {}".format(from_item.data(1), to_item.data(1)))
                        from_point = QtCore.QPointF(from_item.pos().x()+(from_item.sceneBoundingRect().width())/2, from_item.pos().y()+from_item.sceneBoundingRect().height())
                        to_point = QtCore.QPointF(to_item.pos().x()+(to_item.sceneBoundingRect().width())/2, to_item.pos().y()+to_item.sceneBoundingRect().height())
                        # print("({}, {})".format(from_point, to_point))

                        to_line = QtCore.QLineF(from_point, to_point)
                        angle = np.arctan2(-to_line.dy(), to_line.dx())
                        arrow_head_size = 10
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
                        overlay_painter.drawEllipse(from_point, 3, 3)
                        overlay_painter.setPen(white_pen)
                        overlay_painter.drawLine(from_point, to_point)
                        # print("{} to {} drawn".format(from_item.data(1), to_item.data(1)))

        if self._arrow_overlay_item in self._scene.items():
            self._scene.removeItem(self._arrow_overlay_item)
        self._arrow_overlay_item = QtWidgets.QGraphicsPixmapItem(blank_overlay_image)
        self._arrow_overlay_item.setData(1, "Arrows Overlay")
        self._arrow_overlay_item.setData(2, 1)
        self._arrow_overlay_item.setScale(1)
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

    def pos_to_month(self, x_pos, y_pos):
        temp_date = self._start_date
        while (self._end_date-temp_date).days > -1:
            year = temp_date.year
            month = temp_date.month
            month_string = self._months_strings[month - 1]
            current_month_start_y = self._months_dict["{} {}".format(month_string, year)].pos().y()
            # print("{}: {} < {}".format(month_string, y_pos, current_month_start_y))
            if y_pos < current_month_start_y:
                if month == 1:
                    current_month = 12
                    current_year = year-1
                    return date(current_year, current_month, 1)
                else:
                    current_month = month-1
                    current_year = year
                    return date(current_year, current_month, 1)
            else:
                if month < 12:
                    month += 1
                else:
                    month = 1
                    year += 1
                temp_date = date(year, month, 1)

    def pos_to_day(self, x_pos, y_pos, month_grid):
        month_rows = self.calculate_month_rows(month_grid.month, month_grid.year)
        current_column = -1
        current_row = -1
        month_string = self._months_strings[month_grid.month - 1]
        current_month_start_y = self._months_dict["{} {}".format(month_string, month_grid.year)].pos().y()
        # print(current_month_start_y)
        # print(self._months_strings[month_grid.month-1], month_rows)
        for i in range(1, 8):
            # print("x {}: {} < {}".format(i, x_pos, i*self._cell_width))
            if x_pos < i*self._cell_width:
                current_column = i-1
                break
        for j in range(1, month_rows+1):
            # print("y {}: {} < {}".format(j, y_pos, current_month_start_y + self._month_title_y + j*self._cell_height))
            if y_pos < current_month_start_y + self._month_title_y + j*self._cell_height:
                current_row = j-1
                break

        # print("({}, {})".format(current_column, current_row))
        current_date = self.cell_to_date(month_grid.month, month_grid.year, month_rows, current_row, current_column)
        # print(current_date)
        return current_date

    def pos_in_grid(self, x_pos, y_pos, month_grid):
        month_string = self._months_strings[month_grid.month - 1]
        month_row_count = self.calculate_month_rows(month_grid.month, month_grid.year)
        current_month_start_y = self._months_dict["{} {}".format(month_string, month_grid.year)].pos().y()
        if (y_pos < (current_month_start_y + self._month_title_y)) or (y_pos > current_month_start_y +self._cell_height*month_row_count):
            return False
        else:
            return True

    def pos_to_date(self, selected_item, old_date):
        current_pos = selected_item.pos()
        # print(current_pos)
        current_grid = self.pos_to_month(current_pos.x(), current_pos.y())
        # print(current_grid)

        if self.pos_in_grid(current_pos.x(), current_pos.y(), current_grid):
            current_date = self.pos_to_day(current_pos.x(), current_pos.y(), current_grid)
            # print("New Date: ", current_date)
            # print("True")
            return current_date
        else:
            # print("False")
            old_list = old_date.split('-')
            old_due_date = date(int(old_list[0]), int(old_list[1]), int(old_list[1]))
            return old_due_date

    def snap_to_date(self):
        for items in self._scene.selectedItems():
            selected_number = items.data(1)[:6]
            selected_item_dict = self._data.get_item(selected_number)
            new_due_date = self.pos_to_date(items, selected_item_dict["due date"])
            selected_item_dict["due date"] = "{:04d}-{:02d}-{:02d}".format(new_due_date.year, new_due_date.month, new_due_date.day)
            self._data.set_item(selected_number, selected_item_dict)
        self.Fill_Date_Buckets()
        self.Refresh_Triggered()

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
        selected_item_pos = selected_items[0].pos()
        old_item_num = selected_items[0].data(1)[:6]
        if temp_num != old_item_num:
            # old item has been REPLACED. deleter references to old Item
            self._data.remove_item(old_item_num)
            del self._map_data["Coordinates"][old_item_num]

        if temp_num not in self._map_data["Coordinates"]:
            pos_list = [selected_item_pos.x(), selected_item_pos.y()]
            self._map_data["Coordinates"][temp_num] = pos_list

        self._data.set_item(temp_num, temp_data)
        self._data.reset_links()

        self.item_editor.close()
        self.Fill_Date_Buckets()
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

            pos_list = [items.pos().x()+10.0, items.pos().y()]
            self._map_data["Coordinates"][new_item_number] = pos_list
            # render duplicate item offset from map_data["coordinates"]["item_number"]

            self._filters["manual"].append(new_item_number)
        self.Fill_Date_Buckets()
        self.Refresh_Triggered()

    def Delete_Selected(self):
        recycle_dict = dict()
        if len(self._scene.selectedItems()) > 0:
            for items in self._scene.selectedItems():
                if items.data(1)[:6] in self._data.get_arrangement():
                    print("deleting ", items.data(1)[:6])
                    recycle_dict[items.data(1)[:6]] = self._data.remove_item(items.data(1)[:6])
                    # self._data.remove_item(items.data(1)[:6])
                    del self._icon_items_dict[items.data(1)[:6]]
                    del self._map_data["Coordinates"][items.data(1)[:6]]
                    self._scene.removeItem(items)

                    # del self._map_data["Coordinates"][items.data(1)[:6]]
        self._recycler.file_Recycle(recycle_dict)
        self.Fill_Date_Buckets()
        self.Refresh_Triggered()

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

    def Path_Settings_Triggered(self):
        self.path_settings_window = PathSettings(self._data, self._paths_data, self._paths_overlay_items, self._current_path_name)
        self.path_settings_window.setWindowTitle("Path Settings")
        self.path_settings_window.pushButton.clicked.connect(self.Path_Settings_ConfirmButton_Clicked)
        self.path_settings_window.show()

    def Path_Settings_ConfirmButton_Clicked(self):
        self._paths_data = self.path_settings_window.get_paths_data()
        self._paths_overlay_items = self.path_settings_window.get_paths_overlay()
        for keys in self._paths_overlay_items:
            self._paths_visibilities[keys] = self._paths_overlay_items[keys].isVisible()
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
            blank_overlay_dimensions = QtCore.QRectF(0.0, 0.0, self._scene_width, self._scene_height)
            blank_overlay_image = QtGui.QPixmap(int(blank_overlay_dimensions.width()),
                                                int(blank_overlay_dimensions.height()))
            blank_overlay_image.fill(QtGui.QColor("transparent"))
            overlay_painter = QtGui.QPainter(blank_overlay_image)
            path_color = QtGui.QColor(self._paths_data[paths]["Color"][0], self._paths_data[paths]["Color"][1],
                                      self._paths_data[paths]["Color"][2])
            black_pen5 = QtGui.QPen()
            black_pen5.setColor(QtGui.QColor(0, 0, 0))
            black_pen5.setWidth(3)
            black_pen2 = QtGui.QPen()
            black_pen2.setColor(QtGui.QColor(0, 0, 0))
            black_pen2.setWidth(1)
            colored_pen = QtGui.QPen()
            colored_pen.setColor(path_color)
            colored_pen.setWidth(1)
            colored_brush = QtGui.QBrush()
            colored_brush.setColor(path_color)
            colored_brush.setStyle(QtCore.Qt.SolidPattern)


            for check_item in self._paths_data[paths]["Data"]:
                if check_item not in self._data.get_data():
                    check_index = self._paths_data[paths]["Data"].index(check_item)
                    del self._paths_data[paths]["Data"][check_index]

            # print(len(self._paths_data[paths]["Data"]))
            for i in range(0, len(self._paths_data[paths]["Data"])-1):
                j = 1
                while i+j < len(self._paths_data[paths]["Data"]):
                    # print("i < {}, i+j < {}, i == {}, j == {}, i+j == {}".format(len(self._paths_data[paths]["Data"]) - 1, len(self._paths_data[paths]["Data"]), i, j, i + j))

                    from_link = self._paths_data[paths]["Data"][i]
                    to_link = self._paths_data[paths]["Data"][i + j]
                    if from_link not in self._icon_items_dict.keys():
                        # print("from item {} not in icon items".format(from_link))
                        break
                    elif to_link not in self._icon_items_dict.keys():
                        # print("to item {} not in icon items".format(to_link))
                        j += 1
                        continue
                    else:
                        from_item = None
                        to_item = None

                        # print("looking for {} to {}".format(from_link, to_link))

                        for keys in self._icon_items_dict.keys():
                            if self._icon_items_dict[keys].data(1)[:6] == from_link:
                                from_item = self._icon_items_dict[keys]
                            elif self._icon_items_dict[keys].data(1)[:6] == to_link:
                                to_item = self._icon_items_dict[keys]

                        # print("drawing {} to {}".format(from_item.data(1), to_item.data(1)))
                        from_point = QtCore.QPointF(from_item.pos().x() + (from_item.sceneBoundingRect().width()) / 2,
                                                    from_item.pos().y() + from_item.sceneBoundingRect().height())
                        to_point = QtCore.QPointF(to_item.pos().x() + (to_item.sceneBoundingRect().width()) / 2,
                                                  to_item.pos().y() + to_item.sceneBoundingRect().height())
                        # print("({}, {})".format(from_point, to_point))

                        to_line = QtCore.QLineF(from_point, to_point)
                        angle = np.arctan2(-to_line.dy(), to_line.dx())
                        arrow_head_size = 10
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
                        overlay_painter.drawEllipse(from_point, 3, 3)
                        overlay_painter.setPen(colored_pen)
                        overlay_painter.drawLine(from_point, to_point)
                        break
                        # print("drawn {} to {}".format(from_item.data(1), to_item.data(1)))
                        # print("{}: {} -> {} ".format(len(self._paths_data[paths]["Data"])-1, i, i+1))


            # print("prepping overlay item")
            # print(blank_overlay_image)
            path_overlay_item = QtWidgets.QGraphicsPixmapItem(blank_overlay_image)
            path_overlay_item.setData(1, "Path Overlay")
            path_overlay_item.setData(2, 1)
            path_overlay_item.setScale(1)
            path_overlay_item.setZValue(-1)

            # print("preparing to remove old item  from scene")
            # print(self._paths_overlay_items)
            # if self._paths_overlay_items[paths] in self._scene.items():
            #     self._scene.removeItem(self._paths_overlay_items[paths])
            #     print("{} item removed from scene".format(paths))


            if self._paths_visibilities[paths]:
                path_overlay_item.setVisible(True)
                self._paths_overlay_items[paths] = path_overlay_item
            else:
                path_overlay_item.setVisible(False)
                self._paths_overlay_items[paths] = path_overlay_item
            # print("adding new item to scene")
            self._scene.addItem(path_overlay_item)
            overlay_painter.end()

