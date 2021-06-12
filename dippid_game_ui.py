import sys

from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
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
    start_movement = pyqtSignal()
    is_correct_input = pyqtSignal(bool)

    def __init__(self, port):
        super(MainWindow, self).__init__()

        self.__sensor = SensorUDP(port)
        self.__model = GameModel()

        self.current_text = ""
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
        command_text.setText(self.current_text)

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
        self.turn_finished.connect(self.show_next, QtCore.Qt.QueuedConnection)
        self.game_finished.connect(self.stop_game, QtCore.Qt.QueuedConnection)
        self.start_movement.connect(
            self.handle_movement, QtCore.Qt.QueuedConnection)
        self.is_correct_input.connect(
            self.show_is_correct, QtCore.Qt.QueuedConnection)
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
        self.change_background_color("white")
        # palette = self.palette()
        # palette.setColor(QtGui.QPalette.Window, QtGui.QColor("White"))
        # self.setPalette(palette)

        if self.__turns == 0:
            self.game_finished.emit()
        else:
            self.current_text = self.__model.generate_command_text()
            self.command_text_el.setText(self.current_text)
            self.update()

            if self.__model.is_mov_text(self.current_text):
                QtCore.QTimer.singleShot(100, self.handle_movement)

    def handle_button_1_press(self, data):
        self.__sensor.unregister_callback(
            'button_1', self.handle_button_1_press)
        if int(data) != 0:
            print('button 1 pressed')
            self.handle_buttons(1)

    def handle_button_2_press(self, data):
        self.__sensor.unregister_callback(
            'button_2', self.handle_button_2_press)
        if int(data) != 0:
            print('button 2 pressed')
            self.handle_buttons(2)

    def handle_button_3_press(self, data):
        self.__sensor.unregister_callback(
            'button_3', self.handle_button_3_press)
        if int(data) != 0:
            print('button 3 pressed')
            self.handle_buttons(3)

    def handle_buttons(self, button_num):
        if self.__model.is_correct_button(self.current_text, button_num):
            self.__credits += 1
            self.is_correct_input.emit(True)
        else:
            self.is_correct_input.emit(False)

        self.__turns -= 1

    @QtCore.pyqtSlot()
    def handle_movement(self):
        print("handle_movement")
        if self.__model.is_correct_move(self.current_text, self.__sensor):
            self.__credits += 1
            self.is_correct_input.emit(True)

        else:
            self.is_correct_input.emit(False)

        self.__turns -= 1
        print("handle_movement finished")

    def change_background_color(self, background_color):
        self.current_text = ""
        self.command_text_el.setText(self.current_text)
        self.setStyleSheet("background-color:" + background_color + ";")
        self.update()

    def show_is_correct(self, is_correct):
        print(is_correct)

        if is_correct:
            QtCore.QTimer.singleShot(
                1, lambda: self.change_background_color("green"))

        else:
            QtCore.QTimer.singleShot(
                1, lambda: self.change_background_color("red"))

        QtCore.QTimer.singleShot(2000, lambda: self.turn_finished.emit())

    def stop_game(self):
        self.__sensor.disconnect()
        self.show_results()
        QtWidgets.qApp.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(int(sys.argv[1]))
    main_window.show()

    sys.exit(app.exec_())
