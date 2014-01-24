from device import ScpiDevice
from amplifier import Amplifier

class PranaAP32DT120(Amplifier,ScpiDevice):
    defaultName = 'Prana AP32 DT120 Power Amplifier'
    defaultAddress = 'GPIB1::5::INSTR'
    visaIdentificationStartsWith = 'AP32 DT120'

        
    def _turnRfOn(self):
        self.write('MHF')
        self.write('MHF')
        self.write('MHF')
        self.write('MHF')

    def _turnRfOff(self):
        self.write('AHF')
        self.write('AHF')
        self.write('AHF')
        self.write('AHF')
        
  
if __name__ == '__main__':
    amplifier = PranaAP32DT120()
    print amplifier.askIdentity()
    
#    amplifier.turnRfOn()
#    time.sleep(5)
    amplifier.turnRfOff()

    