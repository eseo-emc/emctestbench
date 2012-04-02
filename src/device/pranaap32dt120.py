from device import ScpiDevice
from amplifier import Amplifier
import time

class PranaAP32DT120(Amplifier,ScpiDevice):
    defaultName = 'Prana AP32 DT120 Power Amplifier'
    defaultAddress = 'GPIB1::5::INSTR'
    visaIdentificationStartsWith = 'AP32 DT120'
    def askIdentity(self):
        return self.ask('*ID?')
        
    def turnRfOn(self):
        self.write('MHF')
    def turnRfOff(self):
        self.write('AHF')
        
  
if __name__ == '__main__':
    amplifier = PranaAP32DT120()
    print amplifier.askIdentity()
    
    amplifier.turnRfOn()
    time.sleep(5)
    amplifier.turnRfOff()

    