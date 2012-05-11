from datetime import datetime
import string
from persistance import Dommable

class TimeStamp(Dommable): #TODO make a subclass of the (immutable) datetime to improve performance
    def __init__(self,data =None):
        if data == None:
            data = datetime.now()
        self.data = data
    def __eq__(self,other):
        if hasattr(other,'data'):
            return self.data == other.data
        else:
            return False
    def strftime(self,formatString):
        return self.data.strftime(formatString)
    
    @classmethod
    def fromDom(cls,dom):
#        return datetime.__new__(cls,datetime.strptime(string.strip(cls.getNodeText(dom)),'%Y-%m-%dT%H:%M:%S.%f'))
        newInstance = Dommable.__new__(cls)
        newInstance.__init__(datetime.strptime(string.strip(cls.getNodeText(dom)),'%Y-%m-%dT%H:%M:%S.%f'))
        return newInstance
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        self.appendTextNode(element,self.data.strftime('%Y-%m-%dT%H:%M:%S.%f'))
        return element

