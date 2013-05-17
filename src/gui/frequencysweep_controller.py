from gui.toplevelexperiment_controller import TopLevelExperimentController

from PyQt4 import uic
formClass, qtBaseClass = uic.loadUiType('frequencysweep_view.ui')

class FrequencySweepController(TopLevelExperimentController,formClass):
    def __init__(self,parent,topLevel=True):
        TopLevelExperimentController.__init__(self,parent,topLevel)
        
        self.transmittedPower.label = 'Measurement'
        
    def setModel(self):
        self.generatorPower.model = self.model.generatorPower        
        self.transmittedPower.model = self.model.transmittedPower
        
        self.frequencyMinimum.model = self.model.frequencies.start
        self.frequencyMaximum.model = self.model.frequencies.stop
        self.frequencySteps.model = self.model.frequencies.numberOfPoints
        self.logarithmic.setChecked(self.model.frequencies.logarithmic.value)
        self.logarithmic.stateChanged.connect(self.model.frequencies.logarithmic.setValue)     
        
        self.transmittedPower.model = self.model.transmittedPower

    def enableInputs(self,enable):
        self.frequencyMinimum.setEnabled(enable)             
        self.frequencyMaximum.setEnabled(enable)             
        self.generatorPower.setEnabled(enable)             
        self.logarithmic.setEnabled(enable)  
        self.frequencySteps.setEnabled(enable)



if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from experiment import frequencysweep    
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    frequencySweepController = FrequencySweepController(window)
    frequencySweepController.model = frequencysweep.FrequencySweep()
    window.setCentralWidget(frequencySweepController)
    window.show()
        
    sys.exit(application.exec_())