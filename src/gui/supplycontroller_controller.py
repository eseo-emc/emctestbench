from PyQt4 import uic
formClass, qtBaseClass = uic.loadUiType('supplycontroller_view.ui')

class SupplyControllerController(qtBaseClass,formClass):
    def __init__(self,parent,topLevel=True):
        qtBaseClass.__init__(self,parent)
        self.setupUi(self)  
        
        self.topLevel = topLevel
        
        self._model = None
        
    @property
    def model(self):    
        return self._model
    @model.setter
    def model(self,value):
        self._model = value
    
        self.model.connect()
        self.outputVoltage.model = self.model.outputVoltage
        self.outputCurrent.model = self.model.outputCurrent
        self.offOnTime.model = self.model.offOnTime
        self.startupTime.model = self.model.startupTime
        self.outputOn.model = self.model.outputOn
        
        
  
if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from experiment import supplycontroller
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    experiment = supplycontroller.SupplyController()
    controller = SupplyControllerController(window)
    controller.model = experiment

    
    window.setCentralWidget(controller)
    window.show()
        
    sys.exit(application.exec_())