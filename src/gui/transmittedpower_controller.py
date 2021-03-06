from PyQt4 import uic
formClass, qtBaseClass = uic.loadUiType('transmittedpower_view.ui')

class TransmittedPowerController(qtBaseClass,formClass):
    def __init__(self,parent,topLevel=True):
        qtBaseClass.__init__(self,parent)
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
        self.amplifier.model = self.model.amplifier
        self.model.newResult.connect(self.newResult)        
        self.measure.clicked.connect(self.measureOnce)
        
    def measureNominalVoltage(self):
        self.model.prepare()
    def measureOnce(self):
        self.model.start()
    def newResult(self,result):
        self.generatorPower.setValue(result['generator power'].dBm())
        self.forwardPower.setValue(result['forward power'].dBm())
        self.reflectedPower.setValue(result['reflected power'].dBm())
        self.transmittedPower.setValue(result['transmitted power'].dBm())


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from device import knownDevices    
    from utility.quantities import Power
    from experiment import transmittedpower
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    experiment = transmittedpower.TransmittedPower()
    
    controller = TransmittedPowerController(window)
    controller.model = experiment

    experiment.generatorPower = Power(3,'dBm')
    
    window.setCentralWidget(controller)
    window.show()
        
    sys.exit(application.exec_())