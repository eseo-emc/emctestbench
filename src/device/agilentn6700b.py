from device import ScpiDevice
from powersupply import PowerSupply
import time

class AgilentN6700b(PowerSupply,ScpiDevice):
    defaultName = 'Agilent N6700B Power Supply'
    defaultAddress = 'TCPIP0::192.168.18.183::inst0::INSTR'
    visaIdentificationStartsWith = 'Agilent Technologies,N6700B,'
    documentation = {'Programmers Manual':'http://cp.literature.agilent.com/litweb/pdf/N6700-90902.pdf'}
            
    def setChannelParameters(self,channel,voltage,current):
        self.write('VOLT %f,(@%d); CURRENT %f,(@%d)' % (voltage,channel,current,channel))
    def turnChannelOn(self,channel):
        self.write('OUTP ON,(@%d)' % channel)
    def turnChannelOff(self,channel):
        self.write('OUTP OFF,(@%d)' % channel)
        
         

if __name__ == '__main__':
    powerSupply = AgilentN6700b()
    powerSupply.setChannelParameters(1,1.5,.1)
    powerSupply.turnChannelOn(1)
    time.sleep(1)
    powerSupply.turnChannelOff(1)

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
    
    
    