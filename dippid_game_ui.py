import sys

from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout

from DIPPID_MAIN.DIPPID import SensorUDP
from dippid_model import GameModel

'''
The game is implemented for the M5Stack and uses UDP port for connection.

HOW TO START THE PROGRAM:
- Connect the M5Stack over UDP port
- Type "python3 dippid_game_ui.py [PORT]" into console
- As default PORT use 5700

Author: Sarah
Reviewer: Jonas
'''

TOTAL_TURNS = 10


class MainWindow(QtWidgets.QWidget):
    game_finished = pyqtSignal()
    turn_finished = pyqtSignal()

    def __init__(self, port):
        super(MainWindow, self).__init__()

        self.__sensor = SensorUDP(port)
        self.__model = GameModel(self.__sensor)

        self.current_text = self.__model.generate_command_text()
        self.command_text_el = self.__setup_command_text()

        self.__credits = 0
        self.__turns = TOTAL_TURNS
        self.__start_time = None
        self.__end_time = None

        self.__setup_layout()
        self.__show_hint()

        self.start_game()

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

        self.__sensor.register_callback('button_1', self.handle_button_1_press)
        self.__sensor.register_callback('button_2', self.handle_button_2_press)
        self.__sensor.register_callback('button_3', self.handle_button_3_press)

        self.__start_time = datetime.now()

    def start_game(self):
        self.turn_finished.connect(self.show_next)
        self.game_finished.connect(self.stop_game)
        self.show_next()

    def show_results(self):
        self.__end_time = datetime.now()
        self.__time_diff = self.__model.calculate_time_difference(
            self.__start_time, self.__end_time)

        QtWidgets.QMessageBox.information(self,
                                          "Results",
                                          "Credits: " + str(self.__credits) +
                                          " out of " + str(TOTAL_TURNS) +
                                          "\n Time: " + str(self.__time_diff) + "s")

    def show_next(self):
        if self.__turns == 0:
            self.game_finished.emit()
        else:
            self.current_text = self.__model.generate_command_text()
            self.command_text_el.setText(self.current_text)
            self.update()

    def handle_button_1_press(self, data):
        if int(data) != 0:
            print('button 1 pressed')
            self.handle_buttons(1)

    def handle_button_2_press(self, data):
        if int(data) != 0:
            print('button 2 pressed')
            self.handle_buttons(2)

    def handle_button_3_press(self, data):
        if int(data) != 0:
            print('button 3 pressed')
            self.handle_buttons(3)

    def handle_buttons(self, button_num):
        if self.__model.is_correct_button(self.current_text, button_num):
            self.__credits += 1

        self.__turns -= 1
        self.turn_finished.emit()

    def handle_movement(self):
        if self.__model.get_data(self.__sensor):
            self.__credits += 1

        self.__turns -= 1
        self.turn_finished.emit()

    def unregister_buttons(self):
        self.__sensor.unregister_callback(
            'button_1', self.handle_button_1_press)
        self.__sensor.unregister_callback(
            'button_2', self.handle_button_2_press)
        self.__sensor.unregister_callback(
            'button_3', self.handle_button_3_press)

    def stop_game(self):
        self.unregister_buttons()
        self.__sensor.disconnect()
        self.show_results()
        QtWidgets.qApp.quit()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(int(sys.argv[1]))
    main_window.show()

    sys.exit(app.exec_())
