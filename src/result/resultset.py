from datetime import datetime
from PyQt4.QtCore import pyqtSignal,QObject
import numpy


from persistance import Dommable
from utility.quantities import UnitLess


class Result(QObject):
    changed = pyqtSignal()    
    changedTo = pyqtSignal(object)
    
    def __init__(self):
        QObject.__init__(self)
    
    @classmethod
    def fromDom(self,dom):
        raise NotImplementedError
    def _emitChanged(self):
        self.changedTo.emit(self)
        self.changed.emit()

    def __eq__(self,other):
        return self._data == other._data


       
class ScalarResult(Result,Dommable):
    def __init__(self):
        Result.__init__(self)
        self._data = None
    @classmethod
    def fromDom(cls,dom):
        newScalarResult = cls()
        newScalarResult.data = cls.childObjects(dom).next()
        return newScalarResult
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        self.castToDommable(self.data).asDom(element)
        return element

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self,value):
        self._data = value
        self._emitChanged()
        
class DictResult(Result,Dommable):
    def __init__(self):
        Result.__init__(self)
        self._data = {}
    @classmethod
    def fromDom(cls,dom):
        newDictResult = cls()
        newData = {}
        for name,childObject in cls.childObjectsByName(dom):
            newData.update({name:childObject})
        newDictResult.data = newData
        return newDictResult
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        for name,value in self.data.items():
            print name,type(value)
            item = self.castToDommable(value).asDom(element) 
            item.setAttribute('name',name)  
        return element
        
        
    def __getitem__(self,key):
        return self._data[key]
    @property
    def data(self):
        return self._data
    @data.setter
    def data(self,value):
        self._data = value
        self._emitChanged()
    def append(self,values):
        self._data.update(values)
        self._emitChanged()  
        


        
class ResultSet(Result,Dommable):
    extendedWidth = pyqtSignal(dict)    
    
    def __init__(self,fields):
        Result.__init__(self)
        self.creationMoment = datetime.now()     
        self._data = {}
        self._fields = fields
        self._fields.update({'timeStamp':datetime})
        for fieldName in self._fields.keys():
            self._data[fieldName] = []
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        for fieldName,data in self._data.items():
            dataElement = self.castToDommable(data).asDom(element)
            dataElement.setAttribute('name',fieldName)
            break
        return element
            
    def append(self,values):
        values.update({'timeStamp':datetime.now()})
        for fieldName in self._fields.keys():
            fieldValue = None
            if values.has_key(fieldName):
                fieldValue = values[fieldName]
            self._data[fieldName].append(fieldValue)
            
        self.extendedWidth.emit(self.row(-1))
        self._emitChanged()
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
#    result = ScalarResult()
#    result.data = 3.0
#    
#    from xml.dom.minidom import getDOMImplementation
#    document = getDOMImplementation().createDocument(None,'EmcTestbench',None)
#    
#    element = document.createElement('Result')    
#    document.documentElement.appendChild(element)
#    
#    element.setAttribute('name','Sjoerd')    
#    
#    node = element.ownerDocument.createTextNode('425.5')
#    element.appendChild(node)
#    xml = document.toprettyxml()
#    print xml
#    
#    ###
#    from xml.dom.minidom import parseString
#    document = parseString(xml)
#    resultElement = document.documentElement.getElementsByTagName('Result')[0]
#    print resultElement.getAttribute('name')
#    print float(resultElement.childNodes[0].data)+1
#    
    
    import nose
    nose.run(argv=['-v'])