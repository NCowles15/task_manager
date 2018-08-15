import datetime
from datetime import date
import numpy
from operator import itemgetter
from ClassResources.Validifiers import validate
from ClassResources.File_Handler import File_Handler


class Task_Data(object):
    def __init__(self, data):
        self._field_list_max = ["name", "due date", "i value", "s value", "w value", "priority number", "parameters",
                                "qualifiers", "classification", "calendar", "time range", "display", "selected",
                                "title", "from-links", "to-links", "completed", "calID", "wundID"]
        self._field_list = list()
        self._valid = validate()

        if self._valid.valid_data(data):
            self._data = data

        else:
            defect_file = File_Handler("Defectives File")
            data = self.make_valid_data(data, defect_file)
            self._data = data

        self._arrange_list = list()
        self._selection_list = list()
        self._display_list = list()
        self._printables_list = list()

        # self.reset_display()
        self.init_display()
        self.reset_selection()

        for obj_num in self._data:
            if self._data[obj_num]["selected"]:
                self._selection_list.append(obj_num)
            self._arrange_list.append(obj_num)
        self.set_printables()

    # getters
    def get_data(self):
        return self._data

    def get_item(self, item_num):
        return self._data[item_num]

    def get_display(self):
        return self._display_list
    
    def get_selection(self):
        return self._selection_list

    def get_fields_max(self):
        return self._field_list_max

    def get_fields(self):
        return self._field_list

    def get_arrangement(self):
        return self._arrange_list

    def get_printables(self):
        return self._printables_list

    # setters
    def set_data(self, data):
        if self._valid.valid_data(data):
            self._data = data
            # self.reset_display()
            self.reset_selection()

            for obj_num in self._data:
                if self._data[obj_num]["display"]:
                    self._display_list.append(obj_num)
                if self._data[obj_num]["selected"]:
                    self._selection_list.append(obj_num)
                self._arrange_list.append(obj_num)
            self.set_printables()

    def set_item(self, item_num, item_dict):
        if self._valid.valid_item(item_dict, item_num) and self._valid.valid_number(item_num):
            self._data[item_num] = item_dict
            if item_dict["display"]:
                self.show_item(item_num)
            else:
                self.hide_item(item_num)
            if item_dict["selected"]:
                self.select_item(item_num)
            else:
                self.deselect_item(item_num)

            if item_num in self._arrange_list:
                return None
            else:
                self._arrange_list.append(item_num)
                # self.arrange_data("priority")

    def set_display(self, display):
        if self._valid.valid_display_list(display, self._data):
            self._display_list = display
            for obj_num in self._data:
                if self._data[obj_num]["display"] is True and obj_num not in display:
                    self._data[obj_num]["display"] = False
                elif self._data[obj_num]["display"] is False and obj_num in display:
                    self._data[obj_num]["display"] = True
    
    def set_selection(self, selection):
        if self._valid.valid_select_list(selection, self._data):
            self._selection_list = selection
            for obj_num in self._data:
                if self._data[obj_num]["selected"] is True and obj_num not in selection:
                    self._data[obj_num]["selected"] = False
                elif self._data[obj_num]["selected"] is False and obj_num in selection:
                    self._data[obj_num]["selected"] = True

    def set_fields(self, fields):
        if self._valid.valid_fields(fields):
            self._field_list = fields

    def set_arrangement(self, arrangement):
        if self._valid.valid_arrange_list(arrangement, self._data):
            self._arrange_list = arrangement
            self.set_printables()

    def set_printables(self):
        self.priority_assign()
        printable_list = list()
        for element in self._arrange_list:
            if element in self._display_list:
                printable_list.append(element)
        self._printables_list = printable_list

    # resetters
    def reset_display(self):
        for obj_num in self._data:
            self._data[obj_num]["display"] = True
            self._display_list.append(obj_num)

    def reset_selection(self):
        self._selection_list = list()
        for obj_num in self._data:
            self._data[obj_num]["selected"] = False

    def reset_arrangement(self):
        for obj_num in self._data:
            self._arrange_list.append(obj_num)

    def reset_fields(self):
        self._field_list = list()

    def reset_links(self):
        for keys in self._data:
            self._data[keys]["from-links"] = list()
        for keys in self._data:
            for links in self._data[keys]["to-links"]:
                link_number = links[:6]
                if link_number in self._data:
                    self._data[link_number]["from-links"].append(self._data[keys]["title"])

    # granulars
    def remove_item(self, item_num):
        pop_dict = self._data[item_num]
        if item_num in self._display_list:
            del_ind = self._display_list.index(item_num)
            del self._display_list[del_ind]
        if item_num in self._selection_list:
            del_ind = self._selection_list.index(item_num)
            del self._selection_list[del_ind]
        if item_num in self._arrange_list:
            del_ind = self._arrange_list.index(item_num)
            del self._arrange_list[del_ind]
        del self._data[item_num]
        return pop_dict

    def select_item(self, item_num):
        self._data[item_num]["selected"] = True
        if item_num not in self._selection_list:
            self._selection_list.append(item_num)

    def select_all(self):
        for key in self._data:
            self._data[key]["selected"] = True
            self._selection_list.append(key)

    def deselect_item(self, item_num):
        self._data[item_num]["selected"] = False
        if item_num in self._selection_list:
            del_ind = self._selection_list.index(item_num)
            del self._selection_list[del_ind]

    def deselect_all(self):
        for key in self._data:
            self._data[key]["selected"] = False
            self._selection_list = list()

    def init_display(self):
        for obj_num in self._data:
            if self._data[obj_num]["display"]:
                self._display_list.append(obj_num)

    def hide_item(self, item_num):
        self._data[item_num]["display"] = False
        if item_num in self._display_list:
            del_ind = self._display_list.index(item_num)
            del self._display_list[del_ind]

    def show_item(self, item_num):
        self._data[item_num]["display"] = True
        if item_num not in self._display_list:
            self._display_list.append(item_num)

    def add_field(self, field):
        if field in self._field_list_max:
            self._field_list.append(field)

    def remove_field(self, field):
        del_ind = self._field_list.index(field)
        self._field_list.pop(del_ind)

    # filters
    def main_filter(self, filter_dict):
        if filter_dict["mode"] == "manual":
            self.manual_filter(filter_dict)
        elif filter_dict["mode"] == "inclusive":
            self.inclusive_filter(filter_dict)
        elif filter_dict["mode"] == "exclusive":
            self.exclusive_filter(filter_dict)

    def manual_filter(self, filter_dict):
        temp_list = filter_dict["manual"]
        for keys in self._data:
            if keys in temp_list:
                self.show_item(keys)
            else:
                self.hide_item(keys)

    def inclusive_filter(self, filter_dict):
        temp_dict = filter_dict["inclusive"]
        for keys in self._data:
            if (self._data[keys]["classification"] in temp_dict["classifications"]) \
                    and (self._data[keys]["calendar"] in temp_dict["calendars"]) \
                    and (int(keys[0:2]) in temp_dict["numbers"]) \
                    and (not(self._data[keys]["completed"]) or temp_dict["completed"]) \
                    and (self.in_priority_range(self._data[keys]["priority number"], temp_dict["priorities"])) \
                    and (self.in_date_range(self._data[keys]["due date"], temp_dict["dates"])):
                self.show_item(keys)
            else:
                self.hide_item(keys)

    def exclusive_filter(self, filter_dict):
        temp_dict = filter_dict["exclusive"]
        for keys in self._data:
            if (self._data[keys]["classification"] in temp_dict["classifications"]) \
                    or (self._data[keys]["calendar"] in temp_dict["calendars"]) \
                    or (int(keys[0:2]) in temp_dict["numbers"]) \
                    or (self._data[keys]["completed"] and temp_dict["completed"]) \
                    or (self.in_priority_range(self._data[keys]["priority number"], temp_dict["priorities"])) \
                    or (self.in_date_range(self._data[keys]["due date"], temp_dict["dates"])):
                self.hide_item(keys)
            else:
                self.show_item(keys)

    def in_priority_range(self, priority, priority_ranges):
        for element in priority_ranges:
            range_list = element.split("-")
            lower_prior = float(range_list[0])
            upper_prior = float(range_list[1])
            if (priority >= lower_prior) and (priority <= upper_prior):
                return True
        return False

    def in_date_range(self, in_date, date_ranges):
        for element in date_ranges:
            lower_date, upper_date = element.split(",")
            date_list = in_date.split("-")
            lower_date_list = lower_date.split("-")
            upper_date_list = upper_date.split("-")
            d1 = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
            d2 = date(int(lower_date_list[0]), int(lower_date_list[1]), int(lower_date_list[2]))
            d3 = date(int(upper_date_list[0]), int(upper_date_list[1]), int(upper_date_list[2]))
            if (d1 >= d2) and (d1 <= d3):
                return True
        return False


    # defaults
    def make_valid_data(self, data, garbage_file):
        # data must be a dictionary
        # data must have all valid item numbers as keys
        # each key must have a valid item associated
        if type(data) is not dict:
            data = dict()
            return data
        else:
            broken_items = dict()
            for keys in data:
                if self._valid.valid_number(keys) is False:
                    broken_items[keys] = data[keys]
                    del data[keys]
                elif self._valid.valid_item(data[keys], keys) is False:
                    self.make_valid_item(data[keys], keys)
            if broken_items != dict():
                garbage_file.file_Recycle(broken_items)
            return data

    def make_valid_item(self, item_dict, number):
        # valid items have all proper keys or are empty
        # valid items have valid values associated with each key
        for keys in item_dict:
            if keys not in self._field_list_max:
                del item_dict[keys]

        for elements in self._field_list_max:
            if elements not in item_dict:
                item_dict[elements] = "INVALID"

        while True:
            if self._valid.valid_name(item_dict["name"]) is False:
                self.make_valid_name(item_dict)
                continue
            if self._valid.valid_date(item_dict["due date"]) is False:
                self.make_valid_date(item_dict)
                continue
            if self._valid.valid_ISW(item_dict["i value"]) is False:
                self.make_valid_I_value(item_dict)
                continue
            if self._valid.valid_ISW(item_dict["s value"]) is False:
                self.make_valid_S_value(item_dict)
                continue
            if self._valid.valid_ISW(item_dict["w value"]) is False:
                self.make_valid_W_value(item_dict)
                continue
            if self._valid.valid_priority(item_dict["priority number"]) is False:
                self.make_valid_priority(item_dict)
                continue
            if self._valid.valid_parameter(item_dict["parameters"]) is False:
                self.make_valid_parameter(item_dict)
                continue
            if self._valid.valid_qualifier(item_dict["qualifiers"]) is False:
                self.make_valid_qualifier(item_dict)
                continue
            if self._valid.valid_classify(item_dict["classification"]) is False:
                self.make_valid_classify(item_dict)
                continue
            if self._valid.valid_calendar(item_dict["calendar"]) is False:
                self.make_valid_calendar(item_dict)
                continue
            if self._valid.valid_time(item_dict["time range"]) is False:
                self.make_valid_time(item_dict)
                continue
            if self._valid.valid_select(item_dict["selected"]) is False:
                self.make_valid_select(item_dict)
                continue
            if self._valid.valid_display(item_dict["display"]) is False:
                self.make_valid_display(item_dict)
                continue
            if self._valid.valid_title(item_dict["title"]) is False:
                self.make_valid_title(item_dict, number)
                continue
            if self._valid.matching_title(item_dict["title"], number, item_dict["name"]) is False:
                self.make_valid_title(item_dict, number)
                continue
            if self._valid.valid_from_links(item_dict["from-links"]) is False:
                self.make_valid_from_links(item_dict)
                continue
            if self._valid.valid_to_links(item_dict["to-links"]) is False:
                self.make_valid_to_links(item_dict)
                continue
            if self._valid.valid_completed(item_dict["completed"]) is False:
                self.make_valid_completed(item_dict)
                continue
            if self._valid.valid_calID(item_dict["calID"]) is False:
                self.make_valid_calID(item_dict)
                continue
            if self._valid.valid_wundID(item_dict["wundID"]) is False:
                self.make_valid_wundID(item_dict)
                continue
            break

    def make_valid_name(self, item_dict):
        # a valid name is a string of 30 characters or less
        item_dict["name"] = "Default Name"

    def make_valid_date(self, item_dict):
        # a valid date is of form yyyy-mm-dd
        today_str = str(datetime.datetime.today())
        due_date, today_time = today_str.split()
        item_dict["due date"] = due_date

    def make_valid_I_value(self, item_dict):
        # a valid isw value is a int or float greater than 0
        item_dict["i value"] = 1

    def make_valid_S_value(self, item_dict):
        item_dict["s value"] = 1.0

    def make_valid_W_value(self, item_dict):
        item_dict["w value"] = 1

    def make_valid_parameter(self, item_dict):
        # a valid parameter is a string 40 characters long
        item_dict["parameters"] = list()

    def make_valid_priority(self, item_dict):
        # a valid priority is a float number between 0 and 10
        item_dict["priority number"] = 10.0

    def make_valid_qualifier(self, item_dict):
        # a valid qualifier is a string 40 characters long
        item_dict["qualifiers"] = list()

    def make_valid_classify(self, item_dict):
        # A valid classification is a string in the CFPTVO with modifier S and/or W
        # A valid classification is no more than 3 characters long
        item_dict["classification"] = "O"

    def make_valid_calendar(self, item_dict):
        item_dict["calendar"] = "tactical"

    def make_valid_time(self, item_dict):
        item_dict["time range"] = "22:00:00-05:00,23:00:00-05:00"

    def make_valid_select(self, item_dict):
        item_dict["selected"] = False

    def make_valid_display(self, item_dict):
        item_dict["display"] = True

    def make_valid_title(self, item_dict, number):
        item_dict["title"] = number + " - " + item_dict["name"]

    def make_valid_from_links(self, item_dict):
        item_dict["from-links"] = list()

    def make_valid_to_links(self, item_dict):
        item_dict["to-links"] = list()

    def make_valid_completed(self, item_dict):
        item_dict["completed"] = False

    def make_valid_calID(self, item_dict):
        item_dict["calID"] = "none"

    def make_valid_wundID(self, item_dict):
        item_dict["wundID"] = "none"


    # prioritize in place
    def priority_assign(self):
        """takes input of _data 
        changes _data in place, updating priority to reflect current datetime
        return None"""
        today_str = str(datetime.datetime.today())
        today_date, today_time = today_str.split()
        for key in self._data:
            due = self._data[key]["due date"]
            i = int(self._data[key]["i value"])
            s = int(self._data[key]["s value"])
            w = int(self._data[key]["w value"])
            factor = (self.date_distance(today_date, due))-(i*s*w*.0001)
            number = float(10/(1+numpy.exp(-1.5*(factor-5))))
            self._data[key]["priority number"] = number

    def date_distance(self, date1, date2):
        """Takes in two date objects 
        finds the date difference between two dates in days
        return difference"""
        date1_list = date1.split('-')
        date2_list = date2.split('-')
        d1 = date(int(date1_list[0]), int(date1_list[1]), int(date1_list[2]))
        d2 = date(int(date2_list[0]), int(date2_list[1]), int(date2_list[2]))
        diff = (d2-d1).days
        return diff

    # reshape arrange_list
    def arrange_data(self, sort_type="none"): 
        """takes input of _data, and a decision string
        sets the _arrangement_list
        return _arrangement_list"""
        self.priority_assign()
        tup_list = list()
        self._arrange_list = list()
        if sort_type.lower() == "name":
            for obj_num in self._data:
                tup = tuple([obj_num, self._data[obj_num]["name"]])
                tup_list.append(tup)
            tup_list = sorted(tup_list, key=itemgetter(1))
            for element in tup_list:
                self._arrange_list.append(element[0])
        elif sort_type.lower() == "due":
            for obj_num in self._data:
                tup = tuple([obj_num, self._data[obj_num]["due date"]])
                tup_list.append(tup)
            tup_list = sorted(tup_list, key=itemgetter(1))
            for element in tup_list:
                self._arrange_list.append(element[0])
        elif sort_type.lower() == "priority":
            for obj_num in self._data:
                tup = tuple([obj_num, self._data[obj_num]["priority number"]])
                tup_list.append(tup)
            tup_list = sorted(tup_list, key=itemgetter(1))
            for element in tup_list:
                self._arrange_list.append(element[0])
        elif sort_type.lower() == "number":
            self._arrange_list = sorted(list(self._data.keys()))
        elif sort_type.lower() == "none":
            self.reset_arrangement()
        self.set_printables()

