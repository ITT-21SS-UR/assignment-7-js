import sys
import pyqtgraph as pg
import numpy as np
import pyqtgraph.flowchart.library as fclib
from pyqtgraph.flowchart import Flowchart, Node
from pyqtgraph.flowchart.library.common import CtrlNode
from pyqtgraph.Qt import QtGui, QtCore
from DIPPID import SensorUDP, SensorSerial, SensorWiimote
# import BufferNode and DIPPIDNode
from DIPPID_pyqtnode import BufferNode, DIPPIDNode

#create NormalVectorNode
class NormalVectorNode(Node): 

    nodeName = "NormalVector"

    def __init__(self, name):
        terminals = {
            'accel_value1': dict(io='in'),
            'accel_value2': dict(io='in'),
            'output_vector': dict(io='out')
        }
        self._output_vector = np.array([])
        Node.__init__(self, name, terminals=terminals)

    def process(self, **kwds):
        self._output_vector = np.array([[0, 0], [kwds['accel_value1'][0], kwds['accel_value2'][0]]])
        return {'output_vector': _output_vector}


fclib.registerNodeType(NormalVectorNode, [('Data', )])

#create LogNode
class LogNode(Node):
    
   nodeName = "Log"
   
   def __init__(self, name):
       terminals = {
           'dataIn': dict(io='in')
        }
       
       Node.__init__(self, name, terminals=terminals)
       
    ###def process(self, **kwds): Terminal Calls: IndentationError: unindent does not match any outer indentation level
        ##print(kwds["dataIn"])
        ###return
        
fclib.registerNodeType(LogNode, [('Log', )])

def generate_plots_and_nodes():
    
    pw_accelX = pg.PlotWidget()
    layout.addWidget(pw_accelX, 0, 1)
    pw_accelX.setTitle('Plot for Accelerometer X')
    pw_accelX.setYRange(0, 1)
    
    pw1Node = fc.createNode('PlotWidget', pos=(0, -150))
    pw1Node.setPlot(pw_accelX)
    
    pw_accelY = pg.PlotWidget()
    layout.addWidget(pw_accelY, 0, 1)
    pw_accelY.setTitle('Plot for Accelerometer Y')
    pw_accelY.setYRange(0, 1)
    
    pw2Node = fc.createNode('PlotWidget', pos=(0, -150))
    pw2Node.setPlot(pw_accelY)
    
    pw_accelZ = pg.PlotWidget()
    layout.addWidget(pw_accelZ, 0, 1)
    pw_accelZ.setTitle('Plot for Accelerometer Z')
    pw_accelZ.setYRange(0, 1)
    
    pw3Node = fc.createNode('PlotWidget', pos=(0, -150))
    pw3Node.setPlot(pw_accelZ)
    
    pw_NormalVector = pg.PlotWidget()
    layout.addWidget(pw_NormalVector, 0, 1)
    pw_NormalVector.setTitle('Plot for NormalVectorNode')
    pw_NormalVector.setYRange(0, 1)
    
    pw4Node = fc.createNode('PlotWidget', pos=(0, -150))
    pw4Node.setPlot(pw_NormalVector)
    
#def connect_nodes():
    #fc.connectTerminals(dippidNode['accelX'], bufferNode['dataIn'])
    #fc.connectTerminals(bufferNode['dataOut'], pw1Node['In'])
    

if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    win.setWindowTitle('set title')
    cw = QtGui.QWidget()
    win.setCentralWidget(cw)
    layout = QtGui.QGridLayout()
    cw.setLayout(layout)

    # Create an empty flowchart with a single input and output
    fc = Flowchart(terminals={})
    w = fc.widget()
    layout.addWidget(fc.widget(), 0, 0, 2, 1)
    
    generate_plots_and_nodes()

    dippidNode = fc.createNode("DIPPID", pos=(0, 0))
    
    bufferNode_accelX = fc.createNode("Buffer", pos=(150, 0))
    bufferNode_accelY = fc.createNode("Buffer", pos=(150, 0))
    bufferNode_accelZ = fc.createNode("Buffer", pos=(150, 0))
    
    normalVectorNode = fc.createNode("NormalVector", pos=(0, 0))
    
    logNode = fc.createNode("Log", pos=(150, 0))
    
    #connect_nodes()
    
    win.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        sys.exit(QtGui.QApplication.instance().exec_())
