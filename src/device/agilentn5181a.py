from rfgenerator import RfGenerator
from device import ScpiDevice
from utility.quantities import *

class AgilentN5181a(RfGenerator,ScpiDevice):
    defaultName = 'Agilent N5181A RF Signal Generator'
    visaIdentificationStartsWith = 'Agilent Technologies, N5181A,' 
    
         
    def setWaveform(self,frequency,amplitude):
        '''
        Set the waveform parameters at once
        @param frequency float in Hertz
        @param amplitude Amplitude object
        '''        
        self.deviceHandle.write(':SOURce:FREQuency:CW %e Hz' % (frequency))
        self.deviceHandle.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude %e dBm' % amplitude.dBm())
        
    def enableOutput(self,enable=True):
        if enable:
            self.deviceHandle.write('OUTPut ON')
        else:
            self.deviceHandle.write('OUTPut OFF')

if __name__ == '__main__':
    device = AgilentN5181a()
    assert device.tryConnect()
    device.enableOutput(False)
    device.setWaveform(800e6,Amplitude(-25,'dBm'))
    
    