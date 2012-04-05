from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget

from gui.dpi_view import Ui_Form
from experiment.dpi import Dpi

import numpy

class DpiController(QWidget,Ui_Form):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.setupUi(self)  
        
        self.model = Dpi()
        
        self.powerMinimum.setValue(self.model.powerMinimum.value)
        self.powerMinimum.valueChanged.connect(self.model.powerMinimum.setValue)

        self.powerMaximum.setValue(self.model.powerMaximum.value)
        self.powerMaximum.valueChanged.connect(self.model.powerMaximum.setValue)
        
        self.frequencyMinimum.setValue(self.model.frequencies.start.value)
        self.frequencyMinimum.valueChanged.connect(self.model.frequencies.start.setValue)
        
        self.frequencyMaximum.setValue(self.model.frequencies.stop.value)
        self.frequencyMaximum.valueChanged.connect(self.model.frequencies.stop.setValue)  
        
        self.logarithmic.setChecked(self.model.frequencies.logarithmic.value)
        self.logarithmic.stateChanged.connect(self.model.frequencies.logarithmic.setValue)
        
        self.updateGraph()
        self.model.resultChanged.connect(self.updateGraph)
        
        self.model.progressed.connect(self.progress.setValue)
        
        self.measurementStopped()
        self.model.started.connect(self.measurementStarted)
        self.model.finished.connect(self.measurementStopped)


    def enableInputs(self,enable):
        self.frequencyMinimum.setEnabled(enable)             
        self.frequencyMaximum.setEnabled(enable)             
        self.powerMinimum.setEnabled(enable)             
        self.powerMaximum.setEnabled(enable)             
        self.logarithmic.setEnabled(enable)             
        
    def measurementStarted(self):
        self.startStop.setText('Stop')
        self.startStop.clicked.disconnect()
        self.startStop.clicked.connect(self.model.stop)
        self.enableInputs(False)
        
    def measurementStopped(self):
        self.startStop.setText('Start')
        try:
            self.startStop.clicked.disconnect()
        except:
            pass
        self.startStop.clicked.connect(self.startMeasurement)
        self.enableInputs(True)
        
    def startMeasurement(self):
        self.model.connect()
        self.model.prepare()
        self.model.start()
        
#        x = numpy.linspace(-10, 10)
#        self.dpiGraph.axes.plot(x, x**2,label='Square')
#        self.dpiGraph.axes.hold()
#        self.dpiGraph.axes.plot(x, x**3,label='Cube')
#        self.dpiGraph.axes.legend()



    def updateGraph(self):
        result = self.model.result()
#        print result['frequencies'].values
        self.dpiGraph.axes.plot(result['frequencies'].values, result['forwardPowers'],label='Forward power')
        self.dpiGraph.axes.set_xlabel('Frequency (Hz)')
        self.dpiGraph.axes.set_ylabel('Power (dBm)')
        
        self.dpiGraph.axes.legend()
        
        self.dpiGraph.axes.set_ylim(result['powerLimits'])
        self.dpiGraph.axes.set_xlim(result['frequencies'].start.value,result['frequencies'].stop.value)
        self.dpiGraph.axes.set_xscale('symlog' if result['frequencies'].logarithmic.value else 'linear')        
        self.dpiGraph.draw() #redraw_in_frame()
#        self.dpiGraph.figure.set_frameon(False)
        


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    dpiController = DpiController(window)
    window.setCentralWidget(dpiController)
    window.show()
        
    sys.exit(application.exec_())