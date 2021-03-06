from utility import quantities

import sys
import numpy

from PyQt4 import uic
formClass, qtBaseClass = uic.loadUiType('powerwidget_view.ui')

class QuantityWidgetController(qtBaseClass,formClass):
    def __init__(self,parent):
        qtBaseClass.__init__(self,parent)
        self.setupUi(self)
        
#        self.value.setMinimum(0)
#        self.value.setMaximum(1e99)
        self.value.setDecimals(3)
        self.value.setSingleStep(1.)
        
        self._processChangeSignals = 0
        
        self._model = None

    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        assert self._model == None,'{cls} does not support multiple model assignments'.format(cls=self.__class__.__name__)
        self._model = value
        self._fillUnitMenu(self.model.value.storageUnit)
        
        if not(hasattr(self.model,'minimum')):
            print 'Warning: QuantityWidget wants a defined minimum'
            self.model.minimum = type(self.model.value)(0)
        if not(hasattr(self.model,'maximum')):
            print 'Warning: QuantityWidget wants a defined maximum'
            self.model.maximum = type(self.model.value)(+numpy.inf)
        
        self.update() 
        self.model.changed.connect(self.update)
        self.value.valueChanged.connect(self.valueEntered)
        self.unit.currentIndexChanged.connect(self.update)
            
    def setReadOnly(self,value):
        self.value.setReadOnly(value)
        
    def _fillUnitMenu(self,unit):
        self.unit.clear()
        self._units = []
        for prefix in quantities.siPrefices:
            self._units.append(prefix+unit)
            self.unit.addItem(prefix+unit)
            
        self.unit.setCurrentIndex(self._units.index(self.model.value.preferredUnit()))
        
        
    def update(self):
        self._processChangeSignals -= 1
        self.value.setMinimum(self.model.minimum.asUnit(str(self.unit.currentText())))
        self.value.setMaximum(self.model.maximum.asUnit(str(self.unit.currentText())))
        self.value.setValue(self.model.value.asUnit(str(self.unit.currentText())))
        self._processChangeSignals += 1
    def valueEntered(self):
        if self._processChangeSignals == 0:
            self.model.value = type(self.model.value)(self.value.value(),unit=str(self.unit.currentText()))
    


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from experiment import experiment
    from utility import quantities 
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    widgetUnderTest = QuantityWidgetController(window)
    theModel = experiment.Property(quantities.Frequency(3e9,'Hz'))
    
    widgetUnderTest.model = theModel
    window.setCentralWidget(widgetUnderTest)
    window.show()
        
    sys.exit(application.exec_())