import random
import datetime

from DIPPID_MAIN.DIPPID import Sensor, SensorUDP, SensorSerial
from time import sleep

# use UPD (via WiFi) for communication
# PORT = 5700
# sensor = SensorUDP(PORT)

# use the serial connection (USB) for communication
# TTY = '/dev/ttyUSB0'
# sensor = SensorSerial(TTY)

'''
Model for reading sensor data.
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

        #self.__port = port
        self.__sensor = sensor

        self.__command_list = [
            self.TEXT_BUTTON_LEFT,
            self.TEXT_BUTTON_MIDDLE,
            self.TEXT_BUTTON_RIGHT]
            #self.TEXT_TURN_LEFT]

    def read_data(self):
        while(True):
            # print all capabilities of the sensor
            print('capabilities: ', self.__sensor.get_capabilities())

            # check if the sensor has the 'accelerometer' capability
            if(self.__sensor.has_capability('accelerometer')):
                # print whole accelerometer object (dictionary)
                print('accelerometer data: ',
                      self.__sensor.get_value('accelerometer'))

                # print only one accelerometer axis
                print('accelerometer X: ', self.__sensor.get_value(
                    'accelerometer')['x'])

            sleep(0.1)

    def is_left_button_pressed(self):
        if(self.__sensor.has_capability('button_1')):
            if(self.__sensor.get_value('button_1') == 1):
                print('Left button pressed')
                return True
            return False

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

    def is_movment_text(self, text):
        if text == self.TEXT_TURN_LEFT or self.TEXT_TURN_RIGHT:
            return True
        return False



    def calculate_time_difference(self, start_time, end_time):
        try:
            return round((end_time - start_time).total_seconds(), 2)
        except AttributeError:
            return self.INVALID_TIME
        except TypeError:
            return self.INVALID_TIME
