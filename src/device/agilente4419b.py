import numpy
import time

from utility.quantities import Power
from device import ScpiDevice
from wattmeter import WattMeter

class AgilentE4419b(WattMeter,ScpiDevice):
    defaultName = 'Agilent E4419B Power Meter'
    visaIdentificationStartsWith = 'Agilent Technologies,E4419B,'
    
    def reset(self):
        self.deviceHandle.write('*RST')
        self.deviceHandle.write('CONF1 -50,DEF,(@1)')
        self.deviceHandle.write('SENS1:AVER:COUN 1')
        self.deviceHandle.write('TRIG1:DEL:AUTO OFF')
#         
        # Prepare for downloading waveforms
        #visa.vpp43.gpib_control_ren(self.deviceHandle, visa.VI_GPIB_REN_ASSERT_ADDRESS_LLO)
            
    def getPower(self,channel):
        '''
        Acquire one waveform from a channel.
        @param channel A or B
        
        @return Power instance
        '''
        assert(channel == 'A')
        
        
        self.deviceHandle.write('INIT1')  
        #time.sleep(20)
        dBmPower = float(self.deviceHandle.ask('FETC1?'))
        return Power(dBmPower,'dBm')
        
    
if __name__ == '__main__':
    from matplotlib import pyplot
    import time
    device = AgilentE4419b()
    assert device.tryConnect()
    device.reset()
    
    for iteration in range(10000):
        #time.sleep(1)
        print iteration
#        signal = device.getChannelWaveform(1)
#        signal2 = device.getChannelWaveform(2)
        print device.getPower('A')
        
        
#     pyplot.plot(signal[0,:],signal[1,:],'b.-')
#     pyplot.plot(signal2[0,:],signal2[1,:],'r.-')
#     pyplot.show()



    
    