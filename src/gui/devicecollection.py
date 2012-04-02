from utility import Singleton
from PyQt4.QtCore import QObject,pyqtSignal
from device import knownDevices,Device

import logging
import inspect

@Singleton
class DeviceCollection(QObject):
    changed = pyqtSignal()    
    
    def __init__(self):
        QObject.__init__(self)
        self.devices = {}   
    def __getitem__(self,key):
        return self[key]
    def discover(self):
        self.devices = knownDevices   
        self.changed.emit()
    def refresh(self):
        for device in self.devices.values():
            device.putOnline()
        
if __name__ == '__main__':
    DeviceCollection.Instance().discover()