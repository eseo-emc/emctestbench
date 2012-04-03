from PyQt4.QtGui import QTreeWidget,QTreeWidgetItem,QIcon,QMenu,QAction,QDesktopServices
from PyQt4.Qt import Qt
from PyQt4.QtCore import QUrl, pyqtSignal

from experimentcollection import ExperimentCollection
from devicecollection import DeviceCollection
#import logging

class SystemTreeItem(QTreeWidgetItem):   
    def __init__(self,parent=None,name=None):
        QTreeWidgetItem.__init__(self,parent)
        if name:
            self.setText(0,name)
        if parent:
            self.parent = (lambda : parent)
    def addContextMenuActions(self,menu):
        print self.parent
        print self.parent()
        refreshAction = QAction('Refresh all',menu)
        refreshAction.triggered.connect(DeviceCollection.Instance().refresh)
        menu.addAction(refreshAction)
    
        
class ExperimentItem(SystemTreeItem):
    def __init__(self,experiment):
        SystemTreeItem.__init__(self)
        self.experiment = experiment
        self.setText(0,experiment.name)
    def addContextMenuActions(self,menu):
        SystemTreeItem.addContextMenuActions(self,menu)
        menu.addSeparator()
        noneAction = QAction('None',menu)
        noneAction.setEnabled(False)
        menu.addAction(noneAction)

class DeviceItem(SystemTreeItem):
    def __init__(self,device):
        SystemTreeItem.__init__(self)
        self.device = device
        self.update()
        self.device.changed.connect(self.update)
        self.setIcon(0,QIcon(':/devices/'+self.device.iconName+'.png'))
    def update(self):        
        self.setToolTip(0,self.device.detailedInformation)
        self.setText(0,str(self.device))
    def addContextMenuActions(self,menu):
        SystemTreeItem.addContextMenuActions(self,menu)
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

class SystemTreeWidget(QTreeWidget):
    experimentSelected = pyqtSignal(object)    
    
    def __init__(self,parent):
        QTreeWidget.__init__(self,parent)
        
        self.devices = SystemTreeItem(self,'Devices')      
        self.experiments = SystemTreeItem(self,'Experiments')      
        self.results = SystemTreeItem(self,'Results') 
        
        DeviceCollection.Instance().changed.connect(self.updateDevices)
        ExperimentCollection.Instance().changed.connect(self.updateExperiments)
        
        self.customContextMenuRequested.connect(self.treeContextMenuRequested)
        self.itemClicked.connect(self.itemSelected)
    
    def treeContextMenuRequested(self,point):
        menu = QMenu()
        self.selectedItems()[0].addContextMenuActions(menu)
        menu.exec_(self.mapToGlobal(point))        
    
    def itemSelected(self,item):
        if item.parent() == self.experiments:
            self.experimentSelected.emit(item.experiment)
    
    def updateDevices(self):
        for device in DeviceCollection.Instance().devices.values():
            self.devices.insertChild(0,(DeviceItem(device)))
        self.devices.setExpanded(True)
    
    #TODO: Refactor with updateDevices
    def updateExperiments(self):
        for experiment in ExperimentCollection.Instance().experiments:
            self.experiments.insertChild(0,ExperimentItem(experiment))
        self.experiments.setExpanded(True)   
        

                        
    
#    
        