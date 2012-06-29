from PyQt4.QtGui import QComboBox

import sys

class EnumerateWidgetController(QComboBox):
    def __init__(self,parent):
        QComboBox.__init__(self,parent)
                
        self._processChangeSignals = 0
        self._model = None

    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        assert self._model == None,'{cls} does not support multiple model assignments'.format(cls=self.__class__.__name__)
        self._model = value
                
        self.addItems(self._model.possibleValues)
        
        self.update() 
        self.model.changed.connect(self.update)
        self.currentIndexChanged.connect(self.valueEntered)
                     
        
    def update(self):
        self._processChangeSignals -= 1
        itemNumber = self.findText(self.model._value)
        self.setCurrentIndex(itemNumber)
        self._processChangeSignals += 1
        
    def valueEntered(self):
        if self._processChangeSignals == 0:
            self.model.value = str(self.currentText())
    


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from experiment import experiment
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    widgetUnderTest = EnumerateWidgetController(window)
    theModel = experiment.EnumerateProperty('None',['Automatic','None','Prana','Milmega'])
    
    widgetUnderTest.model = theModel
    window.setCentralWidget(widgetUnderTest)
    window.show()
        
    sys.exit(application.exec_())
    
    