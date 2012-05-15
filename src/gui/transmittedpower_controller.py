from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget

from gui.transmittedpower_view import Ui_Form
from experiment.transmittedpower import TransmittedPower
from experimentresult import ExperimentResult

import numpy

class TransmittedPowerController(QWidget,Ui_Form):
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
        self.model.newResult.connect(self.newResult)        
        self.measure.clicked.connect(self.measureOnce)
        
    def measureNominalVoltage(self):
        self.model.prepare()
    def measureOnce(self):
        self.model.start()
    def newResult(self,result):
        self.generatorPower.setValue(result['Generator power'].dBm())
        self.forwardPower.setValue(result['Forward power'].dBm())
        self.reflectedPower.setValue(result['Reflected power'].dBm())
        self.transmittedPower.setValue(result['Transmitted power'].dBm())


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from device import knownDevices    
    from utility.quantities import Power
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    switchPlatform = knownDevices['switchPlatform']
    switchPlatform.setPreset('bridge')
    rfGenerator = knownDevices['rfGenerator']
    rfGenerator.setPower(Power(10,'dBm'))
    rfGenerator.enableOutput()
    
    
    controller = TransmittedPowerController(window)
    window.setCentralWidget(controller)
    window.show()
        
    sys.exit(application.exec_())