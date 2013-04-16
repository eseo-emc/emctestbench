from gui.toplevelexperiment_controller import TopLevelExperimentController

from PyQt4 import uic
formClass, qtBaseClass = uic.loadUiType('nearfieldscan_view.ui')

class NearFieldScanController(TopLevelExperimentController,formClass):
    def __init__(self,parent,topLevel=True):
        TopLevelExperimentController.__init__(self,parent,topLevel)
        
        self.transmittedPower.label = 'Transmitted Power'
        self.measurement.label = 'Measurement'        

    def setModel(self):
        self.model.connect()        
        
        #TODO: create three-dimensional position property controller
        self.xStart.model = self.model.xPosition
        self.yStart.model = self.model.startPosition        
        self.yStop.model = self.model.stopPosition
        self.zStart.model = self.model.zPosition        
        
        self.numberOfSteps.model = self.model.numberOfSteps

        self.generatorPower.model = self.model.generatorPower
        self.generatorFrequency.model = self.model.generatorFrequency
        
        self.measurement.model = self.model.measurement
        self.transmittedPower.model = self.model.transmittedPower
        
        self.readStartPosition.clicked.connect(self.model.readStartPosition)
        self.readStopPosition.clicked.connect(self.model.readStopPosition)
        self.rehearsePath.clicked.connect(self.model.rehearsePath)

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