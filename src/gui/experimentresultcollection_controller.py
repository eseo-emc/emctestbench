from PyQt4 import uic

from PyQt4.QtGui import QIcon,QMenu,QAction,QFileDialog,QInputDialog
from PyQt4.QtCore import pyqtSignal
from gui.experimentresultcollection import ExperimentResultCollection

from PyQt4.QtGui import QTreeWidgetItem

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
        viewName = self.experimentResult.name 
        if viewName == None:
            viewName = '<No name>'
        self.setText(0,viewName)  
        self.setText(2,self.experimentResult.metadata['creation'].strftime('%Y-%m-%d %H:%M:%S'))
    def addContextMenuActions(self,menu):
        deleteAction = QAction('Delete',menu)
        deleteAction.triggered.connect(self.delete)
        menu.addAction(deleteAction)
        
        renameAction = QAction('Rename',menu)
        renameAction.triggered.connect(self.rename)
        menu.addAction(renameAction)
        
        if len(self.experimentResult.result.exportFunctions()) > 0:
            exportAction = QAction('Export',menu)
            exportAction.triggered.connect(self.export)
            menu.addAction(exportAction)

        menu.addSeparator()            
        ExperimentResultTreeItem.addContextMenuActions(self,menu)
    def delete(self):
        self.experimentResult.delete()
    def rename(self):
        newName,success = QInputDialog.getText(self.parent(),'Rename ExperimentResult:',self.experimentResult.name)
        if success and newName != '':
            self.experimentResult.name = newName
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
            fileName = selectedExportFunction.exportType.appendExtensionToFileName( str(dialog.selectedFiles()[0]) )
            selectedExportFunction(fileName)


formClass, qtBaseClass = uic.loadUiType('experimentresultcollection_view.ui')
  
class ExperimentResultCollectionController(qtBaseClass,formClass):
    experimentResultSelected = pyqtSignal(object)
    changed = pyqtSignal()
    
    def __init__(self,parent=None):
        qtBaseClass.__init__(self,parent)
        self.setupUi(self)
        
        self.model = ExperimentResultCollection.Instance()
        self.model.changed.connect(self.update)

        self.theTreeWidget.doubleClicked.connect(self.itemDoubleClicked)
#        self.theTreeWidget.itemClicked.connect(self.itemClicked)
        self.theTreeWidget.customContextMenuRequested.connect(self.treeContextMenuRequested)

        
    def update(self):
        self.theTreeWidget.setHeaderLabels(['Name','Experiment','Date','Operator','DUT'])
        self.theTreeWidget.setColumnWidth(0,200)
        
        self.theTreeWidget.clear()
        for experimentResult in self.model.experimentResults:
            ExperimentResultItem(experimentResult,parent=self.theTreeWidget)
        
        self.changed.emit()
   
    def treeContextMenuRequested(self,point):
        selectedItems = self.theTreeWidget.selectedItems()
        if len(selectedItems) == 1:
            menu = QMenu()
            selectedItems[0].addContextMenuActions(menu)
            menu.exec_(self.theTreeWidget.mapToGlobal(point))      
#    def itemClicked(self,index,column):
#        print index,column        
    def itemDoubleClicked(self,index):
        
        
        selectedExperimentResult = self.theTreeWidget.selectedItems()[0].experimentResult
        self.experimentResultSelected.emit(selectedExperimentResult)
        
        self.model.changed.emit()
    
        
if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    
    from gui.experimentresult import ExperimentResult
    
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