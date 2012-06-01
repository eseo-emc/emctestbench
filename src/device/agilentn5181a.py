from rfgenerator import RfGenerator
from device import ScpiDevice
from utility.quantities import Amplitude,Power,Frequency

class AgilentN5181a(RfGenerator,ScpiDevice):
    defaultName = 'Agilent N5181A RF Signal Generator'
    visaIdentificationStartsWith = 'Agilent Technologies, N5181A,' 
    defaultAddress = 'TCPIP0::172.20.1.202::inst0::INSTR'
    documentation = {'Programmers Manual':'http://cp.literature.agilent.com/litweb/pdf/N5180-90005.pdf','SCPI Reference':'http://cp.literature.agilent.com/litweb/pdf/N5180-90004.pdf'}
    
         
    def setWaveform(self,frequency,amplitude):
        '''
        Set the waveform parameters at once
        @param frequency float in Hertz
        @param amplitude Amplitude object
        '''        
        self.setFrequency(frequency)
        self.write(':SOURce:POWer:LEVel:IMMediate:AMPLitude %e dBm' % amplitude.dBm())
    def getOutputEnable(self):
        return float(self.ask('OUTPut?'))
    def getPower(self):
        powerString = self.ask(':SOURce:POWer:LEVel:IMMediate:AMPLitude?')
        return Power(float(powerString),'dBm')*self.getOutputEnable() 
    def setFrequency(self,frequency):
        self.write(':SOURce:FREQuency:CW %e Hz' % (frequency.asUnit('Hz')))
    def getFrequency(self):
        return Frequency(float(self.ask(':SOURce:FREQuency:CW?')),'Hz')
    def setPower(self,power):
        setPowerString = ':SOURce:POWer:LEVel:IMMediate:AMPLitude {power:e} dBm'.format(power=power.dBm())
#        print setPowerString
        self.write(setPowerString)
    def enableOutput(self,enable=True):
        if enable:
            self.write('OUTPut ON')
        else:
            self.write('OUTPut OFF')
    def tearDown(self):
        self.enableOutput(False)

if __name__ == '__main__':
    device = AgilentN5181a()
    print device.getFrequency()
#    device.setPower(Power(21,'dBm'))
#    print device.getPower()
    
#    device.enableOutput(False)
#    device.setWaveform(800e6,Amplitude(-25,'dBm'))
    
    