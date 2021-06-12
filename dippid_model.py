import random

from DIPPID_MAIN.DIPPID import Sensor, SensorUDP, SensorSerial
from time import sleep

'''
Model for reading sensor data and .
Author: Sarah
Reviewer: Jonas
'''


class GameModel():

    TEXT_BUTTON_LEFT = "Press the left button"
    TEXT_BUTTON_MIDDLE = "Press the middle button"
    TEXT_BUTTON_RIGHT = "Press the right button"
    TEXT_TURN_LEFT = "Turn it to the left"
    TEXT_TURN_RIGHT = "Turn it to the right"

    def __init__(self, sensor):
        super().__init__()

        self.__command_list = [
            self.TEXT_BUTTON_LEFT,
            self.TEXT_BUTTON_MIDDLE,
            self.TEXT_BUTTON_RIGHT,
            self.TEXT_TURN_LEFT,
            self.TEXT_TURN_RIGHT]

    def generate_command_text(self):
        random.shuffle(self.__command_list)
        return self.__command_list[0]

    def get_command_list(self):
        return self.__command_list

    def is_correct_button(self, text, button_num):
        if text == self.TEXT_BUTTON_LEFT and button_num == 1:
            return True
        elif text == self.TEXT_BUTTON_MIDDLE and button_num == 2:
            return True
        elif text == self.TEXT_BUTTON_RIGHT and button_num == 3:
            return True

        return False

    def is_mov_text(self, text):
        if text == self.TEXT_TURN_LEFT or text == self.TEXT_TURN_RIGHT:
            return True
        return False

    def get_data(self, sensor):
        NUMBER_OF_VALUES = 10
        data = []
        # consider ten angle values
        # if x is negative then it is  a left turn
        # if x is positive then it is a right turn
        for i in range(0, 10):
            data[i] = 0

        while True:
            if data[NUMBER_OF_VALUES] != 0:
                return self.is_correct_move(data)

            for i in data:
                # i%10
                data[i] = sensor.get_value('angle_x')
                sleep(1)

    def is_left_move(self, data):
        # x negative
        for i in data:
            if i > 0:
                return False
        return True

    def is_right_move(self, data):
        # x positve
        for i in data:
            if i < 0:
                return False
        return True

    def is_correct_move(self, text, x):
        if text == self.TEXT_TURN_LEFT and self.is_left_move(x):
            return True
        elif text == self.TEXT_TURN_RIGHT and self.is_right_move(x):
            return True

        return False

    def calculate_time_difference(self, start_time, end_time):
        try:
            return round((end_time - start_time).total_seconds(), 2)
        except AttributeError:
            return self.INVALID_TIME
        except TypeError:
            return self.INVALID_TIME
