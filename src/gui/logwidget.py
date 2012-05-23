from PyQt4.QtGui import QTableWidget,QTableWidgetItem,QHeaderView,QIcon
from PyQt4.QtCore import QObject
import logging


class StdOutLogView(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.logModel = logging.LogModel.Instance()
        self.logModel.itemAdded.connect(self.update)
    def update(self,item):
        print str(item)

class LogWidget(QTableWidget):
    def __init__(self,parent):
        QTableWidget.__init__(self,parent)
        self.logModel = logging.LogModel.Instance()
        self.logModel.itemAdded.connect(self.update)      
        self.maximumLevel = logging.warning
    def setLevel(self,level):
        self.maximumLevel = level
        self.update()
    def update(self):
        self.setHorizontalHeaderLabels(['Kind','Timestamp','Message'])
        self.setColumnWidth(0,30)
        self.setColumnWidth(1,60)
        self.verticalHeader().setResizeMode(QHeaderView.ResizeToContents)
        
        self.clearContents()
        itemNumber = 0
        for logItem in self.logModel.logItems:
            if logItem.level <= self.maximumLevel:
#                if self.rowCount <= itemNumber:
                self.insertRow(itemNumber)
                
                levelItem = QTableWidgetItem(logging.logLevels[logItem.level])
                levelItem.setIcon(QIcon(':/logging/'+logging.logLevels[logItem.level]))
                self.setItem(itemNumber,0,levelItem)
                self.setItem(itemNumber,1,QTableWidgetItem(logItem.timeStamp.strftime('%H:%m:%S')))
                self.setItem(itemNumber,2,QTableWidgetItem(logItem.message))
                
                itemNumber += 1
        self.setRowCount(itemNumber)
        