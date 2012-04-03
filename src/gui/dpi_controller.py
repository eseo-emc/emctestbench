from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget

from gui.dpi_view import Ui_Form
from experiment.dpi import Dpi

import numpy

class DpiController(Ui_Form):
    def __init__(self,inspector):
        self.setupUi(inspector)        
        self.model = Dpi()
        
        self.powerMinimum.setValue(self.model.powerMinimum.value)
        self.powerMinimum.valueChanged.connect(self.model.powerMinimum.setValue)

        self.powerMaximum.setValue(self.model.powerMaximum.value)
        self.powerMaximum.valueChanged.connect(self.model.powerMaximum.setValue)
        
        self.frequencyMinimum.setValue(self.model.frequencies.start.value)
        self.frequencyMinimum.valueChanged.connect(self.model.frequencies.start.setValue)
        
        self.frequencyMaximum.setValue(self.model.frequencies.stop.value)
        self.frequencyMaximum.valueChanged.connect(self.model.frequencies.stop.setValue)  
        
        self.logarithmic.setChecked(self.model.frequencies.logarithmic.value)
        self.logarithmic.stateChanged.connect(self.model.frequencies.logarithmic.setValue)
        
        self.updateGraph()
        self.model.resultChanged.connect(self.updateGraph)
#        x = numpy.linspace(-10, 10)
##        self.dpiGraph.figure.gca().plot(x, x**2,label='Square')
##        self.dpiGraph.figure.gca().plot(x, x**3,label='Cube')
#        self.dpiGraph.axes.plot(x, x**3,label='Cube')
#        self.dpiGraph.axes.legend()



    def updateGraph(self):
        result = self.model.result()
#        print result['frequencies'].values
        self.dpiGraph.axes.plot(result['frequencies'].values, result['forwardPowers'],label='Forward power')
        self.dpiGraph.axes.set_xlabel('Frequency (Hz)')
        self.dpiGraph.axes.set_ylabel('Power (dBm)')
        
        self.dpiGraph.axes.legend()
        
        self.dpiGraph.axes.set_ylim(result['powerLimits'])
        self.dpiGraph.axes.set_xlim(result['frequencies'].start.value,result['frequencies'].stop.value)
        self.dpiGraph.axes.set_xscale('symlog' if result['frequencies'].logarithmic.value else 'linear')        
        self.dpiGraph.draw() #redraw_in_frame()


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    widget = QWidget()
    
    dpiController = DpiController(widget)
    window.setCentralWidget(widget)
    window.show()
        
        
    sys.exit(application.exec_())