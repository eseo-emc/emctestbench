from PyQt4.QtGui import QCheckBox

import sys

class BooleanWidgetController(QCheckBox):
    def __init__(self,parent):
        QCheckBox.__init__(self,parent)
                
        self._processChangeSignals = 0
        self._model = None

    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        assert self._model == None,'{cls} does not support multiple model assignments'.format(cls=self.__class__.__name__)
        self._model = value     
        self.update() 
        self.model.changed.connect(self.update)
        self.stateChanged.connect(self.valueEntered)
                     
        
    def update(self):
        self._processChangeSignals -= 1
#        print self._processChangeSignals,'update',self.model.value
        self.setCheckState((2 if self.model.value else 0))
        self._processChangeSignals += 1
        
    def valueEntered(self,newValue):
        if self._processChangeSignals == 0:
#            print self._processChangeSignals,'valueEntered',newValue==2
            self.model.value = self.isChecked()
    


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from experiment import experiment
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    widgetUnderTest = BooleanWidgetController(window)
    theModel = experiment.BooleanProperty(True)
    
    widgetUnderTest.model = theModel
    window.setCentralWidget(widgetUnderTest)
    window.show()
        
    sys.exit(application.exec_())
    
    