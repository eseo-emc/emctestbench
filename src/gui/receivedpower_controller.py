from experiment import experiment
from utility import quantities

from PyQt4 import uic
formClass, qtBaseClass = uic.loadUiType('receivedpower_view.ui')

class ReceivedPowerController(qtBaseClass,formClass):
    def __init__(self,parent,topLevel=True):
        qtBaseClass.__init__(self,parent)
        self.setupUi(self) 
        self.topLevel = topLevel
        
        self._model = None
        self.result = experiment.Property(quantities.Power(0.0,'dBm'))
    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        self._model = value
        
        self.model.connect()
        
        self.span.model = self.model.span
        self.centerFrequency.model = self.model.centerFrequency
        
        #TODO: create integer property controller
        self.numberOfAveragingPoints.setValue(self.model.numberOfAveragingPoints.value)
        self.numberOfAveragingPoints.valueChanged.connect(self.model.numberOfAveragingPoints.setValue)

        self.model.newResult.connect(self.newResult)        
        self.receivedPower.model = self.result
#
        self.measure.clicked.connect(self.measureOnce)
        

    def measureOnce(self):
        self.model.prepare()
        self.model.measure()
    def newResult(self,result):
        self.result.setValue(result['received power'])

        


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from device import knownDevices  
    from experiment.receivedpower import ReceivedPower
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    positioner = knownDevices['positioner']
    positioner.prepare()
    
    
    controller = ReceivedPowerController(window)
    controller.model = ReceivedPower()
    window.setCentralWidget(controller)
    window.show()
        
    sys.exit(application.exec_())