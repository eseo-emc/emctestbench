from xml.dom.minidom import Element,getDOMImplementation

import string
#from utility.quantities import Power,UnitLess
from datetime import datetime
import numpy

class Dommable(object):
    def asDom(self,parent):
        return self.appendChildTag(parent,self.__class__.__name__)
        
    @classmethod
    def fromDom(cls,dom):
        raise NotImplementedError
    @classmethod
    def castToDommable(cls,anything):
        if hasattr(anything,'asDom'):
            return anything
        elif type(anything) == list:
            return List(anything)
        elif isinstance(anything,bool) or ( isinstance(anything,numpy.ndarray) and anything.dtype.kind == 'b' ):
            from utility.quantities import Boolean
            return Boolean(anything)
        elif type(anything) == datetime:
            from timestamp import Timestamp
            return Timestamp(anything)
        elif isinstance(anything,float) or ( isinstance(anything,numpy.ndarray) and anything.dtype.kind == 'f' ):
            from utility.quantities import UnitLess
            return UnitLess(anything)
        elif isinstance(anything,int) or ( isinstance(anything,numpy.ndarray) and anything.dtype.kind == 'i' ):
            from utility.quantities import Integer
            return Integer(anything)
        elif type(anything) == str:
            casted = String(anything)
            return casted
        elif ( isinstance(anything,numpy.ndarray) and anything.dtype.kind == 'S' ):
            from utility.quantities import StringArray
            return StringArray(anything)
        else:
            print type(anything),anything,isinstance(anything,numpy.ndarray),anything.dtype.kind
            raise ValueError,'Not castable to Dommable'
        
    def appendChildTag(self,parent,tagName):
        element = parent.ownerDocument.createElement(tagName)
        parent.appendChild(element)
        return element
        
    @classmethod
    def appendTextNode(cls,element,text):
        node = element.ownerDocument.createTextNode(text)
        element.appendChild(node)
    @classmethod
    def appendChildObject(cls,parent,childObject,childId):
        element = cls.castToDommable(childObject).asDom(parent)
        element.setAttribute('id',childId)
        return element
    @classmethod
    def getNodeText(cls,element,strip=True):
        childNodes = element.childNodes
        if len(childNodes) >= 1:
            if strip:
                return string.strip(childNodes[0].data)
            else:
                return childNodes[0].data
        else:
            return ''
    @classmethod
    def childElements(cls,parent):
        for node in parent.childNodes:
            if isinstance(node,Element):
                yield node
    @classmethod
    def childObjects(cls,parent,byId=False):
        for element in cls.childElements(parent):
            if byId:
                yield (str(element.getAttribute('id')),cls.objectFromElement(element))
            else:
                yield cls.objectFromElement(element)
    @classmethod
    def childElementById(cls,parent,theId):
        foundElement = None
        for element in cls.childElements(parent):
            if element.getAttribute('id') == theId:
                assert not foundElement,'Multiple elements with the same id found'
                foundElement = element  
        assert foundElement is not None,'Id not found'
        return foundElement
    @classmethod
    def childObjectById(cls,parent,theId):
        return cls.objectFromElement(cls.childElementById(parent,theId))
                
#    @classmethod
#    def childObjectsByName(cls,parent):
#        return cls.childObjects(parent,byId=True)
    @classmethod
    def objectFromElement(cls,element):
        if element.tagName == 'Power':
            from utility.quantities import Power
            factory = Power
        elif element.tagName == 'PowerRatio':
            from utility.quantities import PowerRatio
            factory = PowerRatio
        elif element.tagName == 'Voltage':
            from utility.quantities import Voltage
            factory = Voltage
        elif element.tagName == 'DpiResult':
            from experiment.dpi import DpiResult
            factory = DpiResult
        elif element.tagName == 'FrequencySweepResult':
            from experiment.frequencysweep import FrequencySweepResult
            factory = FrequencySweepResult
        elif element.tagName == 'NearFieldScanResult':
            from experiment.nearfieldscan import NearFieldScanResult
            factory = NearFieldScanResult
        elif element.tagName == 'UnitLess':
            from utility.quantities import UnitLess
            factory = UnitLess
        elif element.tagName == 'Integer':
            from utility.quantities import Integer
            factory = Integer
        elif element.tagName == 'Dict':
            factory = Dict
        elif element.tagName == 'DictResult':
            from result.resultset import DictResult
            factory = DictResult
        elif element.tagName == 'String':
            factory = String
        elif element.tagName == 'StringArray':
            from utility.quantities import StringArray
            factory = StringArray
        elif element.tagName == 'List':
            factory = List
        elif element.tagName == 'Timestamp':
            from result.timestamp import Timestamp
            factory = Timestamp
        elif element.tagName == 'Frequency':
            from utility.quantities import Frequency
            factory = Frequency
        elif element.tagName == 'Position':
            from utility.quantities import Position
            factory = Position
        elif element.tagName == 'Boolean':
            from utility.quantities import Boolean
            factory = Boolean
        elif element.tagName == 'SweepRange':
            from experiment.experiment import SweepRange
            factory = SweepRange
        else:
            raise ValueError("Tag name {tagName} unknown.".format(tagName=element.tagName))
            
        return factory.fromDom(element)
        
    def toXml(self):
        document = getDOMImplementation().createDocument(None,'EmcTestbench',None)
        self.asDom(document.documentElement)
        return document.toprettyxml(encoding='utf-8')
        

        
        
class List(Dommable,list):
    @classmethod
    def fromDom(cls,dom):
        newList = list.__new__(cls)
        for item in cls.childObjects(dom):
            newList.append(item)
        return newList
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        for item in self:
            self.castToDommable(item).asDom(element)
        return element

#TODO: make this subclass dict, to be coherent and efficient
# currently gives baseclass layout conflict...        
class Dict(Dommable):
    def __init__(self,data ={}):
        Dommable.__init__(self)
        self._data = data
    @classmethod
    def fromDom(cls,dom):
        newDictResult = cls()
        newData = {}
        for name,childObject in cls.childObjects(dom,byId=True):
            newData.update({name:childObject})
        newDictResult.data = newData
        return newDictResult
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        for name,value in self.data.items():
            self.appendChildObject(element,value,name)
            
        return element
        
    def __getitem__(self,key):
        return self._data[key]
    def __setitem__(self,key,value):
        self._data[key] = value
        
    @property
    def data(self):
        return self._data
    @data.setter
    def data(self,value):
        self._data = value
    def update(self,values):
        self._data.update(values)
    def values(self):
        return self._data.values()
    def items(self):
        return self._data.items()
    def iteritems(self):
        return self._data.iteritems()
    def keys(self):
        return self._data.keys()
    def has_key(self,fieldName):
        return self._data.has_key(fieldName)
        
    def append(self,values):
        self.update()

class String(Dommable,str):
    @classmethod
    def fromDom(cls,dom):
        return str.__new__(cls,cls.getNodeText(dom))
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        self.appendTextNode(element,self)
        return element

if __name__ == '__main__':
    testDict = Dict({'name':'Mohamed','age':27})
    print testDict['name']
    print testDict.keys()
    print testDict.toXml()