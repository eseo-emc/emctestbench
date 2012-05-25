from PyQt4.QtGui import QWidget

class TopLevelExperimentController(QWidget):
    def __init__(self,parent,topLevel):
        QWidget.__init__(self,parent)
        self.setupUi(self)  
        
        self.topLevel = topLevel # shoudl be abolished
        self._model = None  
    
    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        self._model = value
        
        self.model.progressed.connect(self.progress.setValue)
        self.measurementStopped()
        self.model.started.connect(self.measurementStarted)
        self.model.finished.connect(self.measurementStopped)

        self.setModel()
    def setModel(self):
        raise NotImplementedError,'This method should be implemented by the subclass'
    def enableInputs(self):
        raise NotImplementedError,'This method should be implemented by the subclass'
            
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
        self.model.connect()
        self.model.prepare()
        self.model.start()
