from gui.toplevelexperiment_controller import TopLevelExperimentController

from PyQt4 import uic
formClass, qtBaseClass = uic.loadUiType('sweep_view.ui')

class SweepController(TopLevelExperimentController,formClass):
    def __init__(self,parent,topLevel=True):
        TopLevelExperimentController.__init__(self,parent,topLevel)
        
        self.measurement.label = 'Measurement'
        self.stimulus.label = 'Stimulus'
        
    def setModel(self):
        self.measurement.model = self.model.measurement        
        self.stimulus.model = self.model.stimulus
        
        self.stimulusMinimum.model = self.model.stimulusRange.start
        self.stimulusMaximum.model = self.model.stimulusRange.stop
        self.stimulusSteps.model = self.model.stimulusRange.numberOfPoints
        self.logarithmic.setChecked(self.model.stimulusRange.logarithmic.value)
        self.logarithmic.stateChanged.connect(self.model.stimulusRange.logarithmic.setValue)     

    def enableInputs(self,enable):
        self.stimulusMinimum.setEnabled(enable)             
        self.stimulusMaximum.setEnabled(enable)                       
        self.logarithmic.setEnabled(enable)  
        self.stimulusSteps.setEnabled(enable)



if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from experiment import sweep    
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    sweepController = SweepController(window)
    sweepController.model = sweep.Sweep()
    window.setCentralWidget(sweepController)
    window.show()
        
    sys.exit(application.exec_())