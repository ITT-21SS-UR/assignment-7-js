import random

'''
Model for game logic (change command text, logging, etc.)

Author: Sarah
Reviewer: Jonas
'''


class GameModel():
    TEXT_BUTTON_LEFT = "Press the left button"
    TEXT_BUTTON_MIDDLE = "Press the middle button"
    TEXT_BUTTON_RIGHT = "Press the right button"
    TEXT_TURN_LEFT = "Turn it to the left"

    def select_command(self):
        random.shuffle(self.__command_list)
        return self.__command_list[0]

    def get_command_text(self):
        return self.select_command()

    def __init__(self):
        super().__init__()

        self.__command_list = [
            self.TEXT_BUTTON_LEFT,
            self.TEXT_BUTTON_MIDDLE,
            self.TEXT_BUTTON_RIGHT,
            self.TEXT_TURN_LEFT]
