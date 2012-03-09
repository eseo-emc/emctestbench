import numpy

from device import ScpiDevice
from utility.quantities import *
from multimeter import Multimeter

class AgilentL4411a(Multimeter,ScpiDevice):
    defaultName = 'Agilent L4411A Multimeter'
    visaIdentificationStartsWith = 'Agilent Technologies,L4411A,'
    documentation = {'Users Manual':'http://cp.literature.agilent.com/litweb/pdf/34410-90001.pdf','Programming Reference':'http://www.home.agilent.com/upload/cmc_upload/All/34410A_Prog_Reference.exe'}
    
          
    def voltage(self):
        self.deviceHandle.write('CONF:VOLT:DC AUTO')
        voltageString = self.deviceHandle.ask('MEASure?')
#         voltageString = self.deviceHandle.ask('MEASure:VOLTage:DC?')
        return float(voltageString)
    
if __name__ == '__main__':
    device = AgilentL4411a()
    assert device.tryConnect()

    print 'Average power %0.2e V' % (device.voltage())
 