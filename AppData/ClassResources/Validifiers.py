from ClassResources.File_Handler import File_Handler
import datetime


class validate(object):
    def __init__(self):
        self._field_list_max = ["name", "due date", "i value", "s value", "w value", "priority number", "parameters",
                                "qualifiers", "classification", "calendar", "time range", "display", "selected",
                                "title", "from-links", "to-links", "completed", "calID", "wundID"]

        CalIDs_file = File_Handler("CalendarIDs")
        self._calIDs = CalIDs_file.file_ResourceOpen()

    # validifiers
    def valid_data(self, data):
        # data must be a dictionary
        # data must have all valid item numbers as keys
        # each key must have a valid item associated
        if type(data) is not dict:
            print("Error: Input data is not of type Dict")
            return False
        else:
            for keys in data:
                if self.valid_number(keys) is False:
                    print("Error: Invalid ItemID number")
                    return False
                elif self.valid_item(data[keys], keys) is False:
                    print("Error: invalid item associated with item number")
                    return False
            return True

    def valid_item(self, item_dict, number):
        # valid items have all proper keys or are empty
        # valid items have valid values associated with each key
        for keys in item_dict:
            if keys not in self._field_list_max:
                print("Error: unknown field key")
                return False

        for elements in self._field_list_max:
            if elements not in item_dict:
                return False
                # item_dict[elements] = "INVALID"

        if self.valid_name(item_dict["name"]) is False:
            print("Error: Invalid Name")
            return False
        elif self.valid_date(item_dict["due date"]) is False:
            print("Error: Invalid Due Date")
            return False
        elif self.valid_ISW(item_dict["i value"]) is False:
            print("Error: Invalid I value")
            return False
        elif self.valid_ISW(item_dict["s value"]) is False:
            print("Error: Invalid S value")
            return False
        elif self.valid_ISW(item_dict["w value"]) is False:
            print("Error: Invalid W value")
            return False
        elif self.valid_priority(item_dict["priority number"]) is False:
            print("Error: Invalid Priority Number")
            return False
        elif self.valid_parameter(item_dict["parameters"]) is False:
            print("Error: Invalid Parameters List")
            return False
        elif self.valid_qualifier(item_dict["qualifiers"]) is False:
            print("Error: Invalid Qualifiers List")
            return False
        elif self.valid_classify(item_dict["classification"]) is False:
            print("Error: Invalid Classification")
            return False
        elif self.valid_calendar(item_dict["calendar"]) is False:
            print("Error: Invalid Calendar")
            return False
        elif self.valid_time(item_dict["time range"]) is False:
            print("Error: Invalid Time Range")
            return False
        elif self.valid_select(item_dict["selected"]) is False:
            print("Error: Invalid Selection Value")
            return False
        elif self.valid_display(item_dict["display"]) is False:
            print("Error: Invalid Display Value")
            return False
        elif self.valid_title(item_dict["title"]) is False:
            print("Error: Invalid title Value")
            return False
        elif self.valid_from_links(item_dict["from-links"]) is False:
            print("Error: Invalid from-links list")
            return False
        elif self.valid_to_links(item_dict["to-links"]) is False:
            print("Error: Invalid to-links list")
            return False
        elif self.valid_completed(item_dict["completed"]) is False:
            print("Error: Invalid completion Value")
            return False
        elif self.valid_calID(item_dict["calID"]) is False:
            print("Error: Invalid calID Value")
            return False
        elif self.valid_wundID(item_dict["wundID"]) is False:
            print("Error: Invalid wundID Value")
            return False
        else:
            return True

    def valid_number(self, number):
        # a valid item number is 6 characters long
        # the character at index 3 is '.'
        # all other characters are numbers
        if len(number) != 6:
            print("Error: Invalid ItemID length")
            return False
        elif '.' not in number:
            print("Error: ItemID missing '.'")
            return False
        else:
            number_list = number.split('.')
            if len(number_list[0]) != 3:
                print("Error: First 3 Item ID digits of wrong size")
                return False
            elif number_list[0].isdigit() is False:
                print("Error: non-digit character in first 3 digits of ItemID")
                return False
            elif len(number_list[1]) != 2:
                print("Error: last 2 ItemID digits of wrong size")
                return False
            elif number_list[0].isdigit() is False:
                print("Error: non-digit character in last 2 digits of ItemID")
                return False
            return True

    def valid_name(self, name):
        # a valid name is a string of 30 characters or less
        if len(name) > 30:
            print("Error: Name too long")
            return False
        return True

    def valid_title(self, title):
        if (self.valid_number(title[0:6])) and (self.valid_name(title[9:])) and (title[6:9] == " - "):
            return True
        return False

    def matching_title(self, title, number, name):
        if (title[0:6] == number) and (title[9:] == name) and (title[6:9] == " - "):
            return True
        return False

    def valid_date(self, in_date):
        # a valid date is of form yyyy-mm-dd
        # a valid date is of length 10
        # the character at index 4 and 7 is '-'
        # all other characters are numbers
        # yyyy must be convertable to an integer
        # mm must be an int between 1 and 12
        # dd must be an int between 1 and 31
        if len(in_date) != 10:
            print("Error: Invalid Date length")
            return False
        elif '-' not in in_date:
            print("Error: Date missing '-' characters")
            return False
        else:
            date_list = in_date.split('-')
            if len(date_list[0]) != 4:
                print("Error: Invalid length of year component")
                return False
            elif date_list[0].isdigit() is False:
                print("Error: non-digit character in year component")
                return False
            elif len(date_list[1]) != 2:
                print("Error: Invalid length of month component")
                return False
            elif int(date_list[1]) > 12 or int(date_list[1]) < 1:
                print("Error: Invalid integer value for month")
                return False
            elif date_list[1].isdigit() is False:
                print("Error: non-digit character in month component")
                return False
            elif len(date_list[2]) != 2:
                print("Error: Invalid length of month component")
                return False
            elif int(date_list[2]) > 31 or int(date_list[2]) < 1:
                # does not account for monthly changes to value limit
                print("Error: Invalid integer value for day")
                return False
            elif date_list[2].isdigit() is False:
                print("Error: non-digit character in day component")
                return False
            return True

    def valid_ISW(self, value):
        # a valid isw value is a int or float greater than 0
        if (type(value) is not float) and (type(value) is not int):
            print("Error: ISW value is neither float nor int")
            return False
        elif value < 0:
            print("Error: ISW value less than 0")
            return False
        return True

    def valid_parameter(self, parameter):
        # a valid parameter is a string 40 characters long
        if type(parameter) is not list:
            return False
        elif len(parameter) < 1:
            return True
        else:
            for element in parameter:
                if len(element) > 45:
                    print("Error: Element of parameter list exceeded length limit")
                    return False
            return True

    def valid_priority(self, value):
        # a valid priority is a float number between 0 and 10
        if type(value) is not float:
            print("Error: Priority number is not a float")
            return False
        elif value < 0 or value > 10:
            print("Error: Priority Number less than 0 or greater than 10")
            return False
        return True

    def valid_qualifier(self, qualifier):
        # a valid qualifier is a string 40 characters long
        if type(qualifier) is not list:
            return False
        elif len(qualifier) < 1:
            return True
        else:
            for element in qualifier:
                if len(element) > 42:
                    print("Error: Element of qualifier list exceeded length limit")
                    return False
            return True

    def valid_from_links(self, from_links):
        if type(from_links) is not list:
            return False
        elif len(from_links) < 1:
            return True
        else:
            for element in from_links:
                if not self.valid_title(element):
                    print("Error: Element of from-links list exceeded length limit")
                    return False
            return True

    def valid_to_links(self, to_links):
        if type(to_links) is not list:
            return False
        elif len(to_links) < 1:
            return True
        else:
            for element in to_links:
                if not self.valid_title(element):
                    print("Error: Element of to-links list exceeded length limit")
                    return False
            return True

    def valid_classify(self, classify):
        # A valid classification is a string in the CFPTVO with modifier S and/or W
        # A valid classification is no more than 4 characters long
        classify_list = ["C", "F", "P", "T", "V", "O", "SC", "SF", "SP", "ST", "SV", "SO", "CW", "FW", "PW", "TW", "VW",
                         "OW", "SCW", "SFW", "SPW", "STW", "SVW", "SOW", "AC", "AF", "AP", "AT", "AV", "AO", "ASC",
                         "ASF", "ASP", "AST", "ASV", "ASO", "ACW", "AFW", "APW", "ATW", "AVW", "AOW", "ASCW", "ASFW",
                         "ASPW", "ASTW", "ASVW", "ASOW"]
        if classify.isupper() is False:
            print("Error: classification is of wrong case")
            return False
        elif len(classify) > 4:
            print("Error: classification is of too large")
            return False
        else:
            if classify not in classify_list:
                return False
            # for char in classify:
            #     if char not in "CFPTVOSWA":
            #         print("Error: Unexpected character in classification")
            #         return False
            #     elif classify.count(char) > 1:
            #         print("Error: Recurring character in classification")
            #         return False
            return True

    def valid_calendar(self, calendar):
        # A valid calendar is one of the keys in the calendarIDs list
        # A valid calnedar is no more than 20 characters
        CalIDs = self._calIDs
        if calendar not in CalIDs:
            print("Error: Unknown Calendar")
            return False
        return True

    def valid_time(self, timerange):
        # a valid time range is of size 29 exactly
        # a valid time range is '15:00:00-04:00,16:50:00-04:00'
        #                       '0123456789A123456789A12345678'
        # indexes 2, 5, 11, 17, 20, 26 are ':'
        # indexes 8, 23 are '-' , only accepts '-' not '+'
        # index 14 is ','
        # indexes 0+1 and 15+16 are an 0<=int<24
        # indexes 9+10 and 24+25 are an 0<=int<15
        # indexes 3+4, 6+7, 12+13, 18+19, 21+22, 27+28 are 0<=int<60
        if len(timerange) != 29:
            print("Error: Invalid time range length")
            return False
        else:
            if (timerange[2] is not ':') or (timerange[5] is not ':') or (timerange[11] is not ':') or \
                    (timerange[17] is not ':') or (timerange[20] is not ':') or (timerange[26] is not ':'):
                print("Error: time range missing ':' characters")
                return False
            elif (timerange[8] is not '-') or (timerange[23] is not '-'):
                print("Error: time range  missing '-' characters")
                return False
            elif timerange[14] is not ',':
                print("Error: time range missing ',' characters")
                return False
            elif ((int(timerange[0:1]) >= 24) or (int(timerange[0:1]) < 0)) or \
                    ((int(timerange[15:16]) >= 24) or (int(timerange[15:16]) < 0)):
                print("Error: invalid integer value for hours")
                return False
            elif ((int(timerange[9:10]) >= 15) or (int(timerange[9:10]) < 0)) or \
                    ((int(timerange[24:25]) >= 15) or (int(timerange[24:25]) < 0)):
                print("Error: invalid integer value for timezone hours")
                return False
            elif ((int(timerange[3:4]) >= 60) or (int(timerange[3:4]) < 0)) or \
                    ((int(timerange[6:7]) >= 60) or (int(timerange[6:7]) < 0)) or \
                    ((int(timerange[12:13]) >= 60) or (int(timerange[12:13]) < 0)) or \
                    ((int(timerange[18:19]) >= 60) or (int(timerange[18:19]) < 0)) or \
                    ((int(timerange[21:22]) >= 60) or (int(timerange[21:22]) < 0)) or \
                    ((int(timerange[27:28]) >= 60) or (int(timerange[27:28]) < 0)):
                print("Error: invalid integer value for minutes or seconds")
                return False
            return True

    def valid_select(self, value):
        # a valid selection value is a bool type
        if type(value) is not bool:
            return False
        return True

    def valid_display(self, value):
        # a valid display value is a bool type
        if type(value) is not bool:
            return False
        return True

    def valid_completed(self, value):
        if type(value) is not bool:
            return False
        return True

    def valid_calID(self, calID):
        # type string
        # 5 < len < 1024
        # chars 0-9, a-f
        hex_chars = "123456789abcdefghijklmnopqrstuv"
        if calID == "none":
            return True
        elif calID == "INVALID":
            return False
        elif 5 < len(calID) < 1024:
            for char in calID:
                if char not in hex_chars:
                    return False
            return True

    def valid_wundID(self, wundID):
        # all numbers, 3720068389
        # len == 10
        if wundID == "none":
            return True
        elif str(wundID).isdecimal() and len(wundID) == 10:
            return True
        else:
            return False

    def valid_display_list(self, in_list, data):
        # a valid display value is a bool type
        for elements in in_list:
            if elements not in data:
                print("Error: invalid ItemID specified in display list")
                return False
        return True

    def valid_select_list(self, in_list, data):
        # a valid display value is a bool type
        for elements in in_list:
            if elements not in data:
                print("Error: invalid ItemID specified in selection list")
                return False
        return True

    def valid_arrange_list(self, in_list, data):
        # a valid display value is a bool type
        for elements in in_list:
            if elements not in data:
                print("Error: invalid ItemID specified in arrangement list")
                return False
        return True

    def valid_fields(self, in_list):
        # a valid display value is a bool type
        for elements in in_list:
            if elements not in self._field_list_max:
                print("Error: invalid field specified in fields")
                return False
        return True

    def valid_field(self, field):
        # a valid display value is a bool type
        if field in self._field_list_max:
            return True
        return False

    def valid_sort(self, SortString):
        # a valid display value is a bool type
        if SortString in ["name", "due", "priority", "number", "none"]:
            return True
        return False


