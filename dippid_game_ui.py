import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout

from DIPPID_MAIN.DIPPID import SensorUDP
from dippid_model import GameModel

'''
Class for UI and programm entry.

Author: Sarah
Reviewer: Jonas
'''


class MainWindow(QtWidgets.QWidget):
    def __init__(self, port):
        super(MainWindow, self).__init__()

        self.__sensor = SensorUDP(port)
        self.__model = GameModel(self.__sensor)

        self.current_text = self.__model.generate_command_text()
        self.command_text_el = self.__setup_command_text()
        self.command_text_el.setText(self.current_text)

        self.__setup_layout()
        self.__show_hint()

        self.__sensor.register_callback('button_1', self.handle_button_1_press)
        self.__sensor.register_callback('button_2', self.handle_button_2_press)
        self.__sensor.register_callback('button_3', self.handle_button_3_press)


    def __setup_command_text(self):
        command_text = QtWidgets.QLabel(self)
        command_text.setFont(QFont("Arial", 30))
        command_text.setAlignment(QtCore.Qt.AlignCenter)

        return command_text

    def __setup_layout(self):
        self.setFixedSize(800, 600)
        self.move(QtWidgets.qApp.desktop().availableGeometry(
            self).center() - self.rect().center())

        self.setWindowTitle("Fun Game")

        layout = QVBoxLayout(self)
        layout.addWidget(self.command_text_el)

        self.setLayout(layout)

    def __show_hint(self):
        QtWidgets.QMessageBox.information(self,
                                          "Instructions",
                                          "Follow the text instructions!\
                                              \n e.g. press buttons")

    def update_com_text(self):
        self.current_text = self.__model.generate_command_text()
        self.command_text_el.setText(self.current_text)
        self.update()

    def handle_button_1_press(self, data):
        if int(data) == 0:
            print('button 1 released')
        else:
            print('button 1 pressed')
            print(self.__model.is_correct_button(self.current_text, 1))
            self.update_com_text()
            # TODO limit runs

    def handle_button_2_press(self, data):
        if int(data) == 0:
            print('button 2 released')
        else:
            print('button 2 pressed')
            print(self.__model.is_correct_button(self.current_text, 2))
            self.update_com_text() 

    def handle_button_3_press(self, data):
        if int(data) == 0:
            print('button 3 released')
        else:
            print('button 3 pressed')
            if(self.__model.is_correct_button(self.current_text, 3)):
                print("Correct")
                self.update_com_text()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(int(sys.argv[1]))
    main_window.show()

    sys.exit(app.exec_())
