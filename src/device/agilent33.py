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
        self.deviceHandle.write('APPL:%s %e HZ, %e VPP, %e V' %
                                (waveType,frequency,peakAmplitude*2,offset))
    def enableOutput(self,enable=True):
        if enable:
            self.deviceHandle.write('OUTPut ON')
        else:
            self.deviceHandle.write('OUTPut OFF')

if __name__ == '__main__':
    device = Agilent33()
    assert device.tryConnect()
    device.enableOutput(False)
    device.setWaveform(25e6, 2.5, 1)
    device.setWaveform(25e6, 2.5, 2.5,'SQU')
    
    