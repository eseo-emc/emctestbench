import numpy

from device import ScpiDevice
from spectrumanalyzer import SpectrumAnalyzer
from utility.quantities import *

class AgilentN9010a(SpectrumAnalyzer,ScpiDevice):
    defaultName = 'Agilent N9010A Vector Signal Analyzer'
    defaultAddress = 'TCPIP0::172.20.1.209::inst0::INSTR'
    visaIdentificationStartsWith = 'Agilent Technologies,N9010A,'
    documentation = {'Programmers Manual':'http://cp.literature.agilent.com/litweb/pdf/N9060-90027.pdf','Specifications':'http://cp.literature.agilent.com/litweb/pdf/N9010-90025.pdf'}
    
    def reset(self):
        self.write(':CAL:AUTO OFF')        
        
    def restore(self):
        self.write(':CAL:AUTO ON') 
    
    def align(self):
        
        self.write(':CAL') 
    def waitUntilReady(self):
        oldTimeOut = self._deviceHandle.timeout
        self._deviceHandle.timeout = 60.0
        self.ask('*OPC?')  
        self._deviceHandle.timeout = oldTimeOut
        
        
    def averageComplexVoltage(self):
#         iqInterlacedValues = self.deviceHandle.ask_for_values(':MEASure:WAVeform0?')

#         self.write(':CONFIGURE:SPEC')
#         iqInterlacedValues = self.deviceHandle.ask_for_values(':READ:SPEC0?')
        iqInterlacedValues = self.ask_for_values(':FETCh:SPEC3?')
        iValues = iqInterlacedValues[0::2]
        qValues = iqInterlacedValues[1::2]
        complexValues = numpy.array(iValues) + numpy.array(qValues)*1j
        
        #     from matplotlib import pyplot
        #     pyplot.plot(iValues,'b.-')
        #     pyplot.plot(qValues,'r.-')
        #     pyplot.show()
        
        return numpy.average(complexValues)
    
if __name__ == '__main__':
    analyzer = AgilentN9010a()
    analyzer.reset()
    
    analyzer.align()
    analyzer.waitUntilReady()
    averageVoltage = analyzer.averageComplexVoltage()
    amplitude = Amplitude(abs(averageVoltage),'Vp')
    print 'Average power %0.2f dBm, %0.1f degrees' % (amplitude.dBm(),numpy.angle(averageVoltage,deg=True))
        
    #calculate power in dBm and phase in degrees...
    
    