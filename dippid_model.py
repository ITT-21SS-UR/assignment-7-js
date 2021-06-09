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


class SensorModel():
    def __init__(self, port):
        super().__init__()

        self.__port = port
        self.__sensor = SensorUDP(self.__port)

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

    def is_middle_button_pressed(self):
        if(self.__sensor.has_capability('button_2')):
            if(self.__sensor.get_value('button_2') == 1):
                print('Middle button pressed')

    def is_right_button_pressed(self):
        if(self.__sensor.has_capability('button_3')):
            if(self.__sensor.get_value('button_3') == 1):
                print('Right button pressed')

    def is_button_pressed(self):
        while(True):
            self.is_left_button_pressed()
            self.is_middle_button_pressed()
            self.is_right_button_pressed()
