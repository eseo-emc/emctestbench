'''
@author: Sjoerd Op 't Land
'''

from math import log10,pow,sqrt

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
        

class Power():
    def __init__(self,value,unit):
        if unit == 'W':
            self._power = float(value)
        elif unit == 'dBm':
            self._power = pow(10.,float(value)/10) * 1e-3
        elif unit == 'dBW':
            self._power = pow(10.,float(value)/10) * 1
        else:
            raise ValueError, '''Power unit '%s' not recognised.''' % unit
    
    def watt(self):
        return self._power
        
    def dBW(self):
        return 10.0*log10(self._power)
        
    def dBm(self):
        return self.dBW()+30.0
    
    def __str__(self):
        return '%.2e W' % self.watt()
            
                        
if __name__ == '__main__':
    print 'Testing amplitude...'
    
    test = Amplitude(10,'dBW')
    print test
    print test.dBW()
    
    test = Amplitude(0,'dBm')
    print test
    print test.dBm()