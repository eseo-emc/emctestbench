from datetime import datetime
from utility import Singleton
from PyQt4.QtCore import QObject,pyqtSignal

success = -1
error = 0
warning = 1
info = 2
debug = 3
logLevels = {-1:'Success',0:'Error',1:'Warning',2:'Info',3:'Debug'}

#_logModelInstance = LogModel.Instance()

@Singleton
class LogModel(QObject):
    itemAdded = pyqtSignal(object)    
    def __init__(self):
        QObject.__init__(self)
        self.logItems = []
        self.maximumLevel = 3
        self.gui = True
    def appendLogItem(self,item):
        self.logItems.append(item)
        if self.gui:
            self.itemAdded.emit(item)
        else:
            print str(item)
                
class LogItem(object):
    def __init__(self,message,level=3):
        self.timeStamp = datetime.now()
        self.message = message
        self.level = level    
        LogModel.Instance().appendLogItem(self)
    def __str__(self):
        #TODO: below formatting is a view issue and should, as such, be moved to a View module
        # It is not done yet, because the emit()-connect() mechanism doesn't seem to work outside of the GUI
        return '{level:8s} {message}'.format(level=logLevels[self.level]+':',message=self.message)
        
