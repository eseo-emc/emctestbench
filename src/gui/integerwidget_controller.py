from PyQt4.QtGui import QSpinBox
from utility import quantities

import sys

class IntegerWidgetController(QSpinBox):
    def __init__(self,parent):
        QSpinBox.__init__(self,parent)
                
        self._processChangeSignals = 0
        self._model = None

    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        assert self._model == None,'{cls} does not support multiple model assignments'.format(cls=self.__class__.__name__)
        self._model = value
                
        if not(hasattr(self.model,'minimum')):
            print 'Warning: IntegerWidgetController wants a defined minimum'
            self.model.minimum = type(self.model.value)(0)
        if not(hasattr(self.model,'maximum')):
            print 'Warning: IntegerWidgetController wants a defined maximum'
            self.model.maximum = type(self.model.value)(100)
        
        self.update() 
        self.model.changed.connect(self.update)
        self.valueChanged.connect(self.valueEntered)
                     
        
    def update(self):
        self._processChangeSignals -= 1
        self.setMinimum(self.model.minimum)
        self.setMaximum(self.model.maximum)
        self.setValue(self.model.value)
        self._processChangeSignals += 1
        
    def valueEntered(self):
        if self._processChangeSignals == 0:
            self.model.value = type(self.model.value)(self.value())
    


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from experiment import experiment
    from utility import quantities 
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    widgetUnderTest = IntegerWidgetController(window)
    theModel = experiment.ScalarProperty(quantities.Integer(5),minimum=quantities.Integer(2),maximum=quantities.Integer(10))
    
    widgetUnderTest.model = theModel
    window.setCentralWidget(widgetUnderTest)
    window.show()
        
    sys.exit(application.exec_())