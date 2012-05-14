from PyQt4.QtGui import QStandardItemModel,QStandardItem,QIcon

from device import knownDevices
import logging
from experimentcollection import ExperimentCollection
from devicecollection import DeviceCollection
from experimentresultcollection import ExperimentResultCollection

class ApplicationWindowModel(object):
    def __init__(self):     
        ExperimentCollection.Instance().discover()
        DeviceCollection.Instance().discover()
        ExperimentResultCollection.Instance().refresh()
                
    def tryToConnectDevices(self):
        for deviceItemNumber in [0]: #range(self.devices.rowCount()):
            device = self.devices.child(deviceItemNumber).device
            logging.LogItem('Refreshing ' + str(device),logging.info)
            try:
                device.tryConnect()
            except Exception, errorDetail:
                logging.LogItem(str(errorDetail),logging.error)
    def treeContextMenuRequested(self,point):
        print 'customContextMenuRequested'
        index = self.systemTreeModel.indexAt(point)
        print index
        print index.isValid()
                
if __name__ == '__main__':
#    def statusMethod(message):
#        print message
#    model = ApplicationWindowModel(statusMethod)
#    model.tryToConnectDevices()
    
    knownDevices[1].tryConnect()
    print knownDevices[1]
    knownDevices[1].drawAttention()