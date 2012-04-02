from PyQt4.QtGui import QTreeWidget,QTreeWidgetItem,QIcon,QMenu,QAction
from PyQt4.Qt import Qt
from experimentcollection import ExperimentCollection
from devicecollection import DeviceCollection
import logging

class SystemTreeItem(QTreeWidgetItem):    
    def customContextMenuRequested(self,globalPoint):
        menu = QMenu()
        self.contextMenuActions(menu)
        menu.exec_(globalPoint)
    def contextMenuActions(self,menu):
        noneAction = QAction('Refresh all',menu)
#        noneAction.setEnabled(False)
        noneAction.triggered.connect(DeviceCollection.Instance().refresh)
        menu.addAction(noneAction)
        
class ExperimentItem(SystemTreeItem):
    def __init__(self,experiment):
        SystemTreeItem.__init__(self)
        self.setText(0,experiment.name)

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
    def contextMenuActions(self,menu):
        onlineAction = QAction('Put Online',menu)
        onlineAction.triggered.connect(self.device.putOnline)
        menu.addAction(onlineAction)
        attentionAction = QAction('Draw Attention',menu)
        attentionAction.triggered.connect(self.device.drawAttention)
        menu.addAction(attentionAction)

class SystemTreeWidget(QTreeWidget):
    def __init__(self,parent):
        QTreeWidget.__init__(self,parent)

        self.devices = QTreeWidgetItem(['Devices'])
        self.insertTopLevelItem(0,self.devices)
        
        self.experiments = QTreeWidgetItem(['Experiments'])
        self.insertTopLevelItem(1,self.experiments)
        
        self.results = QTreeWidgetItem(['Results']) 
        self.insertTopLevelItem(2,self.results)   
        
        DeviceCollection.Instance().changed.connect(self.updateDevices)
        ExperimentCollection.Instance().changed.connect(self.updateExperiments)
        
        self.customContextMenuRequested.connect(self.treeContextMenuRequested)
    
    def updateDevices(self):
        for device in DeviceCollection.Instance().devices.values():
            self.devices.insertChild(0,(DeviceItem(device)))
        self.devices.setExpanded(True)
    
    #TODO: Refactor
    def updateExperiments(self):
        for experiment in ExperimentCollection.Instance().experiments:
            self.experiments.insertChild(0,ExperimentItem(experiment))
        self.experiments.setExpanded(True)   
        
    def treeContextMenuRequested(self,point):
        self.selectedItems()[0].customContextMenuRequested(self.mapToGlobal(point))
                
    
#    
        