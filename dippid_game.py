#!/usr/bin/env python3
# coding: utf-8
# -*- coding: utf-8 -*-

import sys

from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout

from DIPPID import SensorUDP
from dippid_model import GameModel

'''
The game is implemented for the M5Stack and uses UDP port for connection.

HOW TO START THE PROGRAM:
- Connect the M5Stack over UDP port
- Type "python3 dippid_game.py [PORT]" into console
- As default PORT use 5700

GAME:
- In random order instructions like "Press the left button" or "Turn it to the right" are shown.
- The user has to follow the instructions.
- If the action was correct, the window gets green, if not it gets red.
- Also the remaning turns are displayed.
- After 10 turns (defined as TOTAL_TURNS; can be adjusted) the game ends.
- The score and the total time are displayed at the end.

Author: Sarah
Reviewer: Jonas
'''

TOTAL_TURNS = 10


class MainWindow(QtWidgets.QWidget):
    game_finished = pyqtSignal()
    turn_finished = pyqtSignal()
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
        self.__accept_button = False

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
                            \nIf action was correct, window turns green, if not, red.")

        self.__sensor.register_callback('button_1', self.handle_button_1_press)
        self.__sensor.register_callback('button_2', self.handle_button_2_press)
        self.__sensor.register_callback('button_3', self.handle_button_3_press)

        self.__start_time = datetime.now()

    def start_game(self):
        self.turn_finished.connect(self.show_next, QtCore.Qt.QueuedConnection)
        self.game_finished.connect(self.stop_game, QtCore.Qt.QueuedConnection)
        self.is_correct_input.connect(
            self.show_is_correct, QtCore.Qt.QueuedConnection)

        self.show_next()

    def show_results(self):
        self.__end_time = datetime.now()
        self.__time_diff = self.__model.calculate_time_difference(
            self.__start_time, self.__end_time)

        QtWidgets.QMessageBox.information(self,
                                          "Results",
                                          "Score: " + str(self.__credits) +
                                          " out of " + str(TOTAL_TURNS) +
                                          "\n Time: " + str(self.__time_diff) + "s")

    def show_next(self):
        self.change_background_color("white")
        if self.__turns <= 0:
            self.game_finished.emit()
        else:
            self.current_text = self.__model.generate_command_text()
            self.command_text_el.setText(self.current_text)
            self.update()

            if self.__model.is_mov_text(self.current_text):
                QtCore.QTimer.singleShot(100, self.handle_movement)
            else:
                self.__accept_button = True

    def handle_button_1_press(self, data):
        if int(data) != 0:
            self.handle_buttons(1)

    def handle_button_2_press(self, data):
        if int(data) != 0:
            self.handle_buttons(2)

    def handle_button_3_press(self, data):
        if int(data) != 0:
            self.handle_buttons(3)

    def handle_buttons(self, button_num):
        if not self.__accept_button:
            return

        self.__accept_button = False

        if self.__model.is_correct_button(self.current_text, button_num):
            self.__credits += 1
            self.is_correct_input.emit(True)
        else:
            self.is_correct_input.emit(False)

        self.__turns -= 1

    @QtCore.pyqtSlot()
    def handle_movement(self):
        if self.__model.is_correct_move(self.current_text, self.__sensor):
            self.__credits += 1
            self.is_correct_input.emit(True)

        else:
            self.is_correct_input.emit(False)

        self.__turns -= 1

    def change_background_color(self, background_color):
        self.setStyleSheet("background-color:" + background_color + ";")
        self.current_text = "Turns remaining: " + str(self.__turns)
        self.command_text_el.setText(self.current_text)
        self.update()

    def show_is_correct(self, is_correct):
        if is_correct:
            QtCore.QTimer.singleShot(
                1, lambda: self.change_background_color("green"))

        else:
            QtCore.QTimer.singleShot(
                1, lambda: self.change_background_color("red"))

        QtCore.QTimer.singleShot(2000, lambda: self.turn_finished.emit())

    def stop_game(self):
        self.__sensor.disconnect()

        self.__sensor.unregister_callback(
            'button_1', self.handle_button_1_press)
        self.__sensor.unregister_callback(
            'button_2', self.handle_button_2_press)
        self.__sensor.unregister_callback(
            'button_3', self.handle_button_3_press)

        self.show_results()
        QtWidgets.qApp.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    if len(sys.argv) < 2:
        sys.stderr.write("Please specify port number as argument\n")
        sys.exit(1)

    main_window = MainWindow(int(sys.argv[1]))
    main_window.show()

    sys.exit(app.exec_())
