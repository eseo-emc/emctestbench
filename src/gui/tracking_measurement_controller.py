import sys
from PyQt4.QtGui import QMainWindow, QApplication
#from gui.matplotlibwidget import MatplotlibWidget
from numpy import linspace
from PyQt4 import QtCore

from experiment.tracking_measurement import TrackingMeasurement

from PyQt4 import uic
formClass, qtBaseClass = uic.loadUiType('tracking_measurement_view.ui')

class TrackingMeasurementController(qtBaseClass,formClass):
    def __init__(self):
        qtBaseClass.__init__(self)
        self.setupUi(self) 

#        self.model = TrackingMeasurement(linspace(2e9,20e9,101))
        self.model = TrackingMeasurement(linspace(1e6,6e9,101))

        self.timer = QtCore.QTimer()

        self.graph.axes.hold(True)
#        self.aPlot = self.graph.axes.plot(self.model.frequencies,self.model.powerA.asUnit('dBm'),label='A')
        self.bPlot = self.graph.axes.plot(self.model.frequencies,self.model.powerB.asUnit('dBm'),label='B')
        self.cursor = self.graph.axes.plot([0,0],[-60,20],label="Cursor")        
        self.graph.axes.set_xlabel = 'Power (dBm)'
        self.graph.axes.set_ylabel = 'Frequency (Hz)'     
        self.graph.axes.legend()

        self.model.dataChanged.connect(self.updateGraphs)
        
        self.timer.timeout.connect(self.sweepOnce)
        self.start.clicked.connect(self.sweepOnce)
#        self.sweepOnce()

    def updateGraphs(self):
        
#        self.aPlot[0].set_data(self.model.frequencies.asUnit('Hz'),self.model.powerA.asUnit('dBm'))
        if self.differential.isChecked():
            self.graph.axes.set_ylim(-5,5)
            self.bPlot[0].set_data(self.model.frequencies.asUnit('Hz'),(self.model.powerB/self.model.referencePowerB).asUnit('dB'))
        else:
            self.graph.axes.set_ylim(-35,0)
            self.bPlot[0].set_data(self.model.frequencies.asUnit('Hz'),self.model.powerB.asUnit('dBm'))
  
        self.cursor[0].set_data([self.model.currentFrequency]*2,[-60,20])        
        self.graph.draw()

        
    def sweepOnce(self):
        self.model.measure() 
#        self.updateGraphs()
        if self.continuous.isChecked():       
            self.timer.start(10) #ms



    
app = QApplication(sys.argv)
win = TrackingMeasurementController()
win.show()
sys.exit(app.exec_())
    
