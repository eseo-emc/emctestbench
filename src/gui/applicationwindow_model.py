from PyQt4.QtGui import QStandardItemModel,QStandardItem,QIcon
from device import knownDevices

class DeviceItem(QStandardItem):
    def __init__(self,device):
        QStandardItem.__init__(self)
        self.setText(str(device))
        self.setData(device)
        self.setToolTip(device.detailedInformation)
        self.setIcon(QIcon('icons/'+device.iconName+'.png'))
    @property
    def device(self):
        return self.data().toPyObject()


class ApplicationWindowModel(object):
    def __init__(self,statusMethod):
        self.statusMethod = statusMethod
        
        self.systemTreeModel = QStandardItemModel()
        self.devices = QStandardItem('Devices')
        self.systemTreeModel.appendRow(self.devices)        
        self.experiments = QStandardItem('Experiments')
        self.systemTreeModel.appendRow(self.experiments)
        self.results = QStandardItem('Results')
        self.systemTreeModel.appendRow(self.results)
        
        for device in knownDevices:
            self.devices.appendRow(DeviceItem(device))

    def refresh(self):
        self.tryToConnectDevices()
        
    def tryToConnectDevices(self):
        for deviceItemNumber in range(self.devices.rowCount()):
            device = self.devices.child(deviceItemNumber).device
            self.statusMethod('Refreshing ' + str(device))
            try:
                device.tryConnect()
            except Exception, errorDetail:
                self.statusMethod(str(errorDetail))
                
if __name__ == '__main__':
    def statusMethod(message):
        print message
    model = ApplicationWindowModel(statusMethod)
    model.tryToConnectDevices()
    
#    DeviceItem(knownDevices[0])