from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget

from gui.dpi_view import Ui_Form
from experiment.dpi import Dpi

import numpy

class DpiController(QWidget,Ui_Form):
    def __init__(self,parent,topLevel=True):
        QWidget.__init__(self,parent)
        self.setupUi(self)  
        self.topLevel = topLevel
        
        self._model = None        
#        self.fileView = DpiCsv()
    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        self._model = value
        
        self.powerMinimum.model = self.model.powerMinimum        
        self.powerMaximum.model = self.model.powerMaximum
        
        self.frequencyMinimum.model = self.model.frequencies.start
        self.frequencyMaximum.model = self.model.frequencies.stop
        
        self.frequencySteps.setValue(self.model.frequencies.numberOfPoints.value)
        self.frequencySteps.valueChanged.connect(self.model.frequencies.numberOfPoints.setValue)
        
        self.logarithmic.setChecked(self.model.frequencies.logarithmic.value)
        self.logarithmic.stateChanged.connect(self.model.frequencies.logarithmic.setValue)
              
        self.model.progressed.connect(self.progress.setValue)
        
        self.measurementStopped()
        self.model.started.connect(self.measurementStarted)
        self.model.finished.connect(self.measurementStopped)
        
        self.criterion.label = 'Criterion'
        self.criterion.model = self.model.passCriterion
        self.stimulus.label = 'Stimulus'
        self.stimulus.model = self.model.transmittedPower

    def enableInputs(self,enable):
        self.frequencyMinimum.setEnabled(enable)             
        self.frequencyMaximum.setEnabled(enable)             
        self.powerMinimum.setEnabled(enable)             
        self.powerMaximum.setEnabled(enable)             
        self.logarithmic.setEnabled(enable)  
        self.saveTransmittedPowers.setEnabled(enable)
        self.searchMethod.setEnabled(enable)    
        self.frequencySteps.setEnabled(enable)
        
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
        


    
        


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from experiment import dpi    
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    dpiController = DpiController(window)
    dpiController.model = dpi.Dpi()
    window.setCentralWidget(dpiController)
    window.show()
        
    sys.exit(application.exec_())