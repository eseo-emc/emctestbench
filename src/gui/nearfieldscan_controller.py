from gui.toplevelexperiment_controller import TopLevelExperimentController
from gui.nearfieldscan_view import Ui_Form

class NearFieldScanController(TopLevelExperimentController,Ui_Form):
    def __init__(self,parent,topLevel=True):
        TopLevelExperimentController.__init__(self,parent,topLevel)
        
        self.transmittedPower.label = 'Transmitted Power'
        self.measurement.label = 'Measurement'        

    def setModel(self):
        #TODO: create three-dimensional position property controller
        self.xStart.model = self.model.xPosition
        self.yStart.model = self.model.startPosition        
        self.yStop.model = self.model.stopPosition
        self.zStart.model = self.model.zPosition        
        
        #TODO: create integer property controller
        self.numberOfSteps.setValue(self.model.numberOfSteps.value)
        self.numberOfSteps.valueChanged.connect(self.model.numberOfSteps.setValue)

        self.generatorPower.model = self.model.generatorPower
        self.generatorFrequency.model = self.model.generatorFrequency
        
        self.measurement.model = self.model.measurement
        self.transmittedPower.model = self.model.transmittedPower

    def enableInputs(self,enable):
        self.xStart.setEnabled(enable)    
        self.yStart.setEnabled(enable)             
        self.yStop.setEnabled(enable)             
        self.zStart.setEnabled(enable)    
        self.numberOfSteps.setEnabled(enable)             
        self.generatorPower.setEnabled(enable)             
        self.generatorFrequency.setEnabled(enable)  
        

    
        


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from experiment import nearfieldscan    
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    controllerUnderTest = NearFieldScanController(window)
    controllerUnderTest.model = nearfieldscan.NearFieldScan()
    window.setCentralWidget(controllerUnderTest)
    window.show()
        
    sys.exit(application.exec_())