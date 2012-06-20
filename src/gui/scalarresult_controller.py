from PyQt4 import uic
formClass, qtBaseClass = uic.loadUiType('scalarresult_view.ui')

class ScalarResultController(qtBaseClass,formClass):
    def __init__(self,parent):
        qtBaseClass.__init__(self,parent)
        self.setupUi(self)  
        
        self._model = None
        
    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        self._model = value
        self.update(self._model.data)
        self._model.changedTo.connect(self.update)
        
    def update(self,newData):
        self.textView.setText(str(newData))
        

if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from result import ScalarResult
    from utility.quantities import Power
    import time
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    widgetUnderTest = ScalarResultController(window)

    testResult = ScalarResult()
    testResult.data = Power(1,'W')    
    widgetUnderTest.model = testResult
    
    
    window.setCentralWidget(widgetUnderTest)
    window.show()
        
    time.sleep(1)
    testResult.data = Power(2,'W')
        
        
    sys.exit(application.exec_())