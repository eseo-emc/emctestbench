from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget

from gui.voltagecriterion_view import Ui_Form
from experiment.voltagecriterion import VoltageCriterion

from experimentresult import ExperimentResult
from experiment import experiment
from utility import quantities

import numpy

class VoltageCriterionController(QWidget,Ui_Form):
    def __init__(self,parent,topLevel=True):
        QWidget.__init__(self,parent)
        self.setupUi(self) 
        self.topLevel = topLevel
        
        self._model = None
        self.result = experiment.Property(quantities.Voltage(0.0))
    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        self._model = value
        
        self.model.connect()
        
        self.nominalVoltage.model = self.model.undisturbedOutputVoltage
        self.voltageMargin.model = self.model.voltageMargin


        self.model.newResult.connect(self.newResult)        
        self.measuredVoltage.model = self.result
        
        self.measureNominal.clicked.connect(self.measureNominalVoltage) 
        self.measure.clicked.connect(self.measureOnce)
        
    def measureNominalVoltage(self):
        self.model.prepare()
    def measureOnce(self):
        self.model.start()
    def newResult(self,result):
        self.result.setValue(result['voltage'])
        self.passFailIndicator.passNotFail = result['pass']

        


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from device import knownDevices  
    from experiment import voltagecriterion
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    switchPlatform = knownDevices['switchPlatform']
    switchPlatform.setPreset('bridge')
    
    
    controller = VoltageCriterionController(window)
    controller.model = voltagecriterion.VoltageCriterion()
    window.setCentralWidget(controller)
    window.show()
        
    sys.exit(application.exec_())