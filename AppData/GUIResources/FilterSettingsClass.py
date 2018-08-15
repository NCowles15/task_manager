import os
import datetime
from datetime import date

from PyQt5 import uic
from PyQt5 import QtGui, QtWidgets, QtCore

path = os.path.dirname(os.path.abspath(__file__))
FilterSettingsUI, FilterSettingsBase = uic.loadUiType(os.path.join(path, 'filtersettings.ui'))


class FilterSettings(FilterSettingsBase, FilterSettingsUI):
    def __init__(self, data, filters_dict, calendars, print_font, parent=None):
        FilterSettingsBase.__init__(self, parent)
        self.setupUi(self)
        self._data = data
        self._filters = filters_dict
        self._arrangement = self._data.get_arrangement()
        self._calsDict = calendars
        self._print_font = print_font

        current_datetime_str = str(datetime.datetime.today())
        current_date_str, current_time_str = current_datetime_str.split()
        current_date_list = current_date_str.split("-")
        current_date = QtCore.QDate(int(current_date_list[0]), int(current_date_list[1]), int(current_date_list[2]))
        self.dateEdit.setDate(current_date)
        self.dateEdit_2.setDate(current_date)
        self.dateEdit_3.setDate(current_date)
        self.dateEdit_4.setDate(current_date)

        all_classify = ["C", "F", "P", "T", "V", "O", "SC", "SF", "SP", "ST", "SV", "SO", "CW", "FW", "PW", "TW", "VW",
                        "OW", "SCW", "SFW", "SPW", "STW", "SVW", "SOW", "AC", "AF", "AP", "AT", "AV", "AO", "ASC",
                        "ASF", "ASP", "AST", "ASV", "ASO", "ACW", "AFW", "APW", "ATW", "AVW", "AOW", "ASCW", "ASFW",
                        "ASPW", "ASTW", "ASVW", "ASOW"]

        for item in all_classify:
            self.comboBox.addItem(item)
            self.comboBox_4.addItem(item)

        for key in self._calsDict:
            self.comboBox_2.addItem(key)
            self.comboBox_3.addItem(key)

        temp_dict = dict(self._data.get_data())
        arrange_list = list(self._data.get_arrangement())
        for item in arrange_list:
            add_string = temp_dict[item]["title"]
            add_widgetitem = QtWidgets.QListWidgetItem(add_string)
            add_widgetitem.setFlags(QtCore.Qt.ItemIsUserCheckable | add_widgetitem.flags())
            if item in self._filters["manual"]:
                add_widgetitem.setCheckState(QtCore.Qt.Checked)
            else:
                add_widgetitem.setCheckState(QtCore.Qt.Unchecked)
            add_widgetitem.setFont(self._print_font)
            self.listWidget.addItem(add_widgetitem)

        temp_dict = self._filters["exclusive"]
        for keys in temp_dict:
            if keys != "completed":
                for item in temp_dict[keys]:
                    add_string = "{} : {}".format(keys, item)
                    add_widgetitem = QtWidgets.QListWidgetItem(add_string)
                    add_widgetitem.setFont(self._print_font)
                    self.listWidget_3.addItem(add_widgetitem)
            else:
                add_string = "{} : {}".format(keys, self._filters["exclusive"]["completed"])
                add_widgetitem = QtWidgets.QListWidgetItem(add_string)
                add_widgetitem.setFont(self._print_font)
                self.listWidget_3.addItem(add_widgetitem)

        temp_dict = self._filters["inclusive"]
        for keys in temp_dict:
            if keys != "completed":
                for item in temp_dict[keys]:
                    add_string = "{} : {}".format(keys, item)
                    add_widgetitem = QtWidgets.QListWidgetItem(add_string)
                    add_widgetitem.setFont(self._print_font)
                    self.listWidget_2.addItem(add_widgetitem)
            else:
                add_string = "{} : {}".format(keys, self._filters["inclusive"]["completed"])
                add_widgetitem = QtWidgets.QListWidgetItem(add_string)
                add_widgetitem.setFont(self._print_font)
                self.listWidget_2.addItem(add_widgetitem)

        self.listWidget.itemSelectionChanged.connect(self.RefreshManual)
        self.pushButton_4.clicked.connect(self.ApplySelectAll)
        self.pushButton_2.clicked.connect(self.close)
        self.radioButton.clicked.connect(self.ExclusiveSelected)
        self.radioButton_2.clicked.connect(self.ManualSelected)
        self.radioButton_3.clicked.connect(self.InclusiveSelected)
        self.listWidget_2.itemDoubleClicked.connect(self.DoubleClickRemovalInclusive)
        self.pushButton_5.clicked.connect(self.AddInclusiveClass)
        self.pushButton_6.clicked.connect(self.AddInclusiveCal)
        self.pushButton_8.clicked.connect(self.AddInclusiveNumber)
        self.pushButton_3.clicked.connect(self.AddInclusiveComp)
        self.listWidget_3.itemDoubleClicked.connect(self.DoubleClickRemovalExclusive)
        self.pushButton_7.clicked.connect(self.AddExclusiveClass)
        self.pushButton_9.clicked.connect(self.AddExclusiveCal)
        self.pushButton_10.clicked.connect(self.AddExclusiveNumber)
        self.pushButton_11.clicked.connect(self.AddExclusiveComp)
        self.pushButton_12.clicked.connect(self.ApplyChanges)
        self.pushButton_13.clicked.connect(self.AddInclusiveDate)
        self.pushButton_14.clicked.connect(self.AddExclusiveDate)
        self.pushButton_15.clicked.connect(self.AddInclusivePriority)
        self.pushButton_16.clicked.connect(self.AddExclusivePriority)


        if self._filters["mode"] == "manual":
            self.radioButton_2.click()
        elif self._filters["mode"] == "inclusive":
            self.radioButton_3.click()
        elif self._filters["mode"] == "exclusive":
            self.radioButton.click()



    def ApplyChanges(self):
        self.RefreshManual()
        self.RefreshExclusiveList()
        self.RefreshInclusiveList()

    def ManualSelected(self):
        self._filters["mode"] = "manual"

        # enable manual
        self.radioButton_2.setChecked(True)
        self.checkBox.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        self.listWidget.setEnabled(True)

        # disable exclusive
        self.radioButton.setChecked(False)
        self.listWidget_3.setEnabled(False)
        self.comboBox_4.setEnabled(False)
        self.comboBox_3.setEnabled(False)
        self.spinBox_2.setEnabled(False)
        self.checkBox_3.setEnabled(False)
        self.dateEdit_3.setEnabled(False)
        self.dateEdit_4.setEnabled(False)
        self.doubleSpinBox_3.setEnabled(False)
        self.doubleSpinBox_4.setEnabled(False)
        self.pushButton_7.setEnabled(False)
        self.pushButton_9.setEnabled(False)
        self.pushButton_10.setEnabled(False)
        self.pushButton_11.setEnabled(False)
        self.pushButton_14.setEnabled(False)
        self.pushButton_16.setEnabled(False)

        # disable inclusive
        self.radioButton_3.setChecked(False)
        self.listWidget_2.setEnabled(False)
        self.comboBox.setEnabled(False)
        self.comboBox_2.setEnabled(False)
        self.spinBox.setEnabled(False)
        self.checkBox_2.setEnabled(False)
        self.dateEdit.setEnabled(False)
        self.dateEdit_2.setEnabled(False)
        self.doubleSpinBox.setEnabled(False)
        self.doubleSpinBox_2.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_13.setEnabled(False)
        self.pushButton_15.setEnabled(False)

    def RefreshManual(self):
        temp_list = list()
        for i in range(0, self.listWidget.count()):
            item = self.listWidget.item(i).text()
            item_num = item[:6]
            if self.listWidget.item(i).checkState() == 2:
                temp_list.append(item_num)
        self._filters["manual"] = temp_list

    def ApplySelectAll(self):
        if self.checkBox.checkState() == 2:
            for i in range(0, self.listWidget.count()):
                if self.listWidget.item(i).checkState() == 0:
                    self.listWidget.item(i).setCheckState(2)
        elif self.checkBox.checkState() == 0:
            for i in range(0, self.listWidget.count()):
                if self.listWidget.item(i).checkState() == 2:
                    self.listWidget.item(i).setCheckState(0)
        self.RefreshManual()

    def InclusiveSelected(self):
        self._filters["mode"] = "inclusive"

        # Enable Inclusive
        self.radioButton_3.setChecked(True)
        self.listWidget_2.setEnabled(True)
        self.comboBox.setEnabled(True)
        self.comboBox_2.setEnabled(True)
        self.spinBox.setEnabled(True)
        self.checkBox_2.setEnabled(True)
        self.dateEdit.setEnabled(True)
        self.dateEdit_2.setEnabled(True)
        self.doubleSpinBox.setEnabled(True)
        self.doubleSpinBox_2.setEnabled(True)
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        self.pushButton_8.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_13.setEnabled(True)
        self.pushButton_15.setEnabled(True)

        # disable manual
        self.radioButton_2.setChecked(False)
        self.checkBox.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.listWidget.setEnabled(False)

        # disable exclusive
        self.radioButton.setChecked(False)
        self.listWidget_3.setEnabled(False)
        self.comboBox_4.setEnabled(False)
        self.comboBox_3.setEnabled(False)
        self.spinBox_2.setEnabled(False)
        self.checkBox_3.setEnabled(False)
        self.dateEdit_3.setEnabled(False)
        self.dateEdit_4.setEnabled(False)
        self.doubleSpinBox_3.setEnabled(False)
        self.doubleSpinBox_4.setEnabled(False)
        self.pushButton_7.setEnabled(False)
        self.pushButton_9.setEnabled(False)
        self.pushButton_10.setEnabled(False)
        self.pushButton_11.setEnabled(False)
        self.pushButton_14.setEnabled(False)
        self.pushButton_16.setEnabled(False)

    def DoubleClickRemovalInclusive(self):
        pop_row = self.listWidget_2.currentRow()
        pop_item = self.listWidget_2.takeItem(pop_row)
        self.RefreshInclusiveList()

    def AddInclusiveClass(self):
        value = self.comboBox.currentText()
        add_string = "classifications : {}".format(value)
        add_widgetitem = QtWidgets.QListWidgetItem(add_string)
        add_widgetitem.setFont(self._print_font)
        self.listWidget_2.addItem(add_widgetitem)
        self._filters["inclusive"]["classifications"].append(value)

    def AddInclusiveCal(self):
        value = self.comboBox_2.currentText()
        add_string = "calendars : {}".format(value)
        add_widgetitem = QtWidgets.QListWidgetItem(add_string)
        add_widgetitem.setFont(self._print_font)
        self.listWidget_2.addItem(add_widgetitem)
        self._filters["inclusive"]["calendars"].append(value)

    def AddInclusiveNumber(self):
        value = self.spinBox.value()
        add_string = "numbers : {:0>2}".format(value)
        add_widgetitem = QtWidgets.QListWidgetItem(add_string)
        add_widgetitem.setFont(self._print_font)
        self.listWidget_2.addItem(add_widgetitem)
        self._filters["inclusive"]["numbers"].append(int(value))

    def AddInclusiveDate(self):
        years_lower = self.dateEdit.date().year()
        months_lower = self.dateEdit.date().month()
        days_lower = self.dateEdit.date().day()
        date_str_lower = "{:04d}-{:02d}-{:02d}".format(years_lower, months_lower, days_lower)
        years_upper = self.dateEdit_2.date().year()
        months_upper = self.dateEdit_2.date().month()
        days_upper = self.dateEdit_2.date().day()
        date_str_upper = "{:04d}-{:02d}-{:02d}".format(years_upper, months_upper, days_upper)
        date_range_str = "{},{}".format(date_str_lower, date_str_upper)
        add_string = "dates : {}".format(date_range_str)
        add_widgetitem = QtWidgets.QListWidgetItem(add_string)
        add_widgetitem.setFont(self._print_font)
        self.listWidget_2.addItem(add_widgetitem)
        self._filters["inclusive"]["dates"].append(date_range_str)

    def AddInclusivePriority(self):
        prior_lower = self.doubleSpinBox.value()
        prior_upper = self.doubleSpinBox_2.value()
        priority_range = "{:.2f}-{:.2f}".format(prior_lower,prior_upper)
        add_string = "priorities : {}".format(priority_range)
        add_widgetitem = QtWidgets.QListWidgetItem(add_string)
        add_widgetitem.setFont(self._print_font)
        self.listWidget_2.addItem(add_widgetitem)
        self._filters["inclusive"]["priorities"].append(priority_range)

    def AddInclusiveComp(self):
        pre_value = self.checkBox_2.checkState()
        if pre_value == 2:
            value = True
        else:
            value = False
        add_string = "completed : {}".format(str(value))
        add_widgetitem = QtWidgets.QListWidgetItem(add_string)
        add_widgetitem.setFont(self._print_font)

        for i in range(0, self.listWidget_2.count()):
            item = self.listWidget_2.item(i).text()
            key, sub_value = item.split(" : ")
            if key == "completed":
                pop_row = i
                pop_item = self.listWidget_2.takeItem(pop_row)
                break
        self.listWidget_2.addItem(add_widgetitem)
        self._filters["inclusive"]["completed"] = value

    def RefreshInclusiveList(self):
        temp_class_list = list()
        temp_cal_list = list()
        temp_num_list = list()
        temp_date_list = list()
        temp_prior_list = list()
        temp_complete = bool()
        for i in range(0, self.listWidget_2.count()):
            item = self.listWidget_2.item(i).text()
            key, sub_val = item.split(" : ")
            if key == "classifications":
                temp_class_list.append(sub_val)
            elif key == "calendars":
                temp_cal_list.append(sub_val)
            elif key == "numbers":
                temp_num_list.append(int(sub_val))
            elif key == "dates":
                temp_date_list.append(sub_val)
            elif key == "priorities":
                temp_prior_list.append(sub_val)
            elif key == "completed":
                if sub_val == "True":
                    temp_complete = True
                else:
                    temp_complete = False

        self._filters["inclusive"]["classifications"] = temp_class_list
        self._filters["inclusive"]["calendars"] = temp_cal_list
        self._filters["inclusive"]["numbers"] = temp_num_list
        self._filters["inclusive"]["dates"] = temp_date_list
        self._filters["inclusive"]["priorities"] = temp_prior_list
        self._filters["inclusive"]["completed"] = temp_complete

    def ExclusiveSelected(self):
        self._filters["mode"] = "exclusive"

        # enable exclusive
        self.radioButton.setChecked(True)
        self.listWidget_3.setEnabled(True)
        self.comboBox_4.setEnabled(True)
        self.comboBox_3.setEnabled(True)
        self.spinBox_2.setEnabled(True)
        self.checkBox_3.setEnabled(True)
        self.dateEdit_3.setEnabled(True)
        self.dateEdit_4.setEnabled(True)
        self.doubleSpinBox_3.setEnabled(True)
        self.doubleSpinBox_4.setEnabled(True)
        self.pushButton_7.setEnabled(True)
        self.pushButton_9.setEnabled(True)
        self.pushButton_10.setEnabled(True)
        self.pushButton_11.setEnabled(True)
        self.pushButton_14.setEnabled(True)
        self.pushButton_16.setEnabled(True)

        # disable inclusive
        self.radioButton_3.setChecked(False)
        self.listWidget_2.setEnabled(False)
        self.comboBox.setEnabled(False)
        self.comboBox_2.setEnabled(False)
        self.spinBox.setEnabled(False)
        self.checkBox_2.setEnabled(False)
        self.dateEdit.setEnabled(False)
        self.dateEdit_2.setEnabled(False)
        self.doubleSpinBox.setEnabled(False)
        self.doubleSpinBox_2.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_13.setEnabled(False)
        self.pushButton_15.setEnabled(False)

        # disable manual
        self.radioButton_2.setChecked(False)
        self.checkBox.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.listWidget.setEnabled(False)

    def DoubleClickRemovalExclusive(self):
        pop_row = self.listWidget_3.currentRow()
        pop_item = self.listWidget_3.takeItem(pop_row)
        self.RefreshExclusiveList()

    def AddExclusiveClass(self):
        value = self.comboBox_4.currentText()
        add_string = "classifications : {}".format(value)
        add_widgetitem = QtWidgets.QListWidgetItem(add_string)
        add_widgetitem.setFont(self._print_font)
        self.listWidget_3.addItem(add_widgetitem)
        self._filters["exclusive"]["classifications"].append(value)

    def AddExclusiveCal(self):
        value = self.comboBox_3.currentText()
        add_string = "calendars : {}".format(value)
        add_widgetitem = QtWidgets.QListWidgetItem(add_string)
        add_widgetitem.setFont(self._print_font)
        self.listWidget_3.addItem(add_widgetitem)
        self._filters["exclusive"]["calendars"].append(value)

    def AddExclusiveNumber(self):
        value = self.spinBox_2.value()
        add_string = "numbers : {:0>2}".format(value)
        add_widgetitem = QtWidgets.QListWidgetItem(add_string)
        add_widgetitem.setFont(self._print_font)
        self.listWidget_3.addItem(add_widgetitem)
        self._filters["exclusive"]["numbers"].append(int(value))

    def AddExclusiveComp(self):
        pre_value = self.checkBox_3.checkState()
        if pre_value == 2:
            value = True
        else:
            value = False
        add_string = "completed : {}".format(str(value))
        add_widgetitem = QtWidgets.QListWidgetItem(add_string)
        add_widgetitem.setFont(self._print_font)

        for i in range(0, self.listWidget_3.count()):
            item = self.listWidget_3.item(i).text()
            key, sub_value = item.split(" : ")
            if key == "completed":
                pop_row = i
                pop_item = self.listWidget_3.takeItem(pop_row)
                break
        self.listWidget_3.addItem(add_widgetitem)
        self._filters["exclusive"]["completed"] = value

    def AddExclusiveDate(self):
        years_lower = self.dateEdit_3.date().year()
        months_lower = self.dateEdit_3.date().month()
        days_lower = self.dateEdit_3.date().day()
        date_str_lower = "{:04d}-{:02d}-{:02d}".format(years_lower, months_lower, days_lower)
        years_upper = self.dateEdit_4.date().year()
        months_upper = self.dateEdit_4.date().month()
        days_upper = self.dateEdit_4.date().day()
        date_str_upper = "{:04d}-{:02d}-{:02d}".format(years_upper, months_upper, days_upper)
        date_range_str = "{},{}".format(date_str_lower, date_str_upper)
        add_string = "dates : {}".format(date_range_str)
        add_widgetitem = QtWidgets.QListWidgetItem(add_string)
        add_widgetitem.setFont(self._print_font)
        self.listWidget_3.addItem(add_widgetitem)
        self._filters["exclusive"]["dates"].append(date_range_str)

    def AddExclusivePriority(self):
        prior_lower = self.doubleSpinBox_3.value()
        prior_upper = self.doubleSpinBox_4.value()
        priority_range = "{:.2f}-{:.2f}".format(prior_lower,prior_upper)
        add_string = "priorities : {}".format(priority_range)
        add_widgetitem = QtWidgets.QListWidgetItem(add_string)
        add_widgetitem.setFont(self._print_font)
        self.listWidget_3.addItem(add_widgetitem)
        self._filters["exclusive"]["priorities"].append(priority_range)

    def RefreshExclusiveList(self):
        temp_class_list = list()
        temp_cal_list = list()
        temp_num_list = list()
        temp_date_list = list()
        temp_prior_list = list()
        temp_complete = bool()
        for i in range(0, self.listWidget_3.count()):
            item = self.listWidget_3.item(i).text()
            key, sub_val = item.split(" : ")
            if key == "classifications":
                temp_class_list.append(sub_val)
            elif key == "calendars":
                temp_cal_list.append(sub_val)
            elif key == "numbers":
                temp_num_list.append(int(sub_val))
            elif key == "dates":
                temp_date_list.append(sub_val)
            elif key == "priorities":
                temp_prior_list.append(sub_val)
            elif key == "completed":
                if sub_val == "True":
                    temp_complete = True
                else:
                    temp_complete = False

        self._filters["exclusive"]["classifications"] = temp_class_list
        self._filters["exclusive"]["calendars"] = temp_cal_list
        self._filters["exclusive"]["numbers"] = temp_num_list
        self._filters["exclusive"]["dates"] = temp_date_list
        self._filters["exclusive"]["priorities"] = temp_prior_list
        self._filters["exclusive"]["completed"] = temp_complete

    def get_data(self):
        return self._data

    def get_filters(self):
        return self._filters