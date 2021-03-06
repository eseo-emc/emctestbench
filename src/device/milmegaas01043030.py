from device import ScpiDevice
from amplifier import Amplifier
import time

class MilmegaAS0104_30_30(Amplifier,ScpiDevice):
    defaultName = 'Milmega AS0104 30/30'
    defaultAddress = 'GPIB0::6::INSTR'
    visaIdentificationStartsWith = '"MILMEGA,RF AMPLIFIER,'
           
    def _turnRfOn(self):
        self._turnLineOn()
        self.write('OUT1 1')
    def _turnRfOff(self):
        self.write('OUT1 0')
        self._turnLineOff()
    
    def _turnLineOn(self):
        self.write('OUT4 1')
    def _turnLineOff(self):
        self.write('OUT4 0')
        
    def switchToBand1(self):
        self.write('OUT3 0')
    def switchToBand2(self):
        self.write('OUT3 1')    

if __name__ == '__main__':
    amplifier = MilmegaAS0104_30_30()
    print amplifier.iconName
    amplifier.rfOn = True

    time.sleep(1)
    amplifier.switchToBand2()
    time.sleep(1)
    amplifier.switchToBand1()
    
    time.sleep(5)
    amplifier.rfOn = False
 

#     
#     frequency meter 206
#     
#     multimeter 207
#     
#     dso 208
    
    
    