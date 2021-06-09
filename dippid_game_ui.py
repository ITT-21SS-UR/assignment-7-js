import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout

from dippid_game_model import GameModel
from dippid_model import SensorModel

'''
Class for UI and programm entry.

Author: Sarah
Reviewer: Jonas
'''


class MainWindow(QtWidgets.QWidget):
    def __init__(self, port):
        super(MainWindow, self).__init__()

        self.__game_model = GameModel()
        self.__sensor_model = SensorModel(port)

        self.setFixedSize(800, 600)
        self.move(QtWidgets.qApp.desktop().availableGeometry(
            self).center() - self.rect().center())

        self.setWindowTitle("Fun Game")

        self.__setup_example_text()
        self.__setup_layout()

        self.__show_hint()

    def __setup_example_text(self):
        command_text = QtWidgets.QLabel(self)
        command_text.setFont(QFont("Arial", 30))
        command_text.setText(self.__game_model.get_command_text())
        command_text.setAlignment(QtCore.Qt.AlignCenter)
        self.__example_text = command_text

    def __setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.__example_text)

        self.setLayout(layout)

    def __show_hint(self):
        QtWidgets.QMessageBox.information(self,
                                          "Instructions",
                                          "Follow the text instructions!\
                                              \n e.g. press buttons")

    def read_data(self):
        # self.__sensor_model.read_data()
        self.__sensor_model.is_button_pressed()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(int(sys.argv[1]))
    main_window.read_data()

    main_window.show()

    sys.exit(app.exec_())
