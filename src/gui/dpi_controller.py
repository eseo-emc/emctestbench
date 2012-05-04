from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget

from gui.dpi_view import Ui_Form
from experiment.dpi import Dpi
from gui.dpicsv_view import DpiCsv
from experimentresultcollection import ExperimentResult


import numpy

class DpiController(QWidget,Ui_Form):
    def __init__(self,parent,topLevel=True):
        QWidget.__init__(self,parent)
        self.setupUi(self)  
        self.topLevel = topLevel
        
        self.model = Dpi()
        self.fileView = DpiCsv()
        
        self.powerMinimum.setValue(self.model.powerMinimum.value)
        self.powerMinimum.valueChanged.connect(self.model.powerMinimum.setValue)

        self.powerMaximum.setValue(self.model.powerMaximum.value)
        self.powerMaximum.valueChanged.connect(self.model.powerMaximum.setValue)
        
        self.frequencyMinimum.setValue(self.model.frequencies.start.value)
        self.frequencyMinimum.valueChanged.connect(self.model.frequencies.start.setValue)
        
        self.frequencyMaximum.setValue(self.model.frequencies.stop.value)
        self.frequencyMaximum.valueChanged.connect(self.model.frequencies.stop.setValue)  
        
        self.frequencySteps.setValue(self.model.frequencies.numberOfPoints.value)
        self.frequencySteps.valueChanged.connect(self.model.frequencies.numberOfPoints.setValue)
        
        self.logarithmic.setChecked(self.model.frequencies.logarithmic.value)
        self.logarithmic.stateChanged.connect(self.model.frequencies.logarithmic.setValue)
              

     
        self.model.newResult.connect(self.newResult)
        self.model.progressed.connect(self.progress.setValue)
        
        self.measurementStopped()
        self.model.started.connect(self.measurementStarted)
        self.model.finished.connect(self.measurementStopped)
        
        self.criterion.label = 'Criterion'
        self.criterion.selectExperiment('VoltageCriterion')
        self.stimulus.label = 'Stimulus'
        self.stimulus.selectExperiment('TransmittedPower')

    def enableInputs(self,enable):
        self.frequencyMinimum.setEnabled(enable)             
        self.frequencyMaximum.setEnabled(enable)             
        self.powerMinimum.setEnabled(enable)             
        self.powerMaximum.setEnabled(enable)             
        self.logarithmic.setEnabled(enable)  
        self.saveTransmittedPowers.setEnabled(enable)
        self.searchMethod.setEnabled(enable)    
        self.frequencySteps.setEnabled(enable)
        
    def measurementStarted(self):
        self.startStop.setText('Stop')
        self.startStop.clicked.disconnect()
        self.startStop.clicked.connect(self.model.stop)
        self.enableInputs(False)
        
    def measurementStopped(self):
        self.startStop.setText('Start')
        try:
            self.startStop.clicked.disconnect()
        except:
            pass
        self.startStop.clicked.connect(self.startMeasurement)
        self.enableInputs(True)
        
    def startMeasurement(self):
        self.model.passCriterion = self.criterion.experiment
        self.model.transmittedPower = self.stimulus.experiment
        self.model.connect()
        self.model.prepare()
        self.model.start()
        
    def newResult(self,result):
        if self.topLevel:
            ExperimentResult(self.model,result)

    
        


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    dpiController = DpiController(window)
    window.setCentralWidget(dpiController)
    window.show()
        
    sys.exit(application.exec_())