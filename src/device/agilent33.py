from generator import Generator
from device import ScpiDevice

class Agilent33(Generator,ScpiDevice):
    defaultName = 'Agilent 33* waveform generator'
    visaIdentificationStartsWith = 'Agilent Technologies,33'
        
    def setWaveform(self,frequency,peakAmplitude,offset,waveType='SIN'):
        '''
        Set the waveform parameters at once
        @param waveType string one of 'SIN','SQU','PULS','RAMP','NOIS','DC','USER'
        @param frequency float in Hertz
        @param peakAmplitude in Vp (beware! not in Vpp)
        @param offset in V
        '''        
        self.write('APPL:%s %e HZ, %e VPP, %e V' %
                                (waveType,frequency,peakAmplitude*2,offset))
    def enableOutput(self,enable=True):
        if enable:
            self.write('OUTPut ON')
        else:
            self.write('OUTPut OFF')

class Agilent33220A(Agilent33):
    defaultName = 'Agilent 33220A waveform generator'
    defaultAddress = 'TCPIP0::172.20.1.204::inst0::INSTR'
    visaIdentificationStartsWith = 'Agilent Technologies,33220A'
    def displayText(self,message):
        self.write('SYSTem:RWLock')
        super(Agilent33220A,self).displayText(message)
        
class Agilent33250A(Agilent33):
    defaultName = 'Agilent 33250A waveform generator'
    defaultAddress = 'GPIB1::10::INSTR'
    visaIdentificationStartsWith = 'Agilent Technologies,33250A'

if __name__ == '__main__':
    device = Agilent33250A()
    assert device.tryConnect()
#    device.enableOutput(False)
#    device.setWaveform(25e6, 2.5, 1)
#    device.setWaveform(25e6, 2.5, 2.5,'SQU')
    device.deviceHandle.write()
    
    