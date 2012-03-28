'''
@author: Sjoerd Op 't Land
'''

from math import log10,pow,sqrt
from numpy import inf,NaN

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
       
class PowerRatio(float):
    def __new__(cls,value,unit=None):
        if unit == 'dB':
            return float.__new__(PowerRatio,pow(10.,float(value)/10))
        elif unit == None:
            return float.__new__(PowerRatio,float(value))
        else:
            raise ValueError, '''Power ratio unit '{unit}' not recognized.'''.format(unit=unit)
    def linear(self):
        return float(self)
    def dB(self):
        if self < 0.:
            raise NaN
        elif self == 0.:
            return -inf
        else:
            return 10.0*log10(self)
    def __repr__(self):
        return str(self)
    def __str__(self):
        dBValue = self.dB()
        if dBValue == -inf:
            return '-inf dB'
        else:
            return '{dB:+.1f} dB'.format(dB=dBValue)
            

class Power(float):
    def __new__(cls,value,unit):
        if unit == 'W':
            return float.__new__(Power,value)
        elif unit == 'dBm':
            return float.__new__(Power,pow(10.,float(value)/10) * 1e-3)
        elif unit == 'dBW':
            return float.__new__(Power,pow(10.,float(value)/10) * 1)
        else:
            raise ValueError, '''Power unit '%s' not recognised.''' % unit
    
    def watt(self):
        return float(self)
        
    def dBW(self):
        if self < 0.:
            return NaN
        elif self == 0.:
            return -inf
        else:
            return 10.0*log10(self)
        
    def dBm(self):
        return self.dBW()+30.0
    def min(self,maximumPower):
        return Power(min(self.watt(),maximumPower.watt()),'W')
    def max(self,minimumPower):
        return Power(max(self.watt(),minimumPower.watt()),'W')
        
    def __mul__(self,other):
        assert type(other) == float or type(other) == PowerRatio
        return Power(self.watt()*float(other),'W')
    def __div__(self,other):
        if type(other) == float or type(other) == PowerRatio:
            return Power(self.watt()/float(other),'W')
        elif type(other) == Power:
            return PowerRatio(self.watt()/float(other),None)
    def __sub__(self,other):
        assert type(other) == Power
        return Power(self.watt()-other.watt(),'W')
    def __repr__(self):
        return str(self)
    def __str__(self):
#        return '{watt:e} W'.format(watt=self.watt())
        if self >= 0:
            dBmValue = self.dBm()
            prefix = ''
        else:
            dBmValue = (-1*self)
            prefix = '<- '
        if dBmValue == -inf:
            return prefix+'-inf dBm'
        else:
            return prefix+'{dBm:+.1f} dBm'.format(dBm=dBmValue)
    
            
                        
if __name__ == '__main__':
    print 'Testing amplitude...'
    test = Power(0,'dBm')
    print test-test*PowerRatio(-3,'dB')
    print test
    print test*2.0
    
    test = PowerRatio(-3.,'dB')
    print test.linear()
#    test = Amplitude(10,'dBW')
#    print test
#    print test.dBW()
#    
#    test = Amplitude(0,'dBm')
#    print test.watt()
#    print test