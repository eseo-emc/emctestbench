import numpy

from device import ScpiDevice
from spectrumanalyzer import SpectrumAnalyzer
from utility import quantities

import time
import subprocess
import skrf

class AgilentN9010a(SpectrumAnalyzer,ScpiDevice):
    defaultName = 'Agilent N9010A Vector Signal Analyzer'
    defaultAddress = 'TCPIP0::192.168.10.30::inst0::INSTR'
    visaIdentificationStartsWith = 'Agilent Technologies,N9010A,'
    documentation = {'Programmers Manual':'http://cp.literature.agilent.com/litweb/pdf/N9060-90027.pdf','Specifications':'http://cp.literature.agilent.com/litweb/pdf/N9010-90025.pdf'}
    
    def putOnline(self):
#        try:
        ScpiDevice.putOnline(self)
#        except: 
#            subprocess.call(['C:\Program Files\Agilent\SignalAnalysis\Infrastructure\LaunchXSA.exe','-s'])
#            time.sleep(90)
#            ScpiDevice.putOnline(self)
#            assert self._deviceHandle is not None
            
    def reset(self):
        ScpiDevice.reset(self)
        
        self.write(':CONFigure:SANalyzer')
#        self.write(':INITiate:CONTinuous ON')
        self.write(':CAL:AUTO OFF')        
        
    def restore(self):
        self.write(':CAL:AUTO ON') 
#        self.write(':INITiate:CONTinuous ON')
    
    def align(self):
        self.write(':CAL') 
        

    
    @property
    def span(self):
        return quantities.Frequency(float(self.ask(':SENS:FREQ:SPAN?')),'Hz')
    @span.setter
    def span(self,value):
        self.write(':SENS:FREQ:SPAN {span:e}HZ'.format(span=value.asUnit('Hz')))

    @property
    def numberOfPoints(self):   
        return int(self.ask(':SENSe:SWEep:POINts?'))
    @numberOfPoints.setter
    def numberOfPoints(self,value):
        self.write(':SENSe:SWEep:POINts {value:d}'.format(value=value))
    
    @property
    def frequency(self):
        return skrf.Frequency.from_f(self.frequencies, unit='Hz')
    @property
    def frequencies(self):
        return numpy.linspace(self.centerFrequency-self.span/2.0,
                              self.centerFrequency+self.span/2.0,
                              self.numberOfPoints)
    
    @property
    def resolutionBandwidth(self):
        return quantities.Frequency(float(self.ask(':SENS:BAND:RES?')),'Hz')
    @resolutionBandwidth.setter
    def resolutionBandwidth(self,value):
        self.write(':SENS:BAND:RES:AUTO OFF')
        self.write(':SENS:BAND:RES {bandwidth:e}HZ'.format(bandwidth=value.asUnit('Hz')))
            
    @property
    def videoBandwidth(self):
        return quantities.Frequency(float(self.ask(':SENS:BAND:VID?')),'Hz')
    @videoBandwidth.setter
    def videoBandwidth(self,value):
        self.write(':SENS:BAND:VID:AUTO OFF')
        self.write(':SENS:BAND:VID {bandwidth:e}HZ'.format(bandwidth=value.asUnit('Hz')))

    @property
    def centerFrequency(self):
        return quantities.Frequency(float(self.ask(':SENS:FREQ:CENT?')),'Hz')
    @centerFrequency.setter
    def centerFrequency(self,value):
        self.write(':SENS:FREQ:CENT {frequency:e}HZ'.format(frequency=value.asUnit('Hz')))

    @property
    def attenuation(self):
        return quantities.PowerRatio(float(self.ask(':SENS:POW:RF:ATT?')),'dB')
    @attenuation.setter
    def attenuation(self,value):
        self.write(':SENS:POW:RF:ATT {attenuation:.2f}dB'.format(attenuation=value.asUnit('dB')))
    
    @property
    def referenceLevel(self):
        return quantities.PowerRatio(float(self.ask(':DISP:WIND:TRAC:Y:SCAL:RLEV?')),'dB')
    @referenceLevel.setter
    def referenceLevel(self,value):
        self.write(':DISP:WIND:TRAC:Y:SCAL:RLEV {level:.2f}'.format(level=value.asUnit('dB')))

    @property
    def numberOfAveragingPoints(self):
        return int(self.ask(':SENSe:AVERage:COUNt?'))
    @numberOfAveragingPoints.setter
    def numberOfAveragingPoints(self,value):
        self.write(':TRACe1:TYPE AVERage') #was MAXHold
        self.write(':SENSe:AVERage:TYPE RMS') #LOG is default
        self.write(':SENSe:AVERage:COUNt {points:d}'.format(points=value))

    def powerAt(self,frequency):
        self.centerFrequency = frequency
#        self.write(':INITiate:CONTinuous OFF')
        self.write(':INIT:RESTart')
        self.write(':CALCulate:MARKer1:MAXimum')
        self.write(':CALCulate:MARKer1:CPSearch ON')

        self.waitUntilReady()
        measuredValues = self.ask(':FETCH:SANalyzer0?').split(',')
        assert int(float(measuredValues[0])) == 0, 'margin or limit failure'
#        print '#points taken',int(float(measuredValues[5]))
        return quantities.Power(float(measuredValues[10]),'dBm')
    
    
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
    
    def measure(self):
        self.write('INIT:IMMediate')
#        print 'wait for done'
        self.waitUntilReady()
#        print 'Reading values'
        return numpy.array(self.ask_for_values('TRAC:DATA? TRACE1'))
    
if __name__ == '__main__':
    from utility.quantities import Frequency,PowerRatio   
    
    analyzer = AgilentN9010a()
    analyzer.reset()
    
    analyzer.span = Frequency(100,'MHz')
#    analyzer.resolutionBandwidth = Frequency(3,'kHz')
#    analyzer.videoBandwidth = Frequency(10,'kHz')
    analyzer.centerFrequency = Frequency(50,'MHz')
#    analyzer.attenuation = PowerRatio(20,'dB')
#    analyzer.referenceLevel = PowerRatio(0,'dB')
    analyzer.numberOfAveragingPoints = 100
    
    print 'Span',analyzer.span
    print 'RBW',analyzer.resolutionBandwidth
    print 'VBW',analyzer.videoBandwidth
    print 'CF',analyzer.centerFrequency
    print 'attenuation',analyzer.attenuation
    print 'ref',analyzer.referenceLevel
    print '#avg',analyzer.numberOfAveragingPoints
    
#    print analyzer.powerAt(Frequency(80,'MHz'))
#    print '#avg',analyzer.numberOfAveragingPoints
#    analyzer.reset()
#    
#    analyzer.align()
#    analyzer.waitUntilReady()
#    averageVoltage = analyzer.averageComplexVoltage()
#    amplitude = Amplitude(abs(averageVoltage),'Vp')
#    print 'Average power %0.2f dBm, %0.1f degrees' % (amplitude.dBm(),numpy.angle(averageVoltage,deg=True))
        
    #calculate power in dBm and phase in degrees...
    
    