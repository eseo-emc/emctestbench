from PyQt4.QtGui import QWidget,QIcon,QMenu,QAction,QFileDialog
from PyQt4.QtCore import pyqtSignal
from gui.experimentresultcollection_view import Ui_ExperimentResultCollection
from gui.experimentresultcollection import ExperimentResultCollection

from PyQt4.QtGui import QTreeWidgetItem

import logging

class ExperimentResultTreeItem(QTreeWidgetItem):   
    def __init__(self,parent=None):
        QTreeWidgetItem.__init__(self,parent)
        if parent:
            self.parent = (lambda : parent)
    def addContextMenuActions(self,menu):
        refreshAction = QAction('Refresh all',menu)
        refreshAction.triggered.connect(ExperimentResultCollection.Instance().refresh)
        menu.addAction(refreshAction) 
        
        
class ExperimentResultItem(ExperimentResultTreeItem):
    def __init__(self,experimentResult,parent=None):
        ExperimentResultTreeItem.__init__(self,parent)
        self.setIcon(0,QIcon(':/results/ExperimentResult.png'))        
        
        self.experimentResult = experimentResult
        self.update()
        self.experimentResult.changed.connect(self.update)
    def update(self):
        self.setText(0,self.experimentResult.name)  
        self.setText(2,self.experimentResult.metadata['Creation'].strftime('%H:%M:%S'))
    def addContextMenuActions(self,menu):
        ExperimentResultTreeItem.addContextMenuActions(self,menu)
        if len(self.experimentResult.result.exportFunctions()) > 0:
            menu.addSeparator()
            exportAction = QAction('Export',menu)
            exportAction.triggered.connect(self.export)
            menu.addAction(exportAction)
    def export(self):
        exportFunctions = self.experimentResult.result.exportFunctions()
        exportStrings = []
        for exportFunction in exportFunctions:
            exportType = exportFunction.exportType
            exportStrings.append(exportType.name + ' (' + ' '.join(exportType.globFilters()) + ')')
        dialog = QFileDialog(None,'Export '+self.experimentResult.result.name + '...')
        dialog.selectFile(self.experimentResult.name)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilter(';;'.join(exportStrings))
        if dialog.exec_() == dialog.Accepted:
            selectedExportFunction = exportFunctions[exportStrings.index(dialog.selectedFilter())]
            fileName = selectedExportFunction.exportType.appendExtensionToFileName( dialog.selectedFiles()[0] )
            selectedExportFunction(fileName)

        
    
class ExperimentResultCollectionController(QWidget,Ui_ExperimentResultCollection):
    experimentResultSelected = pyqtSignal(object)
    changed = pyqtSignal()
    
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setupUi(self)
        
        self.model = ExperimentResultCollection.Instance()
        self.model.changed.connect(self.update)

        self.theTreeWidget.doubleClicked.connect(self.itemDoubleClicked)
        self.theTreeWidget.customContextMenuRequested.connect(self.treeContextMenuRequested)

        
    def update(self):
        self.theTreeWidget.setHeaderLabels(['Name','Experiment','Date','Operator','DUT'])
        self.theTreeWidget.setColumnWidth(0,200)
        
        self.theTreeWidget.clear()
        for experimentResult in self.model.experimentResults:
            ExperimentResultItem(experimentResult,parent=self.theTreeWidget)
        
        self.changed.emit()
   
    def treeContextMenuRequested(self,point):
        menu = QMenu()
        self.theTreeWidget.selectedItems()[0].addContextMenuActions(menu)
        menu.exec_(self.theTreeWidget.mapToGlobal(point))      
            
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
    widgetUnderTest.model.refresh()
        
#    class DummyExperiment:
#        name = 'DummyExperiment'
#    dummyExperiment = DummyExperiment()
#    ExperimentResult(dummyExperiment,3)
    
    sys.exit(application.exec_())