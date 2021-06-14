import sys
import pyqtgraph as pg
import numpy as np

import pyqtgraph.flowchart.library as fclib
from pyqtgraph.flowchart import Flowchart, Node
from pyqtgraph.flowchart.library.common import CtrlNode
from pyqtgraph.Qt import QtGui, QtCore

# import BufferNode and DIPPIDNode
from DIPPID_MAIN.DIPPID_pyqtnode import BufferNode, DIPPIDNode
from DIPPID_MAIN.DIPPID import SensorUDP, SensorSerial, SensorWiimote

# create NormalVectorNode


class NormalVectorNode(Node):

    node_name = "NormalVector"

    # instead of accel_value1 x, y and z?
    def __init__(self, name):
        terminals = {
            'accel_value_x': dict(io='in'),
            'accel_value_y': dict(io='in'),
            'accel_value_z': dict(io='in'),
            'output_vector': dict(io='out')
        }
        self.__output_vector = np.array([])
        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        self.__output_vector = np.array([[0, 0],
                                         [kwds['accel_value_x'][0],
                                          kwds['accel_value_y'][0],
                                          kwds['accel_value_z'][0]]])
        return {'output_vector': self.__output_vector}


fclib.registerNodeType(NormalVectorNode, [('Data', )])

# create LogNode


class LogNode(Node):

    node_name = "Log"

    def __init__(self, name):
        terminals = {'dataIn': dict(io='in')}
        Node.__init__(self, name, terminals=terminals)

    # def process(self, **kwds): Terminal Calls: IndentationError: unindent does not match any outer indentation level
    # print(kwds["dataIn"])
    # return


fclib.registerNodeType(LogNode, [('Log', )])


def generate_plots_and_nodes():
    # TODO nodes should have different positions
    plot_widget_accel_x = pg.PlotWidget()
    layout.addWidget(plot_widget_accel_x, 0, 1)
    plot_widget_accel_x.setTitle('Plot for Accelerometer X')
    plot_widget_accel_x.setYRange(0, 1)

    plot_widget_node_1 = chart.createNode('PlotWidget', pos=(0, -150))
    plot_widget_node_1.setPlot(plot_widget_accel_x)

    plot_widget_accel_y = pg.PlotWidget()
    layout.addWidget(plot_widget_accel_y, 0, 1)
    plot_widget_accel_y.setTitle('Plot for Accelerometer Y')
    plot_widget_accel_y.setYRange(0, 1)

    plot_widget_node_2 = chart.createNode('PlotWidget', pos=(0, -150))
    plot_widget_node_2.setPlot(plot_widget_accel_y)

    plot_widget_accel_z = pg.PlotWidget()
    layout.addWidget(plot_widget_accel_z, 0, 1)
    plot_widget_accel_z.setTitle('Plot for Accelerometer Z')
    plot_widget_accel_z.setYRange(0, 1)

    plot_widget_node_3 = chart.createNode('PlotWidget', pos=(0, -150))
    plot_widget_node_3.setPlot(plot_widget_accel_z)

    plot_widget_normal_vector = pg.PlotWidget()
    layout.addWidget(plot_widget_normal_vector, 0, 1)
    plot_widget_normal_vector.setTitle('Plot for NormalVectorNode')
    plot_widget_normal_vector.setYRange(0, 1)

    plot_widget_node_4 = chart.createNode('PlotWidget', pos=(0, -150))
    plot_widget_node_4.setPlot(plot_widget_normal_vector)

# def connect_nodes():
    # fc.connectTerminals(dippidNode['accelX'], bufferNode['dataIn'])
    # fc.connectTerminals(bufferNode['dataOut'], pw1Node['In'])


if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    win.setWindowTitle('set title')

    central_widget = QtGui.QWidget()
    win.setCentralWidget(central_widget)
    layout = QtGui.QGridLayout()
    central_widget.setLayout(layout)

    # Create an empty flowchart with a single input and output
    chart = Flowchart(terminals={})
    chart_widget = chart.widget()
    layout.addWidget(chart.widget(), 0, 0, 2, 1)

    generate_plots_and_nodes()

    dippid_node = chart.createNode("DIPPID", pos=(0, 0))

    buffer_node_accel_x = chart.createNode("Buffer", pos=(150, 0))
    buffer_node_accel_y = chart.createNode("Buffer", pos=(150, 0))
    buffer_node_accel_z = chart.createNode("Buffer", pos=(150, 0))

    normal_vector_node = chart.createNode("NormalVector", pos=(0, 0))

    log_node = chart.createNode("Log", pos=(150, 0))

    # connect_nodes()

    win.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sys.exit(QtGui.QApplication.instance().exec_())
