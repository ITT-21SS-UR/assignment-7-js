import sys

from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from DIPPID_MAIN.DIPPID import SensorUDP
from dippid_model import GameModel

'''
Class for UI and programm entry.

HOW TO START THE PROGRAM:
python3 dippid_game_ui.py [PORT]
as default PORT use 5700

Author: Sarah
Reviewer: Jonas
'''

TOTAL_TURNS = 10

class MainWindow(QtWidgets.QWidget):
    def __init__(self, port):
        super(MainWindow, self).__init__()

        self.__sensor = SensorUDP(port)
        self.__model = GameModel(self.__sensor)

        self.current_text = self.__model.generate_command_text()
        self.command_text_el = self.__setup_command_text()
        self.command_text_el.setText(self.current_text)
        
        self.__credits = 0
        self.__turns = TOTAL_TURNS
        self.__start_time = None
        self.__end_time = None

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
        msg_box = QtWidgets.QMessageBox
        msg_box.information(self,
                            "Instructions",
                            "Follow the text instructions as fast as possible!\
                            \n(e.g. press left button)")

        # TODO evtl. start timer if ok-button is pressed                   
        self.__start_time = datetime.now()

    def __show_results(self, time):
        QtWidgets.QMessageBox.information(self,
                                          "Results",
                                          "Credits: " + str(self.__credits) + 
                                          " out of " + str(TOTAL_TURNS) +
                                          "\n Time: " + str(time) + "s")
        
        # stop app if ok button is clicked
        QtWidgets.qApp.quit()

    def update_com_text(self):
        self.current_text = self.__model.generate_command_text()
        self.command_text_el.setText(self.current_text)
        self.update()

    def handle_button_1_press(self, data):
        if int(data) == 0:
            print('button 1 released')
        else:
            print('button 1 pressed')
            if self.__model.is_correct_button(self.current_text, 1):
                self.__credits += 1

            self.__turns -= 1
            if self.__turns == 0:
                self.calculate_results()
            else:
                self.update_com_text()

    def handle_button_2_press(self, data):
        if int(data) == 0:
            print('button 2 released')
        else:
            print('button 2 pressed')
            if self.__model.is_correct_button(self.current_text, 2):
                self.__credits += 1

            self.__turns -= 1
            if self.__turns == 0:
                self.calculate_results()
            else:
                self.update_com_text()
            

    def handle_button_3_press(self, data):
        if int(data) == 0:
            print('button 3 released')
        else:
            print('button 3 pressed')
            if self.__model.is_correct_button(self.current_text, 3):
                self.__credits += 1
            
            self.__turns -= 1
            if self.__turns == 0:
                self.calculate_results()
            else:
                self.update_com_text()

    def calculate_results(self):
        self.__end_time = datetime.now()
        time = self.__model.calculate_time_difference(self.__start_time, self.__end_time)
        self.__show_results(time)

    def handle_movement(self):
        if self.__model.is_movment_text(self.current_text):
            print("moving")
            # TODO in do while check if correct


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(int(sys.argv[1]))
    main_window.show()

    sys.exit(app.exec_())
