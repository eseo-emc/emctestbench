from device import knownDevices
from utility.quantities import PowerRatio,Frequency


from numpy import pi,sqrt,sin
import numpy
import pylab


from calibration.bridge import bridgeInsertionTransferAt,bridgeCouplingFactorAt,calibrationFrequencies

from gui.experimentresultcollection import ExperimentResultCollection
calibrationMeasurements = ExperimentResultCollection.Instance().loadExperimentResultFiles('Calibration/Bench/')

class BenchCorrectionsSet(object):
    def __init__(self,amplifier):
        self.amplifier = amplifier
    def corrections(self):
        return NotImplementedError
    def name(self):
        return self.__class__.__name__
    def frequencies(self):
        return calibrationFrequencies
    def plotCorrection(self):
        pylab.title(self.amplifier)
        frequencies = self.frequencies()
        corrections = self.corrections(frequencies)
        pylab.plot(frequencies,corrections[0].asUnit('dB'),label=self.name()+' forward')
        pylab.plot(frequencies,corrections[1].asUnit('dB'),label=self.name()+' reflected')

    

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
    def __init__(self,*args,**kwargs):
        super(MeasuredBenchCorrections,self).__init__(*args,**kwargs)
        
        self._outputMeasurement = calibrationMeasurements[self.amplifier+' output'].result
        self._openReflectMeasurement = calibrationMeasurements[self.amplifier+' open reflect'].result

    def forwardCorrection(self,frequency):
        return PowerRatio(numpy.interp(frequency,
                                       self._outputMeasurement['frequency'],
                                       self._outputMeasurement['reflected power image']/self._outputMeasurement['generator power'] ))
    def corrections(self,frequency):
        forwardCorrection = self.forwardCorrection(frequency)
        
        forwardPowers = self._openReflectMeasurement['generator power']*self.forwardCorrection(self._openReflectMeasurement['frequency'])
        reflectedCorrectionMeasurement = forwardPowers/self._openReflectMeasurement['reflected power image']
        reflectedCorrection = reflectedCorrectionMeasurement
        return (forwardCorrection,reflectedCorrection)
        
    def frequencies(self):
        return self._outputMeasurement['frequency']

if __name__ == '__main__':
    compositeCorrections = CompositeBenchCorrections('None (86205A)')
    analyticCorrections = AnalyticBenchCorrections('None (86205A)')
    measuredCorrections = MeasuredBenchCorrections('None (86205A)')
    for corrections in [compositeCorrections,analyticCorrections,measuredCorrections]:
        corrections.plotCorrection()
    
    pylab.legend()
    pylab.xlabel('Frequency (Hz)')
    pylab.ylabel('Correction (dB)')
    pylab.show()

    from gui.experimentresultcollection import ExperimentResultCollection
    calibrationMeasurements = ExperimentResultCollection.Instance().loadExperimentResultFiles('Calibration/Bench/')
    
    