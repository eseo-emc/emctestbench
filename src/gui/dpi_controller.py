from PyQt4.QtCore import pyqtSignal
from gui.toplevelexperiment_controller import TopLevelExperimentController

from gui.dpi_view import Ui_Form
from experiment.dpi import Dpi

import numpy

class DpiController(TopLevelExperimentController,Ui_Form):
    def __init__(self,parent,topLevel=True):
        TopLevelExperimentController.__init__(self,parent,topLevel)
               
        self.criterion.label = 'Criterion'
        self.stimulus.label = 'Stimulus'
        
    def setModel(self):
        self.powerMinimum.model = self.model.powerMinimum        
        self.powerMaximum.model = self.model.powerMaximum
        
        self.frequencyMinimum.model = self.model.frequencies.start
        self.frequencyMaximum.model = self.model.frequencies.stop
        
        self.frequencySteps.setValue(self.model.frequencies.numberOfPoints.value)
        self.frequencySteps.valueChanged.connect(self.model.frequencies.numberOfPoints.setValue)
        
        self.logarithmic.setChecked(self.model.frequencies.logarithmic.value)
        self.logarithmic.stateChanged.connect(self.model.frequencies.logarithmic.setValue)     
        
        self.criterion.model = self.model.passCriterion
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