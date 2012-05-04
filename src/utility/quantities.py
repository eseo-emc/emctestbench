from math import log10,pow,sqrt
#from numpy import inf,NaN,ndarray,asarray
import numpy
from result.persistance import Dommable

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
       
#class PowerRatio(float):
#    def __new__(cls,value,unit=None):
#        if unit == 'dB':
#            return float.__new__(PowerRatio,pow(10.,float(value)/10))
#        elif unit == None:
#            return float.__new__(PowerRatio,float(value))
#        else:
#            raise ValueError, '''Power ratio unit '{unit}' not recognized.'''.format(unit=unit)
#    def linear(self):
#        return float(self)
#    def dB(self):
#        if self < 0.:
#            raise numpy.NaN
#        elif self == 0.:
#            return -numpy.inf
#        else:
#            return 10.0*log10(self)
#    def __repr__(self):
#        return str(self)
#    def __str__(self):
#        dBValue = self.dB()
#        if dBValue == -numpy.inf:
#            return '-inf dB'
#        else:
#            return '{dB:+.1f} dB'.format(dB=dBValue)

class PowerRatio(numpy.ndarray):
    #http://docs.scipy.org/doc/numpy/user/basics.subclassing.html  
    def __new__(cls, value, unit='', info=None):
        value = numpy.asarray(value) * 1.0 #force values to be floats

        if unit == '':
            pass         
        elif unit == 'dB':
            value = numpy.power(10.,value*0.1) * 1
        else:
            raise ValueError, '''Power unit '%s' not recognised.''' % unit
        
        newObject = numpy.asarray(value).view(cls)
        newObject.info = info
        return newObject
        
    def __getitem__(self,itemNumber):
        singleItem = numpy.ndarray.__getitem__(self,itemNumber)
        return Power(singleItem)

    def __array_finalize__(self, obj):
        if obj is None: return
        self.info = getattr(obj, 'info', None)
            
    def linear(self):
        return numpy.asarray(self)
        
    def dB(self):
        if self < 0.:
            return numpy.NaN
        elif self == 0.:
            return -numpy.inf
        else:
            return 10.0*log10(self)
        

        
    def __repr__(self):
        return str(self)
        
        
    def __str__(self):
        def toString(theArray):
            if theArray.shape == ():
                #return '{watt:e} W'.format(watt=self.watt())
                if theArray >= 0:
                    dBValue = theArray.dB()
                    prefix = ''
                else:
                    dBValue = (-1*theArray)
                    prefix = '<- '
                if dBValue == -numpy.inf:
                    return prefix+'-inf dB'
                else:
                    return prefix+'{dB:+.1f} dB'.format(dB=dBValue)
            else:
                returnList = []
                for item in theArray:
                    returnList.append(toString(item))
                return '[' + ', '.join(returnList) + ']'
                
        return toString(self)




class UnitLess(float,Dommable):
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        self.appendTextNode(element,str(self))
        return element
    @classmethod
    def fromDom(cls,dom):
        return cls(float(cls.getNodeText(dom)))

class Power(numpy.ndarray,Dommable):
    storageUnit = 'W'
    #http://docs.scipy.org/doc/numpy/user/basics.subclassing.html  
    def __new__(cls, value, unit='W', info=None):
        value = numpy.asarray(value) * 1.0 #force values to be floats

        if unit == 'W':
            pass
        elif unit == 'dBm':
            value = numpy.power(10.,value*0.1) * 1e-3            
        elif unit == 'dBW':
            value = numpy.power(10.,value*0.1) * 1
        else:
            raise ValueError, '''Power unit '%s' not recognised.''' % unit
        
        newObject = numpy.asarray(value).view(cls)
        newObject.info = info
        return newObject
        
    @classmethod
    def fromDom(cls,dom):
        return cls(float(cls.getNodeText(dom)),dom.getAttribute('unit'))
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        element.setAttribute('unit',self.storageUnit)
        self.appendTextNode(element,str(self.asUnit(self.storageUnit)))
        return element
        
    def __getitem__(self,itemNumber):
        singleItem = numpy.ndarray.__getitem__(self,itemNumber)
        return Power(singleItem)

    def __array_finalize__(self, obj):
        if obj is None: return
        self.info = getattr(obj, 'info', None)
        
    def append(self,value):
        assert type(value) == type(self)
        return self.__class__(numpy.append(self,value))
            
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
    def asUnit(self,unit):
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
    def __eq__(self,other):
        if type(other) == type(self):
            print repr(self.watt()) , repr(other.watt())
            return self.watt() == other.watt()
        else:
            return numpy.ndarray.__eq__(self,other)

    def __repr__(self):
        return str(self)
    def __str__(self):
        def toString(theArray):
            if theArray.shape == ():
                #return '{watt:e} W'.format(watt=self.watt())
                if numpy.isnan(theArray):
                    return 'NaN'
                if theArray >= 0:
                    dBmValue = theArray.dBm()
                    prefix = ''
                else:
                    dBmValue = (-1*theArray)
                    prefix = '<- '
                if dBmValue == -numpy.inf:
                    return prefix+'-inf dBm'
                else:
                    return prefix+'{dBm:+.1f} dBm'.format(dBm=dBmValue)
            else:
                returnList = []
                for item in theArray:
                    returnList.append(toString(item))
                return '[' + ', '.join(returnList) + ']'
                
        return toString(self)
#    return numpy.ndarray.__str__(self)


    
                        
if __name__ == '__main__':
    import numpy
    
#    print repr(Power([[0.001,0.002],[2.,1.]]))
#    print repr(Power([2.,1.]))
#    print repr(Power(2.))
#
#    print 'Testing Power...'
    a = Power([],'dBm')
    b = Power(numpy.append(a,Power(3,'dBm')))
    c = a.append(Power(3,'dBm'))
    print repr(c)
#    assert abs((test-test*PowerRatio(-3,'dB')).dBm() - -3.0) < 0.1
#    assert str(test) == '+0.0 dBm'
#    assert str(test*2.0) == '+3.0 dBm'
#    
#    test = PowerRatio(-3.,'dB')
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