from rfgenerator import RfGenerator
from device import ScpiDevice
from utility.quantities import Amplitude,Power,Frequency

class AgilentN5181a(RfGenerator,ScpiDevice):
    defaultName = 'Agilent N5181A RF Signal Generator'
    visaIdentificationStartsWith = 'Agilent Technologies, N5181A,' 
    defaultAddress = 'TCPIP0::192.168.18.182::inst0::INSTR'
    documentation = {'Programmers Manual':'http://cp.literature.agilent.com/litweb/pdf/N5180-90005.pdf','SCPI Reference':'http://cp.literature.agilent.com/litweb/pdf/N5180-90004.pdf'}
    
         
    def setWaveform(self,frequency,amplitude):     
        self.setFrequency(frequency)
        self.setPower(amplitude)
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
        setPowerString = ':SOURce:POWer:LEVel:IMMediate:AMPLitude {power:e} dBm'.format(power=max(-110.,power.dBm()))
        self.write(setPowerString)

        if power.negligible:
            self._enableOutput(False)
        else:
            self._enableOutput(True)
    
    def _enableOutput(self,enable=True):
        if enable:
            self.write('OUTPut ON')
        else:
            self.write('OUTPut OFF')
            
    def enableLocalControl(self):
        self.write(':SYSTem:COMMunicate:GTLocal')
        
    def tearDown(self):
        RfGenerator.tearDown(self)
        self.enableLocalControl()


if __name__ == '__main__':
    device = AgilentN5181a()
    print device.getFrequency()
    device.setPower(Power(0,'dBm'))
    device.tearDown()
#    print device.getPower()
    
#    device.enableOutput(False)
#    device.setWaveform(800e6,Amplitude(-25,'dBm'))
    
    