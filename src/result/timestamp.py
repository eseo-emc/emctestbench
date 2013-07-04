from datetime import datetime,date,time
import string
from utility.quantities import DommableArray
import numpy

class Timestamp(DommableArray): 
    storageFormatString = '%Y-%m-%dT%H:%M:%S.%f'    
    
    def __new__(cls,value=None):
        if value == None:
            value = datetime.now()
            
        return DommableArray.__new__(cls,value)
            
    def strftime(self,formatString):
        return datetime.strftime(numpy.asscalar(self),formatString)
   
    @classmethod
    def fromDom(cls,dom):
        newInstance = super(Timestamp,cls).fromDom(dom)
        parseTimestampString = lambda dateString : datetime.strptime(dateString,Timestamp.storageFormatString)
        parseTimestampString = numpy.vectorize(parseTimestampString)
        return Timestamp(parseTimestampString(newInstance))
    @classmethod
    def _safeFormat(cls, value):
        return value.strftime("'"+Timestamp.storageFormatString+"'")
    
if __name__ == '__main__':
    a = Timestamp()
    print a
    
    b = Timestamp([datetime.now(),datetime.now()])
    print repr(b)
    
#class Timestamp(Dommable): #TODO make a subclass of the (immutable) datetime to improve performance
#    def __init__(self,data =None):
#        if data == None:
#            data = datetime.now()
#        self.data = data
#    def __eq__(self,other):
#        if hasattr(other,'data'):
#            return self.data == other.data
#        else:
#            return False
#    def toEpoch(self):
#        return 24. * 60. * 60. * self.data.toordinal() + \
#            60. * 60. * self.data.hour + \
#            60. * self.data.minute + \
#            self.data.second + \
#            1e-6 * self.data.microsecond
#    @classmethod
#    def fromEpoch(cls,value):
#        dateOrdinal = int(value // (24*60*60))
#        value %= 24*60*60
#        hour = int(value // (60*60))
#        value %= 60*60
#        minute = int(value // 60)
#        value %= 60
#        second = int(value // 1)
#        value %= 1
#        theDate = date.fromordinal(dateOrdinal)
#        theTime = time(hour,minute,second,int(round(value,3)*1e6))
#        return Timestamp(datetime.combine(theDate,theTime))
#            
#    def strftime(self,formatString):
#        return self.data.strftime(formatString)
#    
#    @classmethod
#    def fromDom(cls,dom):
##        return datetime.__new__(cls,datetime.strptime(string.strip(cls.getNodeText(dom)),'%Y-%m-%dT%H:%M:%S.%f'))
#        newInstance = Dommable.__new__(cls)
#        newInstance.__init__(datetime.strptime(string.strip(cls.getNodeText(dom)),'%Y-%m-%dT%H:%M:%S.%f'))
#        return newInstance
#    def asDom(self,parent):
#        element = Dommable.asDom(self,parent)
#        self.appendTextNode(element,self.data.strftime('%Y-%m-%dT%H:%M:%S.%f'))
#        return element
#
