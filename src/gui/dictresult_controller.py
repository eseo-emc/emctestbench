from PyQt4.QtGui import QWidget,QTableWidgetItem

from gui.dictresult_view import Ui_DictResult


class DictResultController(QWidget,Ui_DictResult):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
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
        self.tableWidget.clearContents() 
        rowCount = 0
        for key,value in self._model.data.iteritems():
            self.tableWidget.insertRow(rowCount)
            self.tableWidget.setItem(rowCount,0,QTableWidgetItem(key))
            self.tableWidget.setItem(rowCount,1,QTableWidgetItem(str(value)))
            rowCount += 1
        self.tableWidget.setRowCount(rowCount)
        


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    from result import DictResult
    from utility.quantities import Power
    import time
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    widgetUnderTest = DictResultController(window)

    testResult = DictResult()
    testResult.data = {'Voltage':4.9,'Power':Power(1,'W')}    
    widgetUnderTest.model = testResult
    
    
    window.setCentralWidget(widgetUnderTest)
    window.show()
        
#    time.sleep(1)
#    testResult.data = Power(2,'W')
        
        
    sys.exit(application.exec_())