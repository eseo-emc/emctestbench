from device import knownDevices
from utility.quantities import Power,Frequency,PowerRatio,Position
from experiment import Experiment,Property,ScalarProperty
from result import persistance
import numpy
from copy import copy

from calibration.bridge import bridgeInsertionTransferAt,bridgeCouplingFactorAt

from result.resultset import DictResult

class ReceivedPower(Experiment,persistance.Dommable):
    name = 'Received Power'
    
    def __init__(self):
        Experiment.__init__(self)
        self.span = ScalarProperty(Frequency(100,'kHz'),changedSignal=self.settingsChanged,minimum=Frequency(1,'Hz'))
        self.numberOfAveragingPoints = Property(100,changedSignal=self.settingsChanged)
    
    def connect(self):
        self.rfGenerator = knownDevices['rfGenerator']
        self.spectrumAnalyzer = knownDevices['spectrumAnalyzer0']

    def prepare(self):
        self.spectrumAnalyzer.reset()
        self.spectrumAnalyzer.resolutionBandwidth = Frequency(3,'kHz')
        self.spectrumAnalyzer.videoBandwidth = Frequency(10,'kHz')
#        self.spectrumAnalyzer.attenuation = PowerRatio(20,'dB')
#        self.spectrumAnalyzer.referenceLevel = PowerRatio(0,'dB')
        

    def measure(self):
        result = DictResult()
        frequency = self.rfGenerator.getFrequency()

        self.spectrumAnalyzer.span = self.span.value 
        self.spectrumAnalyzer.numberOfAveragingPoints = self.numberOfAveragingPoints.value
    
        result.data = {'received power':self.spectrumAnalyzer.powerAt(frequency)}
        self.emitResult(result)
        return result
            
    def run(self):
        self.measure()            
            
   
        
    
if __name__ == '__main__':
    experiment = ReceivedPower()
    experiment.connect()
    experiment.prepare()
    knownDevices['positioner'].prepare()
    knownDevices['switchPlatform'].setPreset('bridge')
#    print experiment.tryTransmittedPower(Power(0,'dBm'))

#    experiment.rfGenerator.setFrequency(Frequency(150000.))
#    experiment.rfGenerator.setPower(Power(8.2,'dBm'))
#    experiment.rfGenerator.enableOutput()
    
    print experiment.measure().data
