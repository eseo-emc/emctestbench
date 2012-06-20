from PyQt4.QtGui import QApplication,QTreeWidget,QTreeWidgetItem,QIcon,QMenu,QAction,QDesktopServices,QDrag
from PyQt4.QtCore import QUrl, pyqtSignal, QMimeData
from PyQt4.QtCore import Qt

from experimentcollection import ExperimentCollection
from devicecollection import DeviceCollection
#import log

class ExperimentTreeItem(QTreeWidgetItem):   
    def __init__(self,parent=None,name=None):
        QTreeWidgetItem.__init__(self,parent)
        if name:
            self.setText(0,name)
        if parent:
            self.parent = (lambda : parent)
    def addContextMenuActions(self,menu):
        refreshAction = QAction('Refresh all',menu)
        refreshAction.triggered.connect(DeviceCollection.Instance().refresh)
        menu.addAction(refreshAction)
    
        
class ExperimentItem(ExperimentTreeItem):
    def __init__(self,experiment):
        ExperimentTreeItem.__init__(self)
        self.experiment = experiment
        self.setText(0,experiment.name)
        self.setIcon(0,QIcon(':/results/Experiment.png'))
    def addContextMenuActions(self,menu):
        ExperimentTreeItem.addContextMenuActions(self,menu)
        menu.addSeparator()
        noneAction = QAction('None',menu)
        noneAction.setEnabled(False)
        menu.addAction(noneAction)

class DeviceItem(ExperimentTreeItem):
    def __init__(self,device):
        ExperimentTreeItem.__init__(self)
        self.device = device
        self.update()
        self.device.changed.connect(self.update)
        self.setIcon(0,QIcon(':/devices/'+self.device.iconName+'.png'))
    def update(self):        
        self.setToolTip(0,self.device.detailedInformation)
        self.setText(0,str(self.device))
    def addContextMenuActions(self,menu):
        ExperimentTreeItem.addContextMenuActions(self,menu)
        menu.addSeparator()
        onlineAction = QAction('Put Online',menu)
        onlineAction.triggered.connect(self.device.putOnline)
        menu.addAction(onlineAction)
        attentionAction = QAction('Draw Attention',menu)
        attentionAction.triggered.connect(self.device.drawAttention)
        menu.addAction(attentionAction)
        
        if hasattr(self.device,'documentation'):
            documentationMenu = QMenu('Documentation',menu)
            for name,url in self.device.documentation.items():
                urlAction = QAction(name,menu)
                      
                urlAction.triggered.connect(lambda : QDesktopServices.openUrl(QUrl(url)))
                documentationMenu.addAction(urlAction)
            menu.addAction(documentationMenu.menuAction())

class ExperimentTreeWidget(QTreeWidget):
    experimentSelected = pyqtSignal(object)    
    
    def __init__(self,parent):
        QTreeWidget.__init__(self,parent)
        
        self.devices = ExperimentTreeItem(self,'Devices')      
        self.experiments = ExperimentTreeItem(self,'Experiments')      
        
        self.dragStartPosition = None
        
        DeviceCollection.Instance().changed.connect(self.updateDevices)
        ExperimentCollection.Instance().changed.connect(self.updateExperiments)
        
        self.customContextMenuRequested.connect(self.treeContextMenuRequested)
    
    def treeContextMenuRequested(self,point):
        menu = QMenu()
        self.selectedItems()[0].addContextMenuActions(menu)
        menu.exec_(self.mapToGlobal(point))        
    
    def _selectedExperiment(self):
        selectedItems = self.selectedItems()
        if len(selectedItems) == 1 and selectedItems[0].parent() == self.experiments:
            return selectedItems[0].experiment
        else:
            return None
    
    def mouseDoubleClickEvent(self,mouseEvent):
        QTreeWidget.mouseDoubleClickEvent(self,mouseEvent)
#        print 'mouseDoubleClickEvent'
        if self._selectedExperiment():
            self.experimentSelected.emit(self._selectedExperiment())
    
    def mousePressEvent(self,mouseEvent):
        QTreeWidget.mousePressEvent(self,mouseEvent)
#        http://doc.qt.nokia.com/4.7-snapshot/dnd.html
        if mouseEvent.button() != Qt.LeftButton:
            return
        if self._selectedExperiment():
            self.dragStartPosition = mouseEvent.pos()
            
    def mouseMoveEvent(self,mouseEvent):
#        if mouseEvent.button() != Qt.LeftButton:
#            return
        if not self._selectedExperiment():
            return
        if not self.dragStartPosition:
            return
        if (mouseEvent.pos()-self.dragStartPosition).manhattanLength() < QApplication.startDragDistance():
            return
        
        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.setText(self._selectedExperiment().__name__)
        drag.setMimeData(mimeData)
        drag.exec_()
    
    def updateDevices(self):
        for device in DeviceCollection.Instance().devices.values():
            self.devices.insertChild(0,(DeviceItem(device)))
        self.devices.setExpanded(True)
    
    #TODO: Refactor with updateDevices
    def updateExperiments(self):
        for experiment in ExperimentCollection.Instance().experiments:
            self.experiments.insertChild(0,ExperimentItem(experiment))
        self.experiments.setExpanded(True)   
        

if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow
    
    application = QApplication(sys.argv)
    window = QMainWindow()
    
    widget = ExperimentTreeWidget(window)
    window.setCentralWidget(widget)
    window.show()
#    widget.updateDevices()
#    widget.updateExperiments()        
    sys.exit(application.exec_())