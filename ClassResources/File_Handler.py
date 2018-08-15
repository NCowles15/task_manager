import json
import ast
import os
from os import listdir
from os.path import isfile, join


class File_Handler(object):
    def __init__(self, title="default"):
        self._cwd = os.getcwd()
        self._title = title
        self._TextPath = "TextFiles"
        self._DataPath = "DataFiles"
        self._MapPath = "MapFiles"
        self._ResourcePath = "AlgoResources"
        self._RecylcePath = "Recycler"
        self._PrintPath = "PrintedFiles"
        self._UsersPath = "UserFiles"
        self._PathsPath = "PathsFiles"

    def set_title(self, title):
        self._title = title

    def get_title(self):
        return self._title

    def file_ResourceOpen(self):
        jsons_path = os.path.join(self._cwd, self._ResourcePath)
        file_str = os.path.join(jsons_path, self._title + ".json")
        # file_str = self._title + ".json"
        with open(file_str) as fp:
            file_dict = json.load(fp)
        fp.close()
        return file_dict

    def file_UserOpen(self):
        jsons_path = os.path.join(self._cwd, self._UsersPath)
        file_str = os.path.join(jsons_path, self._title + ".json")
        # file_str = self._title + ".json"
        with open(file_str) as fp:
            file_dict = json.load(fp)
        fp.close()
        return file_dict

    def file_UserSave(self, save_dict):
        jsons_path = os.path.join(self._cwd, self._UsersPath)
        file_str = os.path.join(jsons_path, self._title + ".json")
        # file_str = self._title + ".json"
        with open(file_str, "w+") as fp:
            json.dump(save_dict, fp)
        fp.close()

    def file_DataOpen(self):
        jsons_path = os.path.join(self._cwd, self._DataPath)
        file_str = os.path.join(jsons_path, self._title + ".json")
        # file_str = self._title + ".json"
        with open(file_str) as fp:
            file_dict = json.load(fp)
        fp.close()
        return file_dict

    def file_DataSave(self, save_dict):
        jsons_path = os.path.join(self._cwd, self._DataPath)
        file_str = os.path.join(jsons_path, self._title + ".json")
        # file_str = self._title + ".json"
        with open(file_str, "w+") as fp:
            json.dump(save_dict, fp)
        fp.close()
        
    def file_DataOut(self, in_dict, file_name):
        jsons_path = os.path.join(self._cwd, self._DataPath)
        file_str = os.path.join(jsons_path, file_name + ".json")
        # file_str = file_name + ".json"
        out_dict = dict()
        for key in in_dict:
            if in_dict[key]["selected"]:
                out_dict[key] = in_dict[key]

        with open(file_str, "w+") as fp:
            json.dump(out_dict, fp)
        fp.close()
        
    def file_TextOpen(self):
        texts_path = os.path.join(self._cwd, self._TextPath)
        file_str = os.path.join(texts_path, self._title + ".txt")
        # file_str = self._title + ".txt"
        while True:
            try:
                fp = open(file_str, "r")
                break
            except IOError:
                print("Invalid file name, please try again")
                file_str = input("Input Text File Name: ")
                file_str = file_str + "txt"
                continue
        
        file_dict = dict()
        for line in fp:
            temp_line = ast.literal_eval(line)
            temp = list(temp_line.keys())
            for i in range(0, len(temp)):
                temp_num = temp[i]
                file_dict[temp_num] = temp_line[temp_num]
        fp.close()
        return file_dict

    def file_TextSave(self, in_dict):
        texts_path = os.path.join(self._cwd, self._TextPath)
        file_str = os.path.join(texts_path, self._title + ".txt")
        # file_str = self._title + ".txt"
        fp = open(file_str, "w+")
        out_str = ""
        for key in in_dict:
            temp_dict = dict()
            temp_dict[key] = in_dict[key]
            temp_dict_str = str(temp_dict)
            out_str = out_str + temp_dict_str + '\n'
        fp.write(out_str)
        fp.close()

    def file_TextOut(self, in_dict, file_name):
        texts_path = os.path.join(self._cwd, self._TextPath)
        file_str = os.path.join(texts_path, file_name + ".txt")
        # file_str = file_name + ".txt"
        fp = open(file_str, "w+")
        out_str = ""
        for key in in_dict:
            if in_dict[key]["selected"]:
                temp_dict = dict()
                temp_dict[key] = in_dict[key]
                temp_dict_str = str(temp_dict)
                out_str = out_str + temp_dict_str + '\n'
        fp.write(out_str)
        fp.close()

    def file_Recycle(self, in_dict):
        recycle_path = os.path.join(self._cwd, self._RecylcePath)
        onlyfiles = [f for f in listdir(recycle_path) if isfile(join(recycle_path, f))]
        # print("Files in Recycle Directory: ", onlyfiles)
        max_item = 0
        for files in onlyfiles:
            if files[0:4] == "rec_":
                name_list1 = files.split('.')
                temp_str = str(name_list1[0])
                name_list = temp_str.split("_")
                item_number = int(name_list[1])
                # print("Item_number: ", item_number)
                if item_number > max_item:
                    max_item = item_number

        max_item += 1
        # print("new max Item: ", max_item)
        file_str = os.path.join(recycle_path, "rec_" + "{:0>4}".format(max_item) + ".txt")
        # file_str = file_name + ".txt"
        fp = open(file_str, "w+")
        out_str = ""
        for key in in_dict:
            temp_dict = dict()
            temp_dict[key] = in_dict[key]
            temp_dict_str = str(temp_dict)
            out_str = out_str + temp_dict_str + '\n'
        fp.write(out_str)
        fp.close()

    def file_TextPrint(self, out_str):
        prints_path = os.path.join(self._cwd, self._PrintPath)
        file_str = os.path.join(prints_path, self._title + ".txt")
        # file_str = self._title + ".txt"
        fp = open(file_str, "w+")
        fp.write(out_str)
        fp.close()

    def file_MapOpen(self):
        jsons_path = os.path.join(self._cwd, self._MapPath)
        file_str = os.path.join(jsons_path, self._title + ".json")
        # file_str = self._title + ".json"
        with open(file_str) as fp:
            file_dict = json.load(fp)
        fp.close()
        return file_dict

    def file_MapSave(self, save_dict):
        jsons_path = os.path.join(self._cwd, self._MapPath)
        file_str = os.path.join(jsons_path, self._title + ".json")
        # file_str = self._title + ".json"
        with open(file_str, "w+") as fp:
            json.dump(save_dict, fp)
        fp.close()

    def file_MapOut(self, in_dict, file_name):
        jsons_path = os.path.join(self._cwd, self._MapPath)
        file_str = os.path.join(jsons_path, file_name + ".json")
        # file_str = file_name + ".json"
        out_dict = dict()
        for key in in_dict:
            out_dict[key] = in_dict[key]
        with open(file_str, "w+") as fp:
            json.dump(out_dict, fp)
        fp.close()

    def file_PathsOpen(self):
        jsons_path = os.path.join(self._cwd, self._PathsPath)
        file_str = os.path.join(jsons_path, self._title + ".json")
        # file_str = self._title + ".json"
        with open(file_str) as fp:
            file_dict = json.load(fp)
        fp.close()
        return file_dict

    def file_PathsSave(self, save_dict):
        jsons_path = os.path.join(self._cwd, self._PathsPath)
        file_str = os.path.join(jsons_path, self._title + ".json")
        # file_str = self._title + ".json"
        with open(file_str, "w+") as fp:
            json.dump(save_dict, fp)
        fp.close()

    def file_PathsOut(self, in_dict, file_name):
        jsons_path = os.path.join(self._cwd, self._PathsPath)
        file_str = os.path.join(jsons_path, file_name + ".json")
        # file_str = file_name + ".json"
        out_dict = dict()
        for key in in_dict:
            out_dict[key] = in_dict[key]
        with open(file_str, "w+") as fp:
            json.dump(out_dict, fp)
        fp.close()