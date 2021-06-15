import sys
from numpy.core.function_base import logspace
import pyqtgraph as pg
import numpy as np

import pyqtgraph.flowchart.library as fclib
from pyqtgraph.flowchart import Flowchart, Node
from pyqtgraph.flowchart.library.common import CtrlNode
from pyqtgraph.Qt import QtGui, QtCore

# import BufferNode and DIPPIDNode
from DIPPID_pyqtnode import BufferNode, DIPPIDNode
from DIPPID import SensorUDP, SensorSerial, SensorWiimote

# create NormalVectorNode


class NormalVectorNode(Node):

    nodeName = "NormalVector"

    def __init__(self, name):
        terminals = {
            'accel_x': dict(io='in'),
            'accel_z': dict(io='in'),
            'output_rotation': dict(io='out')
        }
        self.__output_vector = np.array([])
        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        normal_x = -kwds["accel_x"][0]
        normal_z = kwds["accel_z"][0]

        self.__output_vector = np.array(((0, 0), (normal_x, normal_z)))

        return {'output_rotation': self.__output_vector}


fclib.registerNodeType(NormalVectorNode, [('Data', )])

# create LogNode
class LogNode(Node):

    nodeName = "Log"

    def __init__(self, name):
        terminals = {
            'accel_x': dict(io='in'),
            'accel_y': dict(io='in'),
            'accel_z': dict(io='in'),
            'output': dict(io='out')
        }
        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        log_data = {
                "accel_x": kwds["accel_x"][0],
                "accel_y": kwds["accel_y"][0],
                "accel_z": kwds["accel_z"][0]
        }
        print(log_data)
        return log_data


fclib.registerNodeType(LogNode, [('Log data', )])


def generate_plots_and_nodes():
    pass

# def connect_nodes():
    # fc.connectTerminals(dippidNode['accelX'], bufferNode['dataIn'])
    # fc.connectTerminals(bufferNode['dataOut'], pw1Node['In'])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stdout.write("Please specify port")
    
    port_num = sys.argv[0]
    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    win.setWindowTitle('set title')

    central_widget = QtGui.QWidget()
    win.setCentralWidget(central_widget)
    layout = QtGui.QGridLayout()
    central_widget.setLayout(layout)
    win.show()

    # generate_plots_and_nodes()

    chart = Flowchart(terminals={'out': dict(io='out')})
    chart_widget = chart.widget()
    layout.addWidget(chart.widget(), 0, 0, 2, 1)
    
    # accelerometer_x
    plot_widget_accel_x = pg.PlotWidget()
    plot_widget_accel_x.setTitle('Plot for Accelerometer X')
    plot_widget_accel_x.setYRange(0, 1)
    layout.addWidget(plot_widget_accel_x, 0, 1)
    plot_widget_node_1 = chart.createNode('PlotWidget', pos=(300, -200))
    plot_widget_node_1.setPlot(plot_widget_accel_x)

    # accelerometer_y
    plot_widget_accel_y = pg.PlotWidget()
    layout.addWidget(plot_widget_accel_y, 0, 2)
    plot_widget_accel_y.setTitle('Plot for Accelerometer Y')
    plot_widget_accel_y.setYRange(0, 1)
    plot_widget_node_2 = chart.createNode('PlotWidget', pos=(300, -100))
    plot_widget_node_2.setPlot(plot_widget_accel_y)

    # accelerometer_z
    plot_widget_accel_z = pg.PlotWidget()
    layout.addWidget(plot_widget_accel_z, 1, 1)
    plot_widget_accel_z.setTitle('Plot for Accelerometer Z')
    plot_widget_accel_z.setYRange(0, 1)
    plot_widget_node_3 = chart.createNode('PlotWidget', pos=(300, 200))
    plot_widget_node_3.setPlot(plot_widget_accel_z)

    # normal vector
    plot_widget_normal_vector = pg.PlotWidget()
    layout.addWidget(plot_widget_normal_vector, 1, 2)
    plot_widget_normal_vector.setTitle('Plot for NormalVectorNode')
    plot_widget_normal_vector.setYRange(0, 1)
    plot_widget_node_4 = chart.createNode('PlotWidget', pos=(300, 100))
    plot_widget_node_4.setPlot(plot_widget_normal_vector)

    # log vector
    #plot_widget_log_vector = pg.PlotWidget()
    #layout.addWidget(plot_widget_log_vector, 1, 2)
    #plot_widget_log_vector.setTitle('Plot for LogVectorNode')
    #plot_widget_log_vector.setYRange(0, 1)
    #plot_widget_node_5 = chart.createNode('PlotWidget', pos=(0, -150)) 
    #plot_widget_node_5.setPlot(plot_widget_log_vector)

    # Create an empty flowchart with a single input and output

    dippid_node = chart.createNode("DIPPID", pos=(0, 0))

    buffer_node_accel_x = chart.createNode("Buffer", pos=(100, -200)) 
    buffer_node_accel_y = chart.createNode("Buffer", pos=(130, -100))
    buffer_node_accel_z = chart.createNode("Buffer", pos=(100, 200))

    normal_vector_node = chart.createNode("NormalVector", pos=(130, 100))

    log_node = chart.createNode("Log", pos=(150, 0))

    #connect_nodes
    chart.connectTerminals(dippid_node['accelX'], buffer_node_accel_x['dataIn'])
    chart.connectTerminals(dippid_node['accelY'], buffer_node_accel_y['dataIn'])
    chart.connectTerminals(dippid_node['accelZ'], buffer_node_accel_z['dataIn'])
    chart.connectTerminals(buffer_node_accel_x['dataOut'], plot_widget_node_1['In'])
    chart.connectTerminals(buffer_node_accel_y['dataOut'], plot_widget_node_2['In'])
    chart.connectTerminals(buffer_node_accel_z['dataOut'], plot_widget_node_3['In'])

    chart.connectTerminals(dippid_node['accelX'], normal_vector_node['accel_x'])
    chart.connectTerminals(dippid_node['accelZ'], normal_vector_node['accel_z'])
    chart.connectTerminals(normal_vector_node['output_rotation'], plot_widget_node_4['In'])

    chart.connectTerminals(dippid_node['accelX'], log_node['accel_x'])
    chart.connectTerminals(dippid_node['accelY'], log_node['accel_y'])
    chart.connectTerminals(dippid_node['accelZ'], log_node['accel_z'])

    #######################################################################################
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sys.exit(QtGui.QApplication.instance().exec_())

    sys.exit(app.exec_())
