from datetime import datetime
from utility import Singleton
from PyQt4.QtCore import QObject,pyqtSignal

success = -1
error = 0
warning = 1
info = 2
debug = 3
logLevels = {-1:'Success',0:'Error',1:'Warning',2:'Info',3:'Debug'}

@Singleton
class LogModel(QObject):
    itemAdded = pyqtSignal()    
    def __init__(self,maximumLevel=3):
        QObject.__init__(self)
        self.logItems = []
        self.maximumLevel = maximumLevel
    def appendLogItem(self,item):
        self.logItems.append(item)
        self.itemAdded.emit()
        
class LogItem(object):
    def __init__(self,message,level=3):
        self.timeStamp = datetime.now()
        self.message = message
        self.level = level    
        LogModel.Instance().appendLogItem(self)