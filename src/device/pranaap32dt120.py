from device import ScpiDevice
from amplifier import Amplifier
import time

class PranaAP32DT120(Amplifier,ScpiDevice):
    defaultName = 'Prana AP32 DT120 Power Amplifier'
    visaIdentificationStartsWith = 'AP32 DT120'
    def askIdentity(self):
        return self.deviceHandle.ask('*ID?')
        
    def turnRfOn(self):
        self.deviceHandle.write('MHF')
    def turnRfOff(self):
        self.deviceHandle.write('AHF')
        
  
if __name__ == '__main__':
    amplifier = PranaAP32DT120()
    assert amplifier.tryConnect()
    
    amplifier.turnRfOn()
    time.sleep(5)
    amplifier.turnRfOff()

#     
#     ampli prana 5
#     * ID
#     MHF # on
#     AHF # off
#     
#     ampli milmega 6
#     OUT4 1 # LINE ON
#     OUT4 0 # LINE OFF
#     OUT1 1 # RF ON
#     OUT1 0 # RF OFF
#     OUT3 0 # Band 1
#     OUT3 1 # Band 2
#     
#     frequency meter 206
#     
#     multimeter 207
#     
#     dso 208
    
    
    