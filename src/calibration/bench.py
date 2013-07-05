from device import knownDevices
from utility.quantities import PowerRatio,Frequency
from utility.smoothing import smoothBoxcar
from gui import log

from numpy import pi,sqrt,sin
import numpy
import pylab


from calibration.bridge import bridgeInsertionTransferAt,bridgeCouplingFactorAt,calibrationFrequencies
from gui.experimentresultcollection import ExperimentResultCollection


class BenchCorrectionsSet(object):
    def __init__(self,amplifier):
        self.amplifier = amplifier
    def corrections(self,frequency):
        return NotImplementedError
    def name(self):
        return self.__class__.__name__
    def _frequencies(self):
        return numpy.linspace(0,20e9,1000)
    def plotCorrection(self):
        pylab.title(self.amplifier)
        frequencies = self._frequencies()
        corrections = self.corrections(frequencies)
        pylab.plot(frequencies,corrections[0].asUnit('dB'),label=self.name()+' forward')
        pylab.plot(frequencies,corrections[1].asUnit('dB'),label=self.name()+' reflected')    

class BestBenchCorrections(BenchCorrectionsSet):
    def __init__(self,*args):
        super(BestBenchCorrections,self).__init__(*args)
        try:
            self._correctionsSet = MeasuredBenchCorrections(self.amplifier)
            
        except KeyError:
            log.LogItem('Did not find "{amplifier} output" and "{amplifier} output reflect" files in /EmcTestbench/Calibration/Bench, reverting to analytical corrections'.format(amplifier=self.amplifier),log.warning)
            self._correctionsSet = AnalyticBenchCorrections(self.amplifier)
        except:
            raise
        
    def corrections(self,frequency):
        return self._correctionsSet.corrections(frequency)
    def _frequencies(self):
        return self._correctionsSet._frequencies()

class AnalyticBenchCorrections(BenchCorrectionsSet):
    def corrections(self,frequency):
        switchAttenuation = PowerRatio(sqrt(frequency/Frequency(170,'GHz')),'dB') # 2 switches - cable - cable - 2 switches
        # in the incident path, these losses cancel (same loss for DUT and incident power meter)
        # in the reflected path, these losses appear (the signal suffers from two cables and twice the switch platform)
        if self.amplifier == 'None (86205A)':
            forwardCorrection = 1/PowerRatio(1.5,'dB') + 0*frequency
            reflectedCorrection = switchAttenuation * PowerRatio(16.0 + 0.6*sin(2*pi*frequency/Frequency(12,'GHz')),'dB')
        elif self.amplifier == 'None (773D)':
            # http://cp.literature.agilent.com/litweb/pdf/00772-90001.pdf
            forwardCorrection = 1/PowerRatio(0.9,'dB')+ 0*frequency
            reflectedCorrection = switchAttenuation * PowerRatio(20.0,'dB')+ 0*frequency
        elif self.amplifier == 'Prana':
            forwardCorrection = PowerRatio(48.7 - 0.4*sin(2*pi*frequency/Frequency(1,'GHz')),'dB')
            reflectedCorrection = switchAttenuation * forwardCorrection / PowerRatio(0.1,'dB')            
        elif self.amplifier == 'Milmega 1':
            forwardCorrection = PowerRatio(44.9 - 0.6*sin(2*pi*(frequency-Frequency(900,'MHz'))/Frequency(2,'GHz')),'dB')
            reflectedCorrection = switchAttenuation * forwardCorrection * PowerRatio(0.4,'dB')
        elif self.amplifier == 'Milmega 2':
            forwardCorrection = PowerRatio(43.6 - 0.6*sin(2*pi*(frequency-Frequency(1.9,'GHz'))/Frequency(4,'GHz')),'dB')
            reflectedCorrection = switchAttenuation * PowerRatio(44.4 - 1.1*sin(2*pi*(frequency-Frequency(1.9,'GHz'))/Frequency(4,'GHz')),'dB')
        
        elif self.amplifier.startswith('None'):
            raise ValueError, 'Non-existant bridge specifier'    
        else:
            raise ValueError, 'The switch platform is in an unsupported position.'
        
        return (forwardCorrection,reflectedCorrection)
    

class CompositeBenchCorrections(BenchCorrectionsSet):
    def corrections(self,frequency):
        assert self.amplifier == 'None (86205A)'
        
        forwardCorrection = bridgeInsertionTransferAt(frequency)
        reflectedCorrection = 1 / bridgeCouplingFactorAt(frequency)
        
        return (forwardCorrection,reflectedCorrection)

class MeasuredBenchCorrections(BenchCorrectionsSet):
    smoothingSamples = 1   
    
    def __init__(self,*args,**kwargs):
        super(MeasuredBenchCorrections,self).__init__(*args,**kwargs)
        
        calibrationMeasurements = ExperimentResultCollection.Instance().loadExperimentResultFiles('Calibration/Bench/'+self.amplifier)
        self._outputMeasurement = calibrationMeasurements[self.amplifier+' output'].result
        self._openReflectMeasurement = calibrationMeasurements[self.amplifier+' open reflect'].result

    def _smoothRatio(self,frequency,measuredFrequency,measuredCorrection):
        smoothedCorrection = smoothBoxcar(measuredCorrection,self.smoothingSamples)
        return PowerRatio(numpy.interp(frequency,measuredFrequency,smoothedCorrection ))
    def _forwardCorrection(self,frequency):
        measuredCorrection = self._outputMeasurement['reflected power image']/self._outputMeasurement['generator power']
        return self._smoothRatio(frequency,self._outputMeasurement['frequency'],measuredCorrection)
    def _reflectedCorrection(self,frequency):
        openReflectFrequency = self._openReflectMeasurement['frequency']
        forwardPowers = self._openReflectMeasurement['generator power']*self._forwardCorrection(openReflectFrequency)
        reflectedCorrectionMeasurement = forwardPowers/self._openReflectMeasurement['reflected power image']
        return self._smoothRatio(frequency,openReflectFrequency,reflectedCorrectionMeasurement)

    def corrections(self,frequency):          
        return (self._forwardCorrection(frequency),self._reflectedCorrection(frequency))
        
    def _frequencies(self):
        return self._outputMeasurement['frequency']

if __name__ == '__main__':
    def plotCorrections(amplifier):
        try:
            CompositeBenchCorrections(amplifier).plotCorrection()
        except:
            pass
        AnalyticBenchCorrections(amplifier).plotCorrection()
        MeasuredBenchCorrections(amplifier).plotCorrection()

        
        pylab.legend()
        pylab.xlabel('Frequency (Hz)')
        pylab.ylabel('Correction (dB)')
        pylab.show()

    plotCorrections('None (86205A)')    
    plotCorrections('None (773D)')