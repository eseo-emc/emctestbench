from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget

from gui.voltagecriterion_view import Ui_Form
from experiment.dpi import VoltageCriterion

import numpy

class VoltageCriterionController(QWidget,Ui_Form):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.setupUi(self)  
        
        self.model = VoltageCriterion()
        
        


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    controller = VoltageCriterionController(window)
    window.setCentralWidget(controller)
    window.show()
        
    sys.exit(application.exec_())