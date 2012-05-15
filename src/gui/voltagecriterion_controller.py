from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget

from gui.voltagecriterion_view import Ui_Form
from experiment.voltagecriterion import VoltageCriterion

from experimentresult import ExperimentResult

import numpy

class VoltageCriterionController(QWidget,Ui_Form):
    def __init__(self,parent,topLevel=True):
        QWidget.__init__(self,parent)
        self.setupUi(self) 
        self.topLevel = topLevel
        
        self._model = None
    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        self._model = value
        
        self.model.connect()
        
        def coupleValue(guiWidget,modelProperty):
            guiWidget.setValue(modelProperty.value)
            modelProperty.changedTo.connect(guiWidget.setValue)
            guiWidget.valueChanged.connect(modelProperty.setValue)
        
        coupleValue(self.nominalVoltage,self.model.undisturbedOutputVoltage)
        coupleValue(self.voltageMargin,self.model.voltageMargin)        
#        coupleValue(self.measuredVoltage,self.model.result)        
        self.model.newResult.connect(self.newResult)        
        
        
        self.measureNominal.clicked.connect(self.measureNominalVoltage) 
        self.measure.clicked.connect(self.measureOnce)
        
    def measureNominalVoltage(self):
        self.model.prepare()
    def measureOnce(self):
        self.model.start()
    def newResult(self,result):
        self.measuredVoltage.setValue(result['Voltage'])
        self.passFailIndicator.passNotFail = result['Pass']

        


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from device import knownDevices    
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    switchPlatform = knownDevices['switchPlatform']
    switchPlatform.setPreset('bridge')
    
    
    controller = VoltageCriterionController(window)
    window.setCentralWidget(controller)
    window.show()
        
    sys.exit(application.exec_())