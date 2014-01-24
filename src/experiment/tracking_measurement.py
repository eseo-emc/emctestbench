from device import knownDevices
import pylab
import numpy
from PyQt4.QtCore import pyqtSignal



from utility import quantities
from experiment import Experiment

class TrackingMeasurement(Experiment):
    dataChanged = pyqtSignal()    
    
    def __init__(self,frequencyRange):
        super(Experiment,self).__init__()        
        
        self.generator = knownDevices['rfGenerator']
        self.wattMeter = knownDevices['wattMeter']

        
        if type(frequencyRange) == type(None):
            frequencyRange = numpy.linspace(10e6,6e9,11)
            
        self.frequencies = quantities.Frequency(frequencyRange,'Hz')
        self.generatorPower = quantities.Power(+15,'dBm')
        
        self.powerA = quantities.Power([0]*len(self.frequencies))
        self.powerB = quantities.Power([1]*len(self.frequencies))
        self.referencePowerA = quantities.Power([-numpy.inf]*len(self.frequencies))
        self.referencePowerB = quantities.Power([-numpy.inf]*len(self.frequencies))

    def connect(self):
        self.generator.putOnline()
        self.wattMeter.putOnline()

    def measure(self):
        self.generator.setPower(self.generatorPower)
        for (sampleNumber,frequency) in enumerate(self.frequencies):
            self.generator.setFrequency(frequency)
            (aSample,bSample) = self.wattMeter.getPower()
            self.powerA[sampleNumber] = aSample
            self.powerB[sampleNumber] = bSample
            
#            if self.referencePowerA[sampleNumber] == numpy.NaN:
#                self.referencePowerA[sampleNumber] = aSample
            if self.referencePowerB[sampleNumber] == quantities.Power(-numpy.inf):
                self.referencePowerB[sampleNumber] = bSample
                
            self.currentFrequency = frequency
            self.dataChanged.emit()
            
    
