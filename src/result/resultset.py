from datetime import datetime
from PyQt4.QtCore import pyqtSignal,QObject
import numpy


from persistance import Dommable,Dict
from timestamp import TimeStamp
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
        
class DictResult(Dict,Result):
    def __init__(self):
        Result.__init__(self)
        Dict.__init__(self)
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
        self._fields.update({'timeStamp':TimeStamp})
        for fieldName in self._fields.keys():
            self._data[fieldName] = []
    def __eq__(self,other):
        print 'Self ',self._data
        print 'Other', other._data
        return self._data == other._data
    @classmethod
    def fromDom(cls,dom):
        fields = {}
        data = {}
        numberOfRows = None
        for elementId,indexableObject in cls.childObjectById(dom,'Data').items():
            items = []
            for item in indexableObject:
                items.append(item)
            if numberOfRows:
                assert len(items) == numberOfRows,'Not all elements of ResultSet have the same number of items'
            else:
                numberOfRows = len(items)
            fields.update({elementId:type(items[0])})
            data.update({elementId:items})
        assert 'timeStamp' in fields.keys()
        
        newResultSet = super(ResultSet,cls).__new__(cls)
        ResultSet.__init__(newResultSet,fields)
        newResultSet._data = data
        return newResultSet
              
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        consolidatedDict = Dict()
        for key in self._fields.keys():
            consolidatedDict.update({key:self[key]})
        self.appendChildObject(element,consolidatedDict,'Data')
        return element
            
    def append(self,values):
        values.update({'timeStamp':TimeStamp()})
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
        
        if fieldType == TimeStamp:
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