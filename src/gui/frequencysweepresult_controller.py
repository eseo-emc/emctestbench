from PyQt4 import uic
formClass, qtBaseClass = uic.loadUiType('frequencysweepresult_view.ui')

class FrequencySweepResultController(qtBaseClass,formClass):
    powerUnit = 'dBm'    
    
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
        self.update(self._model)
        self._model.changedTo.connect(self.update)
        
        self.forwardReflected.toggled.connect(self.updateSettings) 
        self.s11.toggled.connect(self.updateSettings) 
        self.images.toggled.connect(self.updateSettings) 
        
    def updateSettings(self):
        self.update(self.model)
        
    def update(self,result):        
        if result is not None:
            frequency = result['frequency']
            
            self.frequencySweepGraph.axes.clear()
            self.frequencySweepGraph.axes.hold(True)

            if self.s11.isChecked():
                self.frequencySweepGraph.axes.plot(frequency, result['reflection coefficient'].asUnit('dB'),label='Reflection coefficient (S11)')          

            if self.forwardReflected.isChecked():
                self.frequencySweepGraph.axes.plot(frequency, result['forward power'].asUnit(self.powerUnit),label='Forward power ('+self.powerUnit+')')
                self.frequencySweepGraph.axes.plot(frequency, result['reflected power'].asUnit(self.powerUnit),label='Reflected power ('+self.powerUnit+')')
          
            if self.images.isChecked():
                self.frequencySweepGraph.axes.plot(frequency, result['forward power image'].asUnit(self.powerUnit),label='Forward power image ('+self.powerUnit+')')
                self.frequencySweepGraph.axes.plot(frequency, result['reflected power image'].asUnit(self.powerUnit),label='Reflected power image ('+self.powerUnit+')')

        
        self.frequencySweepGraph.axes.set_xlim(result.frequencyRange.start.value,result.frequencyRange.stop.value)
        self.frequencySweepGraph.axes.set_xscale('symlog' if self.model.frequencyRange.logarithmic.value else 'linear') 
        
        self.frequencySweepGraph.axes.set_xlabel('Frequency (Hz)')
        self.frequencySweepGraph.axes.set_ylabel('|S11| (dB)')
        self.frequencySweepGraph.axes.legend()
        self.frequencySweepGraph.draw() #redraw_in_frame()
#        self.frequencySweepGraph.figure.set_frameon(False)



if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from experiment.dpi import DpiResult
    from experiment.experiment import SweepRange
    from utility.quantities import Power
    from numpy import nan
    import datetime
    
    import experimentresult
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    widgetUnderTest = FrequencySweepResultController(window)

    experimentResult = experimentresult.ExperimentResult.loadFromFileSystem('D:\User_My_Documents\Instrument\My Documents\EmcTestbench\Calibration\Bench\None (86205A) reflect.xml')
    widgetUnderTest.model = experimentResult.result    
    
    window.setCentralWidget(widgetUnderTest)
    window.show()
        

        
    sys.exit(application.exec_())