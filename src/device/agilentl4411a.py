import numpy

from device import ScpiDevice
from utility import quantities
from multimeter import Multimeter

class AgilentL4411a(Multimeter,ScpiDevice):
    defaultName = 'Agilent L4411A Multimeter'
    defaultAddress = 'TCPIP0::192.168.18.187::inst0::INSTR'
    visaIdentificationStartsWith = 'Agilent Technologies,L4411A,'
    documentation = {'Users Manual':'http://cp.literature.agilent.com/litweb/pdf/34410-90001.pdf','Programming Reference':'http://www.home.agilent.com/upload/cmc_upload/All/34410A_Prog_Reference.exe'}
    
          
    def measure(self):
        self.write('CONF:VOLT:DC AUTO')
        voltageString = self.ask('MEASure?')
#        voltageString = self.ask('MEASure:VOLTage:DC? 100E-3,1E-8')
        return quantities.Voltage(float(voltageString),'V')
    
if __name__ == '__main__':
    device = AgilentL4411a()

    print 'Average voltage %0.2e V' % (device.measure())
 