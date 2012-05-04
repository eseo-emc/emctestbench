from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignal
from gui.experimentresultcollection_view import Ui_ExperimentResultCollection
from gui.experimentresultcollection import ExperimentResultCollection

from PyQt4.QtGui import QTreeWidgetItem

import logging

class ExperimentResultTreeItem(QTreeWidgetItem):   
    def __init__(self,experimentResult,parent=None):
        QTreeWidgetItem.__init__(self,parent)
        if parent:
            self.parent = (lambda : parent)
        self.experimentResult = experimentResult
        
        self.setText(0,self.experimentResult.metadata['Name'])  
        self.setText(2,self.experimentResult.metadata['Creation'].strftime('%H:%m:%S'))
        
    
class ExperimentResultCollectionController(QWidget,Ui_ExperimentResultCollection):
    experimentResultSelected = pyqtSignal(object)
    
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setupUi(self)
        
        self.model = ExperimentResultCollection.Instance()
        self.model.changed.connect(self.update)

        self.theTreeWidget.doubleClicked.connect(self.itemDoubleClicked)

        
    def update(self):
        self.theTreeWidget.setHeaderLabels(['Name','Experiment','Date','Operator','DUT'])
        self.theTreeWidget.setColumnWidth(0,200)
        
        self.theTreeWidget.clear()
        for experimentResult in self.model.experimentResults:
            ExperimentResultTreeItem(experimentResult,parent=self.theTreeWidget)
            
    def itemDoubleClicked(self,index):
        selectedExperimentResult = self.theTreeWidget.selectedItems()[0].experimentResult
        self.experimentResultSelected.emit(selectedExperimentResult)
        
    
        
if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    
    from gui.experimentresultcollection import ExperimentResult
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    widgetUnderTest = ExperimentResultCollectionController(window)
    window.setCentralWidget(widgetUnderTest)
    window.show()
        
    class DummyExperiment:
        name = 'DummyExperiment'
    dummyExperiment = DummyExperiment()
    ExperimentResult(dummyExperiment,3)
    
    sys.exit(application.exec_())