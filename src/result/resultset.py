from datetime import datetime
from PyQt4.QtCore import pyqtSignal,QObject
import numpy

class ResultSet(QObject):
    changed = pyqtSignal()
    added = pyqtSignal(dict)    
    
    def __init__(self,fields):
        QObject.__init__(self)
        self.creationMoment = datetime.now()     
        self._data = {}
        self._fields = fields
        self._fields.update({'timeStamp':datetime})
        for fieldName in self._fields.keys():
            self._data[fieldName] = []
    def append(self,values):
        values.update({'timeStamp':datetime.now()})
        for fieldName in self._fields.keys():
            fieldValue = None
            if values.has_key(fieldName):
                fieldValue = values[fieldName]
            self._data[fieldName].append(fieldValue)
            
        self.added.emit(self.row(-1))
        self.changed.emit()
    def __getitem__(self,key):
        fieldType = self._fields[key]
        
        if fieldType == str:
            missingValue = ''
        else:
            missingValue = numpy.NaN        
        for number,item in enumerate(self._data[key]):
            if item == None:           
                self._data[key][number] = missingValue
        
        if fieldType == datetime:
            return self._data[key]
        elif isinstance(fieldType(0),numpy.ndarray):
            return fieldType(self._data[key])
        else:
            return numpy.array(self._data[key],dtype=fieldType)
    def byRow(self):
        for rowNumber in range(len(self._data.values()[0])):
            yield self.row(rowNumber)
    def row(self,rowNumber):
        newRow = {}            
        for fieldName in self._fields.keys():
            newRow.update({fieldName:self[fieldName][rowNumber]})
        return newRow
    
if __name__ == '__main__':
    import nose
    nose.run(argv=['-v'])