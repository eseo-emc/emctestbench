from xml.dom.minidom import Element
import string
from datetime import datetime
#from utility.quantities import Power,UnitLess

class Dommable:
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
        elif type(anything) == datetime:
            return DateTime(anything)
        elif type(anything) == float:
            from utility.quantities import UnitLess
            return UnitLess(anything)
        elif type(anything) == str:
            casted = String(anything)
            return casted
        else:
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
    def getNodeText(cls,element):
        return element.childNodes[0].data
    @classmethod
    def childElements(cls,parent):
        for node in parent.childNodes:
            if isinstance(node,Element):
                yield node
    @classmethod
    def childObjects(cls,parent,byName=False):
        for element in cls.childElements(parent):
            if byName:
                yield (str(element.getAttribute('name')),cls.objectFromElement(element))
            else:
                yield cls.objectFromElement(element)
    @classmethod
    def childObjectsByName(cls,parent):
        return cls.childObjects(parent,byName=True)
    @classmethod
    def objectFromElement(cls,element):
        if element.tagName == 'Power':
            from utility.quantities import Power
            factory = Power
        elif element.tagName == 'UnitLess':
            from utility.quantities import UnitLess
            factory = UnitLess
        elif element.tagName == 'String':
            factory = String
        else:
            raise ValueError("Tag name {tagName} unknown.".format(tagName=element.tagName))
            
        return factory.fromDom(element)
        
class String(Dommable,str):
    @classmethod
    def fromDom(cls,dom):
        return str.__new__(cls,string.strip(cls.getNodeText(dom)))
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        self.appendTextNode(element,self)
        return element
        
class DateTime(Dommable,datetime):
    @classmethod
    def fromDom(cls,dom):
        return datetime.__new__(cls,datetime.strptime(string.strip(cls.getNodeText(dom)),'%Y-%m-%dT%H:%M:%S.%f'))
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        self.appendTextNode(element,self.strftime('%Y-%m-%dT%H:%M:%S.%f'))
        return element
        
class List(Dommable,list):
#    @classmethod
#    def fromDom(cls,dom):
#        newList = list.__new__(cls)
#        
#        return datetime.__new__(cls,datetime.strptime(string.strip(cls.getNodeText(dom)),'%Y-%m-%dT%H:%M:%S.%f'))
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        for item in self:
            self.castToDommable(item).asDom(element)
        return element