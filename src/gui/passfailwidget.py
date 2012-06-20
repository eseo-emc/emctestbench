from PyQt4.QtGui import QIcon

import sys

from PyQt4 import uic
formClass, qtBaseClass = uic.loadUiType('passfailwidget_view.ui')

class PassFailWidget(qtBaseClass,formClass):
    def __init__(self,parent):
        qtBaseClass.__init__(self,parent)
        self.setupUi(self)
        
        self.passNotFail = None
        
    @property
    def passNotFail(self):
        return self._passNotFail
    @passNotFail.setter
    def passNotFail(self,value):
        self._passNotFail = value
        if value == True:
            self.button.setIcon(QIcon(':/logging/Success'))
            self.text.setText('PASS')
        elif value == False:
            self.button.setIcon(QIcon(':/logging/Error'))
            self.text.setText('FAIL')
        else:
            self.button.setIcon(QIcon(':/logging/Unknown'))
            self.text.setText('Unknown')


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    widgetUnderTest = PassFailWidget(window)
    widgetUnderTest.passNotFail = False
    window.setCentralWidget(widgetUnderTest)
    window.show()
        
    sys.exit(application.exec_())