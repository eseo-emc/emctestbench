import numpy
import time

from utility.quantities import Power
from device import ScpiDevice
from wattmeter import WattMeter

class AgilentE4419b(WattMeter,ScpiDevice):
    defaultAddress = 'GPIB1::13::INSTR'
    defaultName = 'Agilent E4419B Power Meter'
    visaIdentificationStartsWith = 'Agilent Technologies,E4419B,'
    documentation = {'Programmers Manual':'http://cp.literature.agilent.com/litweb/pdf/E4418-90029.pdf'}
    
    def reset(self):
        self.write('*RST')
        def configureChannel(channelNumber):
            self.write('CONF{channel} -50,DEF,(@{channel})'.format(channel=channelNumber))
            self.write('SENS{channel}:AVER:COUN 1'.format(channel=channelNumber))
            self.write('TRIG{channel}:DEL:AUTO OFF'.format(channel=channelNumber))
        configureChannel(1)
        configureChannel(2)
             
    def getPower(self,channelNumber=None):
        if channelNumber==None:
            self._initializeMeasurement(1)
            self._initializeMeasurement(2)
            return (self._fetchMeasurement(1),self._fetchMeasurement(2))
        else:
            self._initializeMeasurement(channelNumber)
            return self._fetchMeasurement(channelNumber)
            
    def _initializeMeasurement(self,channelNumber):
        self.write('INIT{channel}'.format(channel=channelNumber))  
    def _fetchMeasurement(self,channelNumber):
        dBmPower = float(self.ask('FETC{channel}?'.format(channel=channelNumber)))
        return Power(dBmPower,'dBm')
        
    
if __name__ == '__main__':
    from matplotlib import pyplot
    import time
    device = AgilentE4419b()
    assert device.tryConnect()
    device.reset()
    
    for iteration in range(100):
        print iteration
        print device.getPower()



    
    