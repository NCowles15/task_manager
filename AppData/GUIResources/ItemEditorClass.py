from ClassResources.Validifiers import validate
from GUIResources.EditableListClass import EditableList
from GUIResources.EditableListCheckableClass import EditableListCheckable
from GUIResources.CheckableLinksListClass import CheckableLinksList

import os

from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore

path = os.path.dirname(os.path.abspath(__file__))
ItemEditorUI, ItemEditorBase = uic.loadUiType(os.path.join(path, 'itemeditor.ui'))


class ItemEditor(ItemEditorBase, ItemEditorUI):
    def __init__(self, start_dict, cal_dict, total_data, parent=None):

        ItemEditorBase.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)

        self._data = dict(start_dict)
        title_string = self._data["title"]
        self._number = title_string[:6]
        self._calID_dict = dict(cal_dict)
        self._validater = validate()
        self._total_data = total_data

        self.lineEdit.setText(self._data["name"])
        self.lineEdit_2.setText(self._number)
        self.label_invalid3.setText(self._data["title"])
        # self.lineEdit_3.setText(self._data["title"])
        date_list = self._data["due date"].split('-')
        due_date = QtCore.QDate(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        self.dateEdit.setDate(due_date)
        start_time_range, end_time_range = self._data["time range"].split(',')
        start_time_string, start_time_zone = start_time_range.split('-')
        start_time_list = start_time_string.split(":")
        start_zone = int(start_time_zone[:2])
        start_time = QtCore.QTime(int(start_time_list[0]), int(start_time_list[1]), int(start_time_list[2]))
        self.timeEdit.setTime(start_time)
        self.spinBox.setMaximum(15)
        self.spinBox.setMinimum(0)
        self.spinBox.setValue(start_zone)
        end_time_string, end_time_zone = end_time_range.split('-')
        end_time_list = end_time_string.split(":")
        end_zone = int(end_time_zone[:2])
        end_time = QtCore.QTime(int(end_time_list[0]), int(end_time_list[1]), int(end_time_list[2]))
        self.timeEdit_2.setTime(end_time)
        self.spinBox_2.setMaximum(15)
        self.spinBox_2.setMinimum(0)
        self.spinBox_2.setValue(end_zone)
        self.lineEdit_4.setText(self._data["classification"])
        for key in self._calID_dict:
            self.comboBox_2.addItem(key)
        cal_index = self.comboBox_2.findText(self._data["calendar"])
        self.comboBox_2.setCurrentIndex(cal_index)
        self.label_18.setText(self.List_String_Format(self._data["parameters"]))
        self.label_19.setText(self.List_String_Format(self._data["qualifiers"]))
        # print("before from links")
        self.label_20.setText(self.List_String_Format(self._data["from-links"]))
        # print("after from links")
        self.label_21.setText(self.List_String_Format(self._data["to-links"]))
        self.spinBox_3.setMinimum(0)
        self.spinBox_3.setValue(self._data["i value"])
        self.doubleSpinBox.setMinimum(0)
        self.doubleSpinBox.setSingleStep(0.25)
        self.doubleSpinBox.setValue(self._data["s value"])
        self.spinBox_5.setMinimum(1)
        self.spinBox_5.setMaximum(12)
        self.spinBox_5.setValue(self._data["w value"])
        if self._data["display"]:
            self.checkBox.setCheckState(0)
        else:
            self.checkBox.setCheckState(2)

        if self._data["completed"]:
            self.checkBox_2.setCheckState(2)
        else:
            self.checkBox_2.setCheckState(0)


        self.pushButton_2.clicked.connect(self.ItemEditor_ApplyAll_Clicked)
        self.pushButton_4.clicked.connect(self.ItemEditor_NameApply_Clicked)
        self.pushButton_5.clicked.connect(self.ItemEditor_NumberApply_Clicked)
        # self.pushButton_6.clicked.connect(self.ItemEditor_TitleApply_Clicked)
        self.pushButton_7.clicked.connect(self.ItemEditor_DueApply_Clicked)
        self.pushButton_8.clicked.connect(self.ItemEditor_StartTimeApply_Clicked)
        self.pushButton_9.clicked.connect(self.ItemEditor_EndTimeApply_Clicked)
        self.pushButton_10.clicked.connect(self.ItemEditor_ClassApply_Clicked)
        self.pushButton_11.clicked.connect(self.ItemEditor_CalendarApply_Clicked)
        self.pushButton_12.clicked.connect(self.ItemEditor_EditParams_Clicked)
        self.pushButton_13.clicked.connect(self.ItemEditor_EditQuals_Clicked)
        # self.pushButton_14.clicked.connect(self.ItemEditor_EditFroms_Clicked)
        self.pushButton_15.clicked.connect(self.ItemEditor_EditTos_Clicked)
        self.pushButton_16.clicked.connect(self.ItemEditor_ISWApply_Clicked)
        self.pushButton_18.clicked.connect(self.ItemEditor_CompleteApply_Clicked)
        self.pushButton_17.clicked.connect(self.ItemEditor_HiddenApply_Clicked)

    def List_String_Format(self, in_list):
        list_string = "[ "
        i = 0
        for items in in_list:
            if i > 3:
                list_string += "..."
                break
            else:
                list_string += str(items)
                list_string += ", "
                i += 1
        if (i <= 3) and (i >= 1):
            list_string = list_string[:-2]
        list_string += " ]"
        return list_string

    def get_data(self):
        return self._data

    def get_number(self):
        return self._number

    def ItemEditor_ApplyAll_Clicked(self):
        self.ItemEditor_NameApply_Clicked()
        self.ItemEditor_NumberApply_Clicked()
        # self.ItemEditor_TitleApply_Clicked()
        self.ItemEditor_DueApply_Clicked()
        self.ItemEditor_StartTimeApply_Clicked()
        self.ItemEditor_EndTimeApply_Clicked()
        self.ItemEditor_ClassApply_Clicked()
        self.ItemEditor_CalendarApply_Clicked()
        # self.ItemEditor_EditParams_Clicked()
        # self.ItemEditor_EditQuals_Clicked()
        # self.ItemEditor_EditTos_Clicked()
        self.ItemEditor_ISWApply_Clicked()
        self.ItemEditor_CompleteApply_Clicked()
        self.ItemEditor_HiddenApply_Clicked()

    def ItemEditor_NameApply_Clicked(self):
        text = self.lineEdit.text()
        if self._validater.valid_name(text):
            self._data["name"] = text
            self.label_invalid1.setText("")
            # current_number = self._data["title"][:6]
            self._data["title"] = "{} - {}".format(self._number, self._data["name"])
            self.label_invalid3.setText(self._data["title"])
        else:
            self.label_invalid1.setText("Invalid")

    def ItemEditor_NumberApply_Clicked(self):
        text = self.lineEdit_2.text()
        if self._validater.valid_number(text):
            if text in self._total_data.get_data().keys():
                number_warning = "Warning: This task number already exists"
                self.label_warning1.setText(number_warning)
            else:
                self.label_warning1.setText("")
            self._number = text
            self.label_invalid2.setText("")
            self._data["title"] = "{} - {}".format(self._number, self._data["name"])
            self.label_invalid3.setText(self._data["title"])
        else:
            self.label_invalid2.setText("Invalid")

    # def ItemEditor_TitleApply_Clicked(self):
    #     text = self.lineEdit_3.text()
    #     if self._validater.valid_title(text):
    #         self._data["title"] = text
    #         self.label_invalid3.setText("")
    #     else:
    #         self.label_invalid3.setText("Invalid")

    def ItemEditor_DueApply_Clicked(self):
        years = self.dateEdit.date().year()
        months = self.dateEdit.date().month()
        days = self.dateEdit.date().day()
        date_str = "{:04d}-{:02d}-{:02d}".format(years, months, days)
        if self._validater.valid_date(date_str):
            self._data["due date"] = date_str

    def ItemEditor_StartTimeApply_Clicked(self):
        time_range_str = self._data["time range"]
        time_range_list = time_range_str.split(',')
        hours = self.timeEdit.time().hour()
        minutes = self.timeEdit.time().minute()
        seconds = self.timeEdit.time().second()
        zone_hours = self.spinBox.value()
        zone_minutes = 0
        fill_str = "{:02d}:{:02d}:{:02d}-{:02d}:{:02d}".format(hours, minutes, seconds, zone_hours, zone_minutes)
        time_range_list[0] = fill_str
        time_range_out = ",".join(time_range_list)
        if self._validater.valid_time(time_range_out):
            self._data["time range"] = time_range_out

    def ItemEditor_EndTimeApply_Clicked(self):
        time_range_str = self._data["time range"]
        time_range_list = time_range_str.split(',')
        hours = self.timeEdit_2.time().hour()
        minutes = self.timeEdit_2.time().minute()
        seconds = self.timeEdit_2.time().second()
        zone_hours = self.spinBox_2.value()
        zone_minutes = 0
        fill_str = "{:02d}:{:02d}:{:02d}-{:02d}:{:02d}".format(hours, minutes, seconds, zone_hours, zone_minutes)
        time_range_list[1] = fill_str
        time_range_out = ",".join(time_range_list)
        if self._validater.valid_time(time_range_out):
            self._data["time range"] = time_range_out

    def ItemEditor_ClassApply_Clicked(self):
        text = self.lineEdit_4.text()
        if self._validater.valid_classify(text):
            self._data["classification"] = text
            self.label_invalid4.setText("")
        else:
            self.label_invalid4.setText("Invalid")

    def ItemEditor_CalendarApply_Clicked(self):
        text = self.comboBox_2.currentText()
        if self._validater.valid_calendar(text):
            self._data["calendar"] = text

    def ItemEditor_EditParams_Clicked(self):
        self.params_editor = EditableListCheckable(self._data["parameters"])
        self.params_editor.setWindowTitle("Parameters Editor")
        self.params_editor.pushButton.clicked.connect(self.ParamEditor_ConfirmButton_Clicked)
        self.params_editor.show()

    def ParamEditor_ConfirmButton_Clicked(self):
        temp_list = self.params_editor.get_list()
        if self._validater.valid_parameter(temp_list):
            self._data["parameters"] = temp_list
            self.label_18.setText(self.List_String_Format(self._data["parameters"]))
        self.params_editor.close()

    def ItemEditor_EditQuals_Clicked(self):
        self.quals_editor = EditableList(self._data["qualifiers"])
        self.quals_editor.setWindowTitle("Qualifiers Editor")
        self.quals_editor.pushButton.clicked.connect(self.QualEditor_ConfirmButton_Clicked)
        self.quals_editor.show()

    def QualEditor_ConfirmButton_Clicked(self):
        temp_list = self.quals_editor.get_list()
        if self._validater.valid_qualifier(temp_list):
            self._data["qualifiers"] = temp_list
            self.label_19.setText(self.List_String_Format(self._data["qualifiers"]))
        self.quals_editor.close()

    # def ItemEditor_EditFroms_Clicked(self):
    #     arrange_list = list(self._total_data.get_arrangement())
    #     temp_dict = dict(self._total_data.get_data())
    #     self.froms_editor = CheckableLinksList(self._data["from-links"])
    #     self.froms_editor.setWindowTitle("From-Links Editor")
    #     self.froms_editor.pushButton.clicked.connect(self.FromsEditor_ConfirmButton_Clicked)
    #     for item in arrange_list:
    #         add_string = temp_dict[item]["title"]
    #         add_widgetitem = QtWidgets.QListWidgetItem(add_string)
    #         add_widgetitem.setFlags(QtCore.Qt.ItemIsUserCheckable | add_widgetitem.flags())
    #         if add_string in self._data["from-links"]:
    #             # pass
    #             add_widgetitem.setCheckState(QtCore.Qt.Checked)
    #         else:
    #             add_widgetitem.setCheckState(QtCore.Qt.Unchecked)
    #         # add_widgetitem.setFont(self._print_font)
    #         self.froms_editor.listWidget.addItem(add_widgetitem)
    #     self.froms_editor.show()
    #
    # def FromsEditor_ConfirmButton_Clicked(self):
    #     temp_list = self.froms_editor.get_list()
    #     if self._validater.valid_from_links(temp_list):
    #         self._data["from-links"] = temp_list
    #         self.label_20.setText(str(self._data["from-links"]))
    #     self.froms_editor.close()

    def ItemEditor_EditTos_Clicked(self):
        arrange_list = list(self._total_data.get_arrangement())
        temp_dict = dict(self._total_data.get_data())
        self.tos_editor = CheckableLinksList(self._data["to-links"])
        self.tos_editor.setWindowTitle("To-Links Editor")
        self.tos_editor.pushButton.clicked.connect(self.TosEditor_ConfirmButton_Clicked)
        for item in arrange_list:
            add_string = temp_dict[item]["title"]
            add_widgetitem = QtWidgets.QListWidgetItem(add_string)
            add_widgetitem.setFlags(QtCore.Qt.ItemIsUserCheckable | add_widgetitem.flags())
            if add_string in self._data["to-links"]:
                add_widgetitem.setCheckState(QtCore.Qt.Checked)
            else:
                add_widgetitem.setCheckState(QtCore.Qt.Unchecked)
            # add_widgetitem.setFont(self._print_font)
            self.tos_editor.listWidget.addItem(add_widgetitem)
        self.tos_editor.show()

    def TosEditor_ConfirmButton_Clicked(self):
        temp_list = self.tos_editor.get_list()
        if self._validater.valid_to_links(temp_list):
            self._data["to-links"] = temp_list
            self.label_21.setText(self.List_String_Format(self._data["to-links"]))
        self.tos_editor.close()

    def ItemEditor_ISWApply_Clicked(self):
        i_val = self.spinBox_3.value()
        s_val = self.doubleSpinBox.value()
        w_val = self.spinBox_5.value()
        if self._validater.valid_ISW(i_val):
            self._data["i value"] = i_val
        if self._validater.valid_ISW(s_val):
            self._data["s value"] = s_val
        if self._validater.valid_ISW(w_val):
            self._data["w value"] = w_val

    def ItemEditor_CompleteApply_Clicked(self):
        if self.checkBox_2.checkState() == 2:
            self._data["completed"] = True
        else:
            self._data["completed"] = False

    def ItemEditor_HiddenApply_Clicked(self):
        if self.checkBox.checkState() == 2:
            self._data["display"] = False
        else:
            self._data["display"] = True