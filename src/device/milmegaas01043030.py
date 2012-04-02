from device import ScpiDevice
from amplifier import Amplifier
import time

class MilmegaAS0104_30_30(Amplifier,ScpiDevice):
    defaultName = 'Milmega AS0104 30/30'
    defaultAddress = 'GPIB1::6::INSTR'
    visaIdentificationStartsWith = '"MILMEGA,RF AMPLIFIER,'
           
    def turnRfOn(self):
        self.write('OUT1 1')
    def turnRfOff(self):
        self.write('OUT1 0')
    
    def turnLineOn(self):
        self.write('OUT4 1')
    def turnLineOff(self):
        self.write('OUT4 0')
        
    def switchToBand1(self):
        self.write('OUT3 0')
    def switchToBand2(self):
        self.write('OUT3 1')    

if __name__ == '__main__':
    amplifier = MilmegaAS0104_30_30()
    print amplifier.iconName
    amplifier.turnLineOn()
    time.sleep(1)
    amplifier.turnRfOn()
    time.sleep(5)
    amplifier.turnRfOff()
    time.sleep(1)
    amplifier.switchToBand2()
    time.sleep(1)
    amplifier.switchToBand1()
    time.sleep(5)
    amplifier.turnLineOff()


#     
#     frequency meter 206
#     
#     multimeter 207
#     
#     dso 208
    
    
    