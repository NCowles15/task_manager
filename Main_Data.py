from ClassResources.Edit_Data import Edit_Data
from ClassResources.Task_Data import Task_Data
from ClassResources.Validifiers import validate
from ClassResources.File_Handler import File_Handler
from ClassResources.Send_Printer import Send_Printer
# from ClassResources.Send_Calendar import Send_Calendar
from ClassResources.Send_Wunderlist import Send_Wunderlist
from GUIResources.MainWindowClass import MainWindow

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtGui, QtWidgets



def main():
    """
    Main executable for task manager application.
    Begins running Gui
    """

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Main Database")
    window.show()
    window.Open_User_Triggered()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
