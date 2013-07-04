from math import log10,pow,sqrt
from numpy import inf,nan
import numpy
from result.persistance import Dommable
import string

#siPrefices = ['y','z','a','f','p','n','u','m','','k','M','G','T','P','E','Z','Y']
#siUnitIndex = 8
siPrefices = ['n','u','m','','k','M','G']
siUnitIndex = 3

class Amplitude():
    '''
    Represents a voltage amplitude. When set using power quantities, a characteristic impedance of 50 Ohm is assumed.
    '''
    z0 = 50.0 # characteristic impedance
            
    def __init__(self,value,unit):
        if unit == 'Vp':
            self._amplitude = float(value)
        elif unit == 'Vpp':
            self._amplitude = float(value)/2.0
        else:
            try:
                power = Power(value,unit)
            except ValueError as strerror:
                raise ValueError, 'Amplitude unit not recognised, tried to interpret as power unit, but ... %s' % strerror
            self._amplitude = sqrt(2.0) * sqrt(power.watt()*Amplitude.z0)
            
            
    def Vp(self):
        return self._amplitude
    
    def Vpp(self):
        return 2*self._amplitude
        
    def __getattr__(self,name):
        power = Power(pow(self._amplitude,2.0) / 2.0 / Amplitude.z0,'W')
        return getattr(power,name)
        
    def __str__(self):
        return '%.2e Vp' % self.Vp()
       


class DommableArray(numpy.ndarray,Dommable):
    def __new__(cls, value):
        #http://docs.scipy.org/doc/numpy/user/basics.subclassing.html  
        newObject = numpy.asarray(value).view(cls)
        return newObject
    def __deepcopy__(self,memo):
        return type(self)(self)
    def __getitem__(self,itemNumber):
        singleItem = numpy.ndarray.__getitem__(self,itemNumber)
        return self.__class__(singleItem)
#    def __array_finalize__(self, obj):
#        if obj is None: return
#        self.info = getattr(obj, 'info', None)  
    def __eq__(self,other):
        if type(other) == type(None):
            return False
        else:
            return numpy.asarray(self) == numpy.asarray(other)
#        equality = numpy.ndarray.__eq__(self,other)
#        if isinstance(equality,numpy.ndarray):
#            return equality.all()
#        else:
#            return equality      
    def append(self,value):
        assert type(value) == type(self)
        return self.__class__(numpy.append(self,value))
        
    @classmethod
    def fromDom(cls,dom):
        return eval('cls('+cls.getNodeText(dom)+')')
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        self.appendTextNode(element,self.toArrayString(separator=',\n'))
        return element
        
    def __repr__(self):
        return self.__class__.__name__+'('+self.toArrayString()+")"

    @classmethod
    def _safeFormat(cls, value):
        return str(numpy.asarray(value))
    
    def __str__(self):
        return self.toArrayString(formatFunction=self._safeFormat)
#        return self.toArrayString(separator=' ')

    def toArrayString(self,formatFunction=None,separator=', '):
        #TODO: remove formatFunction and use self._safeFormat
        if not formatFunction:
            formatFunction = lambda value : str(numpy.asarray(value))
        def toString(theArray):
            if theArray.shape == ():
                return formatFunction(theArray)
            else:
                returnList = []
                for item in theArray:
                    returnList.append(toString(item))
                return '[' + separator.join(returnList) + ']'
        return toString(self)


class UnitLess(DommableArray):
    pass
class Integer(DommableArray):
    pass

class Boolean(DommableArray):
    pass

def reasonableExponent(number):
    if number == 0.:
        return 0
    else:
        return numpy.int(numpy.floor(numpy.log10(abs(number))/3.)*3)
def exponentToPrefix(exponent):
    return siPrefices[exponent/3+siUnitIndex]
def prefixToExponent(prefix):
    return (siPrefices.index(prefix)-siUnitIndex)*3

#def siMultiplierAndUnit(jointUnit,unit=''):
#    prefix = jointUnit[0]
#    unit = jointUnit[1:]
#    multiplier = 10**(index)
#    (siPrefices.index('m')-8)*3

class DommableDimensionalArray(DommableArray):
    storageUnit = None
    proportionWithPower = None
    
    def __new__(cls,value,unit=None):
        value = numpy.asarray(value) * 1.0
        if unit == None:
            unit = cls.storageUnit
        if unit.startswith('dB'):
            value = numpy.power(10.,value/(10.*cls.proportionWithPower))
            unit = unit[2:]
        value *= 10**cls._getExponent(unit)
        
        return DommableArray.__new__(cls,value)
    @classmethod
    def _getExponent(cls,jointUnit):
        assert jointUnit.endswith(cls.storageUnit),'Requested {jointUnit} does not end with {storageUnit}'.format(jointUnit=jointUnit,storageUnit=cls.storageUnit)
        return prefixToExponent(jointUnit[:len(jointUnit)-1*len(cls.storageUnit)])
    def asUnit(self,jointUnit):
        if jointUnit.startswith('dB'):
            dB = True
            jointUnit = jointUnit[2:]
        else:
            dB = False
        linearResult = numpy.asarray(self)/(10**self._getExponent(jointUnit))
        if dB:
            return self.proportionWithPower * 10. *numpy.log10(linearResult)
        else:
            return linearResult
    def preferredUnit(self):
        return exponentToPrefix(reasonableExponent(self.min())) + self.storageUnit
        
    #TODO: refactor to units with an ISO prefix, perhaps a list of enumerator/denominator unit, analytical math to simplify unit?
    @classmethod
    def fromDom(cls,dom):
        return eval('cls('+cls.getNodeText(dom)+',"'+dom.getAttribute('unit')+'")')
    def asDom(self,parent):
        element = DommableArray.asDom(self,parent)
        element.setAttribute('unit',self.storageUnit)
        return element
    
    def __repr__(self):
        return self.__class__.__name__+'('+self.toArrayString()+",'"+self.storageUnit+"')"    
    @classmethod
    def _safeFormat(cls, value):
        if numpy.isnan(value):
            return 'NaN'
        else:
            return str(value.asUnit(value.preferredUnit())) + ' ' + value.preferredUnit()


class Voltage(DommableDimensionalArray):
    storageUnit = 'V'    

class Frequency(DommableDimensionalArray):
    storageUnit = 'Hz'
    
    def Hz(self):
        return self.asUnit('Hz')
        
class Position(DommableDimensionalArray):
    storageUnit = 'm'
    
class Power(DommableArray):
    storageUnit = 'W'
        
    def __new__(cls, value, unit=None, info=None):
        value = numpy.asarray(value) * 1.0 #force values to be floats
        
        if unit == None:
            unit = cls.storageUnit
        if unit == 'W':
            pass
        elif unit == 'dBm':
            value = numpy.power(10.,value*0.1) * 1e-3            
        elif unit == 'dBW':
            value = numpy.power(10.,value*0.1) * 1
        else:
            raise ValueError, '''Power unit '%s' not recognised.''' % unit
        
        return DommableArray.__new__(cls,value)
#        newObject = numpy.asarray(value).view(cls)
#        newObject.info = info
#        return newObject
        
    @classmethod
    def fromDom(cls,dom):
        return eval('cls('+cls.getNodeText(dom)+',"'+dom.getAttribute('unit')+'")')
    def asDom(self,parent):
        element = DommableArray.asDom(self,parent)
        element.setAttribute('unit',self.storageUnit)
        return element
    
    @property
    def negligible(self):
        return self < 1e-16 # -130 dBm
     
    def watt(self):
        return numpy.asarray(self) 
    def dBW(self):
        invalid = (lambda linearValue: numpy.NaN)
        infinite = (lambda linearValue: -numpy.inf)
        decibel = (lambda linearValue: 10.0*numpy.log10(linearValue))
        return numpy.piecewise(self,[self < 0.,self == 0.],[invalid,infinite,decibel])
#        def dBWElement(value):
#            if value < 0.:
#                return numpy.NaN
#            elif self == 0.:
#                return -numpy.inf
#            else:
#                return 10.0*log10(self)
#        numpy.apply_along_axis()
    def dBm(self):
        return self.dBW()+30.0
    def asUnit(self,unit=None):
        if not unit:
            unit = self.storageUnit
        if unit == 'W':
            return self.watt()
        elif unit == 'dBm':
            return self.dBm()
        elif unit == 'dBW':
            return self.dBW()
            
    def min(self,maximumPower):
        return Power(min(self.watt(),maximumPower.watt()),'W')
    def max(self,minimumPower):
        return Power(max(self.watt(),minimumPower.watt()),'W')
        
    def __mul__(self,other):
#        assert type(other) == float or type(other) == PowerRatio
        return Power(self.watt()*numpy.array(other),'W')
    def __div__(self,other):
        if type(other) == numpy.array or type(other) == PowerRatio:
            return Power(self.watt()/numpy.array(other),'W')
        elif type(other) == Power:
            return PowerRatio(self.watt()/numpy.array(other))
    def __sub__(self,other):
        assert type(other) == Power
        return Power(self.watt()-other.watt(),'W')
    def __add__(self,other):
        assert type(other) == Power
        return Power(self.watt()+other.watt(),'W')        
#    def __eq__(self,other): 
#        if type(other) == type(self):
#            return DommableArray.__eq__(self,other.watt())
#        else:
#            return DommableArray.__eq__(self,other)

    def __repr__(self):
        return self.__class__.__name__+'('+self.toArrayString()+",'"+self.storageUnit+"')"

    @classmethod
    def _safeFormat(cls,value):
        if numpy.isnan(value):
            return 'NaN'
        if value >= 0:
            dBmValue = value.dBm()
            prefix = ''
        else:
            dBmValue = (-1*value).dBm()
            prefix = '<-- '
        if dBmValue == -numpy.inf:
            return prefix+'-inf dBm'
        else:
            return prefix+'{dBm:+.1f} dBm'.format(dBm=dBmValue)
    
    def toArrayString(self,formatFunction=None,separator=', '):
        if not formatFunction:
            formatFunction = lambda value : str(value.asUnit())
        return DommableArray.toArrayString(self,formatFunction=formatFunction,separator=separator)

class PowerRatio(DommableDimensionalArray):
    storageUnit = ''
    proportionWithPower = 1
    
    def linear(self):
        return self.asUnit()
    def preferredUnit(self):
        return 'dB'
        
    
 
                        
if __name__ == '__main__':
#    import numpy
#    a = Frequency([1,2 ],'GHz')
#    b= Frequency([1,0],'GHz')
#    print a == b
#    print repr(Power([[0.001,0.002],[2.,1.]]))
#    print repr(Power([2.,1.]))
#    print repr(Power(2.))
#
#    print 'Testing Power...'
#    a = Power([],'dBm')
#    b = Power(numpy.append(a,Power(3,'dBm')))
#    c = a.append(Power(3,'dBm'))
#    c = Power(6,'dBW')
#    print c
#    
#    import copy
#    d = copy.deepcopy(c)
#    print d
    
#    print Power([[1,2],[.001,.002]]).toArrayString()
#    assert abs((test-test*PowerRatio(-3,'dB')).dBm() - -3.0) < 0.1
#    assert str(test) == '+0.0 dBm'
#    assert str(test*2.0) == '+3.0 dBm'
#    
#    test = PowerRatio(20,'dB')
#    print test.asUnit('dB')
#    print test
#    assert abs(test.linear()-0.5) < 0.1
#    
#    test = Power(30,'dBm')+Power(30,'dBm')
#    assert abs(test.dBW() - 3.0) < 0.1
#    
#    
#    test = Amplitude(10,'dBW')
#    print test
#    print test.dBW()
#    
#    test = Amplitude(0,'dBm')
#    print test.watt()
#    print test

    f = Frequency([1,2,nan],'Hz')
    print f
    p = Power([1,2,nan],'W')
    print p
    print repr(p)