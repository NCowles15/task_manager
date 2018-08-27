# from ClassResources.Edit_Data import Edit_Data
# from ClassResources.Task_Data import Task_Data
# from ClassResources.Send_Calendar import Send_Calendar

from GUIResources.CheckableListClass import CheckableList
# from GUIResources.EditableListClass import EditableList
from GUIResources.FilterSettingsClass import FilterSettings
from GUIResources.ItemEditorClass import ItemEditor
from GUIResources.JsonFileDialogClass import JsonFileDialog
from GUIResources.OpenFileDialogClass import OpenFileDialog
from GUIResources.PickListClass import PickList
from GUIResources.PrinterSettingsClass import PrinterSettings
from GUIResources.TextFileDialogClass import TextFileDialog
from GUIResources.OpenTextDialogClass import OpenTextDialog
from GUIResources.MapMainWindowClass import MapMainWindow


# from ClassResources.Send_Wunderlist import Send_Wunderlist
from ClassResources.Task_Data import Task_Data
from ClassResources.File_Handler import File_Handler
from ClassResources.Send_Printer import Send_Printer
from ClassResources.Validifiers import validate

# from MapFiles.MapMainWindowClass import MapMainWindow

# import sys
import os
# from os import listdir
# from os.path import isfile, join

from PyQt5 import uic
# from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtGui, QtWidgets, QtCore


# get the directory of this script
path = os.path.dirname(os.path.abspath(__file__))

MainWindowUI, MainWindowBase = uic.loadUiType(os.path.join(path, 'mainwindow.ui'))


class MainWindow(MainWindowBase, MainWindowUI):
    def __init__(self, parent=None):
        MainWindowBase.__init__(self, parent)
        self._data_file = File_Handler()
        self._all_data = Task_Data(dict())
        self._temp_item = dict()
        self._printer = Send_Printer()
        self._settings = dict()
        self._user_file = File_Handler()

        # temp = {"sort": "none", "fields": [], "filters": {"mode": "manual", "manual": [], "exclusive": {"classifications": [], "calendars": [], "numbers": [], "completed": False}, "inclusive": {"classifications": [], "calendars": [], "numbers": [], "completed": False}}}

        # self._wund_send = Send_Wunderlist()
        self._validater = validate()
        self._recycler = File_Handler()
        calendars_file = File_Handler("CalendarIDs")
        self._calID_dict = calendars_file.file_ResourceOpen()

        self._print_font = QtGui.QFont("lucida console", 10)

        self.setupUi(self)
        self.actionOpen_File.triggered.connect(self.Open_File_Triggered)
        self.actionRefresh.triggered.connect(self.Refresh_Triggered)
        self.listWidget.itemDoubleClicked.connect(self.DoubleClickEdit)
        self.listWidget.itemChanged.connect(self.UpdateCompleteds)
        # self.actionNew_File.triggered.connect()
        self.actionSave.triggered.connect(self.Save_Triggered)
        self.actionSave_As.triggered.connect(self.Save_As_Triggered)
        self.actionClose.triggered.connect(self.Close_Triggered)
        self.actionNew_Item.triggered.connect(self.New_Item_Triggered)
        self.actionEdit_Item.triggered.connect(self.Edit_Item_Triggered)
        self.actionDelete_Items.triggered.connect(self.Delete_Items_Triggered)
        # self.actionCalendar.triggered.connect()
        # self.actionWunderlist.triggered.connect()
        # self.actionEmail.triggered.connect()
        self.actionPlain_Text.triggered.connect(self.Plain_Text_Triggered)
        self.actionLine_Text.triggered.connect(self.LinePrint_Items_Triggered)
        self.actionImport_Text.triggered.connect(self.Import_Text_Triggered)
        self.actionImport_Data.triggered.connect(self.Import_Data_Triggered)
        self.actionPrint_Settings.triggered.connect(self.Print_Settings_Triggered)
        self.actionOpen_Map.triggered.connect(self.Open_Map_Triggered)
        self.actionFilter_Settings.triggered.connect(self.Filter_Settings_Triggered)
        self.actionDuplicate_Selected.triggered.connect(self.Duplicate_Selected_Triggered)
        self.actionDelete_Selected.triggered.connect(self.Delete_Selected_Triggered)
        self.actionSave_User_Settings.triggered.connect(self.Save_User_Settings)
        self.actionSave_Exit.triggered.connect(self.Save_Exit)
        # self.actionShow_Complete.triggered.connect()

        # self.Open_User_Triggered()

    def Save_Exit(self):
        self.Save_Triggered()
        self.close()

    def Open_Map_Triggered(self):
        self.map_window = MapMainWindow(self._all_data, self._filters, self._data_file, self._recycler, self._calID_dict, self._print_font)
        self.map_window.setWindowTitle("Map Window")
        self.map_window.pushButton.clicked.connect(self.MapWindow_ConfirmButton_Clicked)
        self.map_window.show()

    def MapWindow_ConfirmButton_Clicked(self):
        self._all_data = self.map_window.get_data()
        self._filters = self.map_window.get_map_filters()
        # self._arrange_type = self.print_settings.get_arrangement()
        # print(self._all_data.get_display())

        self.Save_Triggered()
        self.map_window.close()
        self.Refresh_Triggered()

    def UpdateCompleteds(self):
        # pass
        printable_list = self._all_data.get_printables()
        if self.listWidget.count() > 0:
            for i in range(1, self.listWidget.count()):
                real_index = i - 1
                item_number = printable_list[real_index]
                item = dict(self._all_data.get_item(item_number))
                if (self.listWidget.item(i).checkState() == 2) and not(item["completed"]):
                    item["completed"] = True
                    self._all_data.set_item(item_number, item)

                elif (self.listWidget.item(i).checkState() == 0) and (item["completed"]):
                    item["completed"] = False
                    self._all_data.set_item(item_number, item)
        self.Refresh_Triggered()

    def Delete_Selected_Triggered(self):
        row_index = self.listWidget.currentRow()
        printable_list = self._all_data.get_printables()
        if row_index == 0:
            return None
        elif row_index <= len(printable_list):
            real_index = row_index - 1
            item_number = printable_list[real_index]
            recycle_dict = dict()
            recycle_dict[item_number] = self._all_data.remove_item(item_number)
            self._recycler.file_Recycle(recycle_dict)
            self.Refresh_Triggered()
        else:
            return None

    def Duplicate_Selected_Triggered(self):
        row_index = self.listWidget.currentRow()
        printable_list = self._all_data.get_printables()
        if row_index == 0:
            return None
        elif row_index <= len(printable_list):
            # get item to duplicate
            real_index = row_index - 1
            item_number = printable_list[real_index]
            item = dict(self._all_data.get_item(item_number))
            old_title = item["title"]
            item_number1 = item_number[0:3]
            item_number2 = int(item_number[4:])

            for keys in self._all_data.get_data():
                if (keys[0:3] == item_number1) and (int(keys[4:]) > item_number2):
                    item_number2 = int(keys[4:])

            # if item_number2 == int(item_number[4:]):
            item_number2 += 1

            new_item_number = "{}.{:0>2}".format(item_number1, item_number2)
            new_title = new_item_number + old_title[6:]
            item["title"] = new_title
            item["from-links"] = list()
            self._all_data.set_item(new_item_number, item)
            self.Refresh_Triggered()
        else:
            return None

    def Plain_Text_Triggered(self):
        self.text_dialog = TextFileDialog()
        self.text_dialog.setWindowTitle("Plain Text Export")
        self.text_dialog.pushButton.clicked.connect(self.PlainTextPrinter)
        self.text_dialog.show()

    def PlainTextPrinter(self):
        file_name = self.text_dialog.lineEdit.text()
        self._all_data.set_printables()
        header_string = self._printer.print_header(self._all_data)
        printables_list = list(self._all_data.get_printables())
        add_string = ""
        for item in printables_list:
            add_string += self._printer.print_item(self._all_data, item)
            add_string += self._printer.print_divider()
            add_string += "\n"
        out_string = header_string + "\n" + add_string
        self._recycler.set_title(file_name)
        self._recycler.file_TextPrint(out_string)
        self.text_dialog.close()

    def LinePrint_Items_Triggered(self):
        arrange_list = list(self._all_data.get_arrangement())
        temp_dict = dict(self._all_data.get_data())
        self.selection_list = CheckableList()
        self.selection_list.setWindowTitle("Line Data Export")
        self.selection_list.pushButton.clicked.connect(self.LinePrintSelection_ConfirmButton_Clicked)
        for item in arrange_list:
            add_string = temp_dict[item]["title"]
            add_widgetitem = QtWidgets.QListWidgetItem(add_string)
            add_widgetitem.setFlags(QtCore.Qt.ItemIsUserCheckable | add_widgetitem.flags())
            add_widgetitem.setCheckState(QtCore.Qt.Unchecked)
            add_widgetitem.setFont(self._print_font)
            self.selection_list.listWidget.addItem(add_widgetitem)
        self.selection_list.show()

    def LinePrintSelection_ConfirmButton_Clicked(self):
        for i in range(0, self.selection_list.listWidget.count()):
            if self.selection_list.listWidget.item(i).checkState() == 2:
                selected_item_title = self.selection_list.listWidget.item(i).text()
                selected_item_number = selected_item_title[0:6]
                self._all_data.select_item(selected_item_number)
            elif self.selection_list.listWidget.item(i).checkState() == 0:
                selected_item_title = self.selection_list.listWidget.item(i).text()
                selected_item_number = selected_item_title[0:6]
                self._all_data.deselect_item(selected_item_number)
        self.selection_list.close()
        self.text_dialog = TextFileDialog()
        self.text_dialog.pushButton.clicked.connect(self.LinePrint_FileConfirmed)
        self.text_dialog.show()

    def LinePrint_FileConfirmed(self):
        print_dict = dict()
        temp_sel = list(self._all_data.get_selection())
        file_name = self.text_dialog.lineEdit.text()
        for element in temp_sel:
            print_dict[element] = self._all_data.get_item(element)
        self._data_file.file_TextOut(print_dict, file_name)
        self.text_dialog.close()
        self.Refresh_Triggered()

    def Import_Text_Triggered(self):
        self.file_finder = OpenTextDialog()
        self.file_finder.setWindowTitle("Import Line Data")
        self.file_finder.pushButton_2.clicked.connect(self.ImportTextDialog_ConfirmButton_Clicked)
        self.file_finder.show()

    def ImportTextDialog_ConfirmButton_Clicked(self):
        data_name_raw = self.file_finder.comboBox.currentText()
        if "." in data_name_raw:
            data_name_list = data_name_raw.split('.')
            data_name = data_name_list[0]
        else:
            data_name = data_name_raw
        self._recycler.set_title(data_name)
        # need exceptions handling, or do I?
        data_dict = self._recycler.file_TextOpen()
        for keys in data_dict:
            if self._validater.valid_item(data_dict[keys], keys):
                self._all_data.set_item(keys, data_dict[keys])
            else:
                self._all_data.make_valid_item(data_dict[keys], keys)
                self._all_data.set_item(keys, data_dict[keys])
        self.file_finder.close()
        self.Refresh_Triggered()

    def Import_Data_Triggered(self):
        self.file_finder = OpenFileDialog("DataFiles")
        self.file_finder.setWindowTitle("Import File Data")
        self.file_finder.pushButton_2.clicked.connect(self.ImportDataDialog_ConfirmButton_Clicked)
        self.file_finder.show()

    def ImportDataDialog_ConfirmButton_Clicked(self):
        data_name_raw = self.file_finder.comboBox.currentText()
        if "." in data_name_raw:
            data_name_list = data_name_raw.split('.')
            data_name = data_name_list[0]
        else:
            data_name = data_name_raw
        self._recycler.set_title(data_name)
        # need exceptions handling, or do I?
        data_dict = self._recycler.file_DataOpen()
        for keys in data_dict:
            self._all_data.set_item(keys, data_dict[keys])
        self.file_finder.close()
        self.Refresh_Triggered()

    def DoubleClickEdit(self):
        row_index = self.listWidget.currentRow()
        if row_index == 0:
            return None
        else:
            real_index = row_index - 1
            arrange_list = self._all_data.get_printables()
            item_number = arrange_list[real_index]
            item = self._all_data.get_item(item_number)
            self.item_editor = ItemEditor(item, self._calID_dict, self._all_data)
            self.item_editor.pushButton_3.clicked.connect(self.ItemEditor_ConfirmButton_Clicked)
            self.item_editor.show()

    def Delete_Items_Triggered(self):
        arrange_list = list(self._all_data.get_arrangement())
        temp_dict = dict(self._all_data.get_data())
        self.selection_list = CheckableList()
        self.selection_list.setWindowTitle("Delete Items")
        self.selection_list.pushButton.clicked.connect(self.DeleteSelection_ConfirmButton_Clicked)
        for item in arrange_list:
            add_string = temp_dict[item]["title"]
            add_widgetitem = QtWidgets.QListWidgetItem(add_string)
            add_widgetitem.setFlags(QtCore.Qt.ItemIsUserCheckable | add_widgetitem.flags())
            add_widgetitem.setCheckState(QtCore.Qt.Unchecked)
            add_widgetitem.setFont(self._print_font)
            self.selection_list.listWidget.addItem(add_widgetitem)
        self.selection_list.show()

    def DeleteSelection_ConfirmButton_Clicked(self):
        recycle_dict = dict()
        for i in range(0, self.selection_list.listWidget.count()):
            if self.selection_list.listWidget.item(i).checkState() == 2:

                selected_item_title = self.selection_list.listWidget.item(i).text()
                selected_item_number = selected_item_title[0:6]
                self._all_data.select_item(selected_item_number)
            elif self.selection_list.listWidget.item(i).checkState() == 0:
                selected_item_title = self.selection_list.listWidget.item(i).text()
                selected_item_number = selected_item_title[0:6]
                self._all_data.deselect_item(selected_item_number)
        temp_sel = list(self._all_data.get_selection())
        for element in temp_sel:
            recycle_dict[element] = self._all_data.remove_item(element)
        self._recycler.file_Recycle(recycle_dict)
        self.selection_list.close()
        self.Refresh_Triggered()

    def Print_Settings_Triggered(self):
        self.print_settings = PrinterSettings(self._all_data, self._print_font, self._arrange_type)
        self.print_settings.setWindowTitle("Print Settings")
        self.print_settings.pushButton.clicked.connect(self.PrintSettings_ConfirmButton_Clicked)
        self.print_settings.show()

    def PrintSettings_ConfirmButton_Clicked(self):
        self._all_data = self.print_settings.get_data()
        self._arrange_type = self.print_settings.get_arrangement()
        # print(self._all_data.get_display())
        self.print_settings.close()
        self.Refresh_Triggered()

    def Filter_Settings_Triggered(self):
        self.filter_settings = FilterSettings(self._all_data, self._filters, self._calID_dict, self._print_font)
        self.filter_settings.setWindowTitle("Filter Settings")
        self.filter_settings.pushButton.clicked.connect(self.Filter_Settings_ConfirmButton_Clicked)
        self.filter_settings.show()

    def Filter_Settings_ConfirmButton_Clicked(self):
        self.filter_settings.ApplyChanges()
        self._filters = self.filter_settings.get_filters()
        self._all_data.main_filter(self._filters)
        self.filter_settings.close()
        self.Refresh_Triggered()

    def New_Item_Triggered(self):
        default_item = dict()
        self._all_data.make_valid_item(default_item, "000.00")
        self.item_editor = ItemEditor(default_item, self._calID_dict, self._all_data)
        self.item_editor.setWindowTitle("Item Editor")
        self.item_editor.pushButton_3.clicked.connect(self.ItemEditor_ConfirmButton_Clicked)
        self.item_editor.show()

    def Edit_Item_Triggered(self):
        arrange_list = list(self._all_data.get_arrangement())
        temp_dict = dict(self._all_data.get_data())
        self.pick_list = PickList()
        self.pick_list.setWindowTitle("Edit Item Selection")
        self.pick_list.pushButton_2.clicked.connect(self.PickList_ConfirmButton_Clicked)
        for item in arrange_list:
            add_string = temp_dict[item]["title"]
            add_widgetitem = QtWidgets.QListWidgetItem(add_string)
            add_widgetitem.setFont(self._print_font)
            self.pick_list.listWidget.addItem(add_widgetitem)
        self.pick_list.show()

    def PickList_ConfirmButton_Clicked(self):
        selected_item_title = self.pick_list.listWidget.currentItem().text()
        selected_item_number = selected_item_title[0:6]
        selected_item = self._all_data.get_data()[selected_item_number]
        self.item_editor = ItemEditor(selected_item, self._calID_dict, self._all_data)
        self.item_editor.setWindowTitle("Item Editor")
        self.item_editor.pushButton_3.clicked.connect(self.ItemEditor_ConfirmButton_Clicked)
        self.pick_list.close()
        self.item_editor.show()

    def ItemEditor_ConfirmButton_Clicked(self):
        temp_num = self.item_editor.get_number()
        temp_data = self.item_editor.get_data()
        self._all_data.set_item(temp_num, temp_data)
        self._all_data.reset_links()
        # for from_item in temp_data["from-links"]:
        #     temp_from_number = from_item[0:6]
        #     temp_from_item = self._all_data.get_item(temp_from_number)
        #     if temp_data["title"] not in temp_from_item["to-links"]:
        #         temp_from_item["to-links"].append(temp_data["title"])
        #     self._all_data.set_item(temp_from_number,temp_from_item)
        #
        # for to_item in temp_data["to-links"]:
        #     temp_to_number = to_item[0:6]
        #     temp_to_item = self._all_data.get_item(temp_to_number)
        #     if temp_data["title"] not in temp_to_item["from-links"]:
        #         temp_to_item["from-links"].append(temp_data["title"])
        #     self._all_data.set_item(temp_to_number,temp_to_item)

        self.item_editor.close()
        self.Refresh_Triggered()

    def Close_Triggered(self):
        self._data_file = File_Handler()
        self._all_data = Task_Data(dict())
        self.Refresh_Triggered()

    def Save_Triggered(self):
        self._data_file.file_DataSave(self._all_data.get_data())

    def Save_As_Triggered(self):
        self.file_finder = JsonFileDialog()
        self.file_finder.setWindowTitle("Save Data File As")
        self.file_finder.pushButton.clicked.connect(self.JsonFileDialog_ConfirmButton_Clicked)
        self.file_finder.show()

    def JsonFileDialog_ConfirmButton_Clicked(self):
        file_name = self.file_finder.lineEdit.text()
        self._all_data.select_all()
        self._data_file.file_DataOut(self._all_data.get_data(), file_name)
        self._all_data.reset_selection()
        self.file_finder.close()

    def Refresh_Triggered(self):
        self._settings["sort"] = self._arrange_type
        self._settings["fields"] = self._all_data.get_fields()
        self._settings["filters"] = self._filters
        if self._all_data.get_data() == dict():
            self.listWidget.clear()
        else:
            self.listWidget.clear()
            # self._all_data.set_fields(self._all_data.get_fields_max())
            self._all_data.arrange_data(self._arrange_type)
            self._all_data.set_printables()
            header_string = self._printer.print_header(self._all_data)
            header_widgetitem = QtWidgets.QListWidgetItem(header_string)
            header_widgetitem.setFont(self._print_font)
            header_widgetitem.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(header_widgetitem)
            printables_list = list(self._all_data.get_printables())
            for item in printables_list:
                item_dict = self._all_data.get_item(item)
                add_string = self._printer.print_item(self._all_data, item)
                add_string += self._printer.print_divider()
                add_widgetitem = QtWidgets.QListWidgetItem(add_string)
                add_widgetitem.setFont(self._print_font)
                add_widgetitem.setFlags(QtCore.Qt.ItemIsUserCheckable | add_widgetitem.flags())
                if item_dict["completed"]:
                    add_widgetitem.setCheckState(QtCore.Qt.Checked)
                else:
                    add_widgetitem.setCheckState(QtCore.Qt.Unchecked)
                # add_widgetitem.setCheckState(QtCore.Qt.Unchecked)
                self.listWidget.addItem(add_widgetitem)

    def Open_File_Triggered(self):
        self.file_finder = OpenFileDialog("DataFiles")
        self.file_finder.setWindowTitle("Open Data File")
        self.file_finder.pushButton_2.clicked.connect(self.OpenFileDialog_ConfirmButton_Clicked)
        self.file_finder.show()

    def OpenFileDialog_ConfirmButton_Clicked(self):
        data_name_raw = self.file_finder.comboBox.currentText()
        if "." in data_name_raw:
            data_name_list = data_name_raw.split('.')
            data_name = data_name_list[0]
        else:
            data_name = data_name_raw
        self._data_file.set_title(data_name)
        # need exceptions handling, or do I?
        data_dict = self._data_file.file_DataOpen()
        self._all_data.set_data(data_dict)
        self._all_data.set_fields(self._settings["fields"])
        self.file_finder.close()
        self.Refresh_Triggered()

    def Open_User_Triggered(self):
        self.file_finder = OpenFileDialog("UserFiles")
        self.file_finder.setWindowTitle("Open User Settings")
        self.file_finder.pushButton_2.clicked.connect(self.OpenUserDialog_ConfirmButton_Clicked)
        self.file_finder.show()

    def OpenUserDialog_ConfirmButton_Clicked(self):
        data_name_raw = self.file_finder.comboBox.currentText()
        if "." in data_name_raw:
            user_name_list = data_name_raw.split('.')
            user_name = user_name_list[0]
        else:
            user_name = data_name_raw
        self._user_file.set_title(user_name)
        # need exceptions handling, or do I?
        user_dict = self._user_file.file_UserOpen()
        self._settings = user_dict
        self._arrange_type = self._settings["sort"]
        self._filters = self._settings["filters"]
        self._all_data.set_fields(self._settings["fields"])
        self.file_finder.close()
        self.Refresh_Triggered()

    def Save_User_Settings(self):
        self._settings["fields"] = self._all_data.get_fields()
        self._settings["filters"] = self._filters
        self._settings["sort"] = self._arrange_type
        self._user_file.file_UserSave(self._settings)
