import smtplib
from ClassResources.Task_Data import Task_Data
from email.mime.multipart import MIMEMultipart
from ClassResources.File_Handler import File_Handler
from email.mime.text import MIMEText


class Send_Printer(object):
    def __init__(self, destination="console", length="all", subject="Database Information List"):
        self._valid_destinations = ["console", "textfile"]
        self._formats = {"ItemID": {"format": "{:^6}: ", "width": 8}, "name": {"format": "{:^34}|", "width": 35},
                         "due date": {"format": "{:^10}|", "width": 11}, "i value": {"format": "{:^8}|", "width": 9},
                         "s value": {"format": "{:^8}|", "width": 9}, "w value": {"format": "{:^8}|", "width": 9},
                         "priority number": {"format": "{:^10}|", "width": 11},
                         "parameters": {"format": "{:^47}|", "width": 48},
                         "qualifiers": {"format": "{:^44}|", "width": 45},
                         "classification": {"format": "{:^7}|", "width": 8},
                         "calendar": {"format": "{:^20}|", "width": 21},
                         "time range": {"format": "{:^32}|", "width": 33},
                         "display": {"format": "{:^10}|", "width": 11},
                         "selected": {"format": "{:^10}|", "width": 11}, "title": {"format": "{:^44}|", "width": 45},
                         "from-links": {"format": "{:^44}|", "width": 45},
                         "to-links": {"format": "{:^44}|", "width": 45},
                         "completed": {"format": "{:^10}|", "width": 11}, "calID": {"format": "", "width": 0},
                         "wundID": {"format": "", "width": 0}}

            
        if self.valid_destination(destination):
            self._destination = destination
        else:
            self._destination = "console"

        if self.valid_length(length):
            self._length = length
        else:
            self._length = "all"

        self._line_width = 0
        self._leadingID = True
        self._subject = subject
        self._out_string = str()

    def valid_length(self, length):
        if (str(length).isdigit() is True) or (str(length) == "all"):
            return True
        else:
            return False

    def valid_destination(self, destination):
        if destination in self._valid_destinations:
            return True
        else:
            return False

    def set_length(self, length):
        if self.valid_length(length):
            self._length = length
        else:
            self._length = "all"

    def get_out_string(self):
        return self._out_string

    def leadingID_on(self):
        self._leadingID = True

    def leadingID_off(self):
        self._leadingID = False

    def set_subject(self, subject):
        self._subject = subject

    def set_destination(self, destination):
        if self.valid_destination(destination):
            self._destination = destination
        else:
            self._destination = "console"

    def route_printer(self):
        """takes input of a formatted string and a string indicating where to send it
        prints contents of in_str to destination of dec_str
        return None"""
        # make use of of self._out_string and self._destination, possibly self._subject or
        in_str = self._out_string
        dec_str = self._destination
        decision = dec_str
        if decision.lower() == "console":
            print(in_str)
        elif decision.lower() == "textfile":
            temp_file = File_Handler(self._subject)
            temp_file.file_TextPrint(self._out_string)
        else:
            print("Invalid input, please try again")

    def print_header(self, data):
        format_list = list()
        headers_list = list()
        if self._leadingID:
            format_list.append(self._formats["ItemID"])
            headers_list.append("ItemID")

        fields_list = data.get_fields()
        for elements in fields_list:
            format_list.append(self._formats[elements])
            headers_list.append(elements)

        header_string = ""
        for i in range(0, len(format_list)):
            if headers_list[i] == "classification":
                header_string += format_list[i]["format"].format("class")
            elif headers_list[i] == "priority number":
                header_string += format_list[i]["format"].format("priority")
            else:
                header_string += format_list[i]["format"].format(headers_list[i])

        width_sum = 0
        for items in format_list:
            width_sum += items["width"]

        self._line_width = width_sum

        header_string += "\n"
        header_string += "="*width_sum

        return header_string

    def get_row_info(self, format_list, fields_list):
        # fields list is a list of items
        max_rows = 0
        row_info = dict()
        for elements in fields_list:
            if type(elements) is list:
                temp_len = len(elements)
                if temp_len > max_rows:
                    # find maximum number of rows needed to print
                    max_rows = temp_len

        depth_list = list()
        for elements in fields_list:
            if type(elements) is list:
                # keep a list of list lengths
                depth_list.append(len(elements))

        # i is the row number starting at 1
        for i in range(1, max_rows+1):
            row_key = "row" + str(i)
            row_info[row_key] = dict()
            k = 0  # block key index, list #
            li = 0
            space_sum = 0
            for j in range(0, len(format_list)):
                if type(fields_list[j]) is list and depth_list[li] >= i:
                    # if the element is a list with depth >= current row number
                    # create a new space key and set the sum
                    # everything preceding this element is space, then fill in block width
                    if space_sum > 0:
                        space_key = "space" + str(k)
                        row_info[row_key][space_key] = space_sum
                        space_sum = 0
                        k += 1
                    block_key = "block" + str(k)
                    row_info[row_key][block_key] = format_list[j]["width"]
                    k += 1
                    li += 1
                elif type(fields_list[j]) is list:
                    # if current list has depth less than i, move on to next list
                    space_sum += format_list[j]["width"]
                    li += 1
                else:
                    space_sum += format_list[j]["width"]

        return row_info

    def print_item(self, data, item_number):
        format_list = list()
        items_list = list()
        if self._leadingID:
            # controls whether the number is printed in front by default
            format_list.append(self._formats["ItemID"])
            items_list.append(item_number)

        fields_list = data.get_fields()
        true_data = data.get_data()
        for elements in fields_list:
            # add the format blueprint to a list for each type of field
            # add the item itself to items_list
            format_list.append(self._formats[elements])
            items_list.append(true_data[item_number][elements])

        lists_list = list()
        lists_formats = list()
        index = 0
        for elements in items_list:
            if type(elements) is list:
                # if the item is a list it will be placed in to lists_list
                # format for particular list stored in lists_formats at same index
                lists_list.append(elements)
                lists_formats.append(format_list[index])
            index += 1

        row_info = self.get_row_info(format_list, items_list)
        # get back a dict where every row has keys for when to call a space and when to format a block, in the lists

        # first row printed
        print_string = ""
        for i in range(0, len(format_list)):
            if type(items_list[i]) is list and len(items_list[i]) > 0:
                print_string += format_list[i]["format"].format(items_list[i][0])
            elif type(items_list[i]) is list and len(items_list[i]) == 0:
                print_string += format_list[i]["format"].format("[]")
            elif type(items_list[i]) is int or type(items_list[i]) is float:
                temp_string = "{:.2f}".format(items_list[i])
                print_string += format_list[i]["format"].format(temp_string)
            elif type(items_list[i]) is bool:
                temp_string = str(items_list[i])
                print_string += format_list[i]["format"].format(temp_string)
            else:
                print_string += format_list[i]["format"].format(items_list[i])

        print_string += "\n"

        row_string = ""
        # row 2-n
        row_index = 1
        for row_keys in row_info:
            # print(row_keys)
            if row_keys == "row1":
                # already printed first row
                row_index += 1
                continue
            else:
                list_index = 0  # the current list to be formatted
                row_order = list(row_info[row_keys].keys())
                # sorted(row_order, key=lambda string: string[-1])
                for i in range(0, len(row_order)):
                    # doesn't know which list item to print in a block, needs to use list index and depth to find out
                    # if the list at the current index is too shallow, know to move on to the next list to fill block
                    # two cases for blocks, block following block or block following space
                    # two cases for space, Preceding a block or going to the
                    current_line_key = row_order[i]
                    while list_index < len(lists_list):
                        if len(lists_list[list_index]) < row_index:
                            list_index += 1
                        else:
                            break

                    if (row_order[i-1][0:5] == "space") and (current_line_key[0:5] == "block"):
                        # block preceded by space, add "|"
                        row_string += "|"
                        row_string += lists_formats[list_index]["format"].format(lists_list[list_index][row_index-1])
                        list_index += 1
                    elif (row_order[i-1][0:5] == "block") and (current_line_key[0:5] == "block"):
                        # block preceded by block
                        row_string += lists_formats[list_index]["format"].format(lists_list[list_index][row_index-1])
                        list_index += 1
                    elif (row_order[i+1][0:5] == "block") and (current_line_key[0:5] == "space"):
                        # space preceding block, 1 short
                        row_string += " "*(row_info[row_keys][current_line_key]-1)
                    elif (i == len(row_order)-1) and (current_line_key[0:5] == "space"):
                        # terminating space
                        row_string += " "*row_info[row_keys][current_line_key]

                row_index += 1
            row_string += "\n"

        # row_string = row_string[:-1]
        width_sum = 0
        for items in format_list:
            width_sum += items["width"]

        print_string += row_string

        return print_string

    def print_divider(self):
        div_string = "-" * self._line_width
        # div_string += "\n"
        return div_string

    def format_string(self, data, print_list):
        """takes input of _data, _arrange_list, field_list, a length string and a destination string
        formats contents of _data into a single string for printing, send string to print_decide
        return None"""

        if self._length == "all":
            # set length to full len of list
            printer_length = len(print_list)
        else:
            # otherwise set length to be set length
            printer_length = int(self._length)

        header_string = self.print_header(data)

        j = printer_length
        printer_string = ""
        for items in print_list:
            # control number of items to be printed
            if j == 0:
                break
            else:
                printer_string += self.print_item(data, items)
                # printer_string += "\n"
                printer_string += self.print_divider()
                printer_string += "\n"
                j -= 1

        self._out_string = header_string + "\n" + printer_string
        # self.route_printer()

