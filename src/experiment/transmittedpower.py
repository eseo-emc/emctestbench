from device import knownDevices
from utility.quantities import Power,Frequency
from experiment import Experiment,EnumerateProperty
from result import persistance
from copy import copy


from calibration.bench import BestBenchCorrections

from result.resultset import DictResult

class TransmittedPower(Experiment,persistance.Dommable):
    name = 'Transmitted Power Calculation'
    
    def __init__(self):
        Experiment.__init__(self)
        persistance.Dommable.__init__(self)
        
        self.amplifiers = {'None (86205A)':'bridge 86205A', 'None (773D)':'bridge 773D', 'Prana':'Prana', 'Milmega 1':'Milmega', 'Milmega 2':'Milmega'}
        self.amplifier = EnumerateProperty('None (86205A)',['Automatic'] + self.amplifiers.keys())
        self.amplifier.changed.connect(self.setAmplifier)

        self.amplifierCorrections = {}        
        for amplifier in self.amplifiers.keys():
            self.amplifierCorrections.update({amplifier:BestBenchCorrections(amplifier)})
    
    def connect(self):
        self.switchPlatform = knownDevices['switchPlatform']
        self.setAmplifier()
        self.wattMeter = knownDevices['wattMeter']
        self.rfGenerator = knownDevices['rfGenerator']

    def prepare(self):
        self.wattMeter.reset()
    
    @property
    def generatorFrequency(self):
        return self.rfGenerator.getFrequency()
    @generatorFrequency.setter
    def generatorFrequency(self,value):
        self.rfGenerator.setFrequency(value)
    
    @property
    def generatorPower(self):        
        return self.rfGenerator.getPower()
    @generatorPower.setter
    def generatorPower(self,newPower):
        self.rfGenerator.setPower(newPower)
        if not self.amplifier.value.startswith('None'):
            if newPower.negligible:
                knownDevices[self.amplifiers[self.amplifier.value]].turnRfOff()
            else:
                knownDevices[self.amplifiers[self.amplifier.value]].turnRfOn()
    
    def setAmplifier(self):
#        if not self.generatorPower.negligible:
#            print "Trying to change amplifier while outputting RF... need to implement turn off, change, turn on sequence"
#            raise NotImplementedError
        if self.amplifier.value == 'Automatic':
            raise ValueError, 'Automatic amplifier selection is not yet supported'
        else:
            self.switchPlatform.setPreset(self.amplifiers[self.amplifier.value])
            if self.amplifier.value == 'Milmega 1':
                knownDevices[self.amplifiers[self.amplifier.value]].switchToBand1()
            elif self.amplifier.value == 'Milmega 2':
                knownDevices[self.amplifiers[self.amplifier.value]].switchToBand2()
            
            
    def measure(self):
        assert self.switchPlatform.checkPreset(self.amplifiers[self.amplifier.value]),'The switch platform is not in the {position} position'.format(position=self.amplifier.value)

        result = DictResult()  
        generatorPower = self.rfGenerator.getPower()
        frequency = self.rfGenerator.getFrequency()        
          
        (forwardPowerReadout,reflectedPowerReadout) = self.wattMeter.getPower()
        
        reflectedImage = reflectedPowerReadout        
        if self.amplifier.value.startswith('None'):
            forwardImage = generatorPower
        else:
            forwardImage = forwardPowerReadout

        (forwardCorrection,reflectedCorrection) = self.amplifierCorrections[self.amplifier.value].corrections(frequency)                
            
        forwardPower = forwardImage * forwardCorrection
        reflectedPower = reflectedImage * reflectedCorrection

        result.data = {'generator power':generatorPower,
                       'forward power image':forwardImage,
                       'reflected power image':reflectedPowerReadout,
                       'forward power':forwardPower,
                       'reflected power':reflectedPower,
                       'transmitted power':forwardPower-reflectedPower,
                       'reflection coefficient':reflectedPower/forwardPower}
        self.emitResult(result)
        return result
        

    def run(self):
        self.measure()  
    def tearDown(self):
        self.generatorPower = Power(0)    
        
            
    def tryTransmittedPower(self,nominalPower):
        generatorMaximum = Power(20,'dBm')
        tryForwardPower = copy(nominalPower)
        for tryNumber in range(4):
#            print tryForwardPower
            self.rfGenerator.setPower(tryForwardPower)
            self.rfGenerator.enableOutput()
            realTransmittedPower = self.measure()['transmitted power']
            realTransmittedPower = realTransmittedPower.max(Power(-40,'dBm'))

            gain = nominalPower/realTransmittedPower

            tryForwardPower *= gain
            tryForwardPower = tryForwardPower.min(generatorMaximum)

        return self.measure()['transmitted power']

        
    
if __name__ == '__main__':
    experiment = TransmittedPower()
    experiment.connect()
    experiment.prepare()
#    experiment.switchPlatform.setPreset('bridge')
#    print experiment.tryTransmittedPower(Power(0,'dBm'))
    experiment.amplifier.setValue('None (86205A)')
    experiment.generatorFrequency = Frequency(150000,'Hz')
    experiment.generatorPower = Power(-60,'dBm')
#    experiment.rfGenerator.enableOutput()
    
    print experiment.measure()
