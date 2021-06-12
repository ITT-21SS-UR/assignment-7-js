import random

from DIPPID_MAIN.DIPPID import Sensor, SensorUDP, SensorSerial
from time import sleep

'''
Model for reading sensor data and verify data.
Author: Sarah
Reviewer: Jonas
'''


class GameModel():

    TEXT_BUTTON_LEFT = "Press the left button"
    TEXT_BUTTON_MIDDLE = "Press the middle button"
    TEXT_BUTTON_RIGHT = "Press the right button"
    TEXT_TURN_LEFT = "Turn it to the left"
    TEXT_TURN_RIGHT = "Turn it to the right"

    def __init__(self):
        super().__init__()

        self.__command_list = [
            self.TEXT_BUTTON_LEFT,
            self.TEXT_BUTTON_MIDDLE,
            self.TEXT_BUTTON_RIGHT,
            self.TEXT_TURN_LEFT,
            self.TEXT_TURN_RIGHT]

    # TODO better choice
    # not one mov after another
    # not same instructions after another
    def generate_command_text(self):
        return random.choice(self.__command_list)

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

    def is_correct_move(self, text, sensor):
        SAMPLE_SIZE = 200
        SAMPLE_RATE = 1 / 20  # 20 Hz

        NUMBER_OF_VALUES = 5
        data = [0] * NUMBER_OF_VALUES

        for i in range(0, SAMPLE_SIZE):
            data[i % NUMBER_OF_VALUES] = sensor.get_value('accelerometer')['x']
            if all(x < -0.1 for x in data):  # right
                return self.__is_correct_move(text, 1)

            if all(x > 0.1 for x in data):  # left
                return self.__is_correct_move(text, -1)

            sleep(SAMPLE_RATE)

        return False

    def __is_correct_move(self, text, x):
        if text == self.TEXT_TURN_LEFT and x < 0:
            return True

        if text == self.TEXT_TURN_RIGHT and x > 0:
            return True

        return False

    def calculate_time_difference(self, start_time, end_time):
        try:
            return round((end_time - start_time).total_seconds(), 2)
        except AttributeError:
            return self.INVALID_TIME
        except TypeError:
            return self.INVALID_TIME
