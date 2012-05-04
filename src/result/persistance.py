from xml.dom.minidom import Element

#from utility.quantities import Power,UnitLess

class Dommable:
    def asDom(self,parent):
        element = parent.ownerDocument.createElement(self.__class__.__name__)
        parent.appendChild(element)
        return element
    @classmethod
    def fromDom(cls,dom):
        raise NotImplementedError
    @classmethod
    def castToDommable(cls,anything):
        if isinstance(anything,Dommable):
            return anything
        elif type(anything) == float:
            from utility.quantities import UnitLess
            return UnitLess(anything)
        elif type(anything) == str:
            casted = String(anything)
            return casted
        
        
        
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
        return str.__new__(cls,cls.getNodeText(dom))
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        self.appendTextNode(element,self)
        return element