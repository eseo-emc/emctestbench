from PyQt4.QtGui import QWidget
from gui.powerwidget_view import Ui_Form
from utility import quantities

import sys


class PowerWidgetController(QWidget,Ui_Form):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.setupUi(self)
        
        self.value.valueChanged.connect(self.valueEntered)
        self.unit.currentIndexChanged.connect(self.update)
        
        self._processChangeSignals = True
        
        self._model = None

    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        self._model = value
        self.update()        
        
    def update(self):
        self._processChangeSignals = False
        if self.unit.currentText() == 'W':
            self.value.setDecimals(4)
            self.value.setSingleStep(0.001)
            self.value.setMinimum(0.)
            self.value.setMaximum(100.)
        elif self.unit.currentText() == 'dBm':
            self.value.setDecimals(1)
            self.value.setSingleStep(0.1)
            self.value.setMinimum(-200.)
            self.value.setMaximum(50.)
            
        self.value.setValue(self.model.value.asUnit(self.unit.currentText()))
        self._processChangeSignals = True
    def valueEntered(self):
        if self._processChangeSignals:
            self.model.value = quantities.Power(self.value.value(),self.unit.currentText())
    


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from experiment import experiment
    from utility import quantities 
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    widgetUnderTest = PowerWidgetController(window)
    theModel = experiment.Property(quantities.Power(3,'dBm'))
    
    widgetUnderTest.model = theModel
    window.setCentralWidget(widgetUnderTest)
    window.show()
        
    sys.exit(application.exec_())