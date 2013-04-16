from device import knownDevices
from utility.quantities import Power,PowerRatio,Frequency
from experiment import Experiment,EnumerateProperty
from result import persistance
from numpy import pi,sqrt,sin,NaN
from copy import copy

from calibration.bridge import bridgeInsertionTransferAt,bridgeCouplingFactorAt

from result.resultset import DictResult

class TransmittedPower(Experiment,persistance.Dommable):
    name = 'Transmitted Power Calculation'
    
    def __init__(self):
        Experiment.__init__(self)
        persistance.Dommable.__init__(self)
        
        self.amplifiers = {'None':'bridge', 'Prana':'Prana', 'Milmega 1':'Milmega', 'Milmega 2':'Milmega'}
        self.amplifier = EnumerateProperty('None',['Automatic'] + self.amplifiers.keys())
        self.amplifier.changed.connect(self.setAmplifier)
    
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
        if self.amplifier.value is not 'None':
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
        
        switchAttenuation = PowerRatio(sqrt(frequency/Frequency(170,'GHz')),'dB') # 2 switches - cable - cable - 2 switches
        # in the incident path, these losses cancel (same loss for DUT and incident power meter)
        # in the reflected path, these losses appear (the signal suffers from two cables and twice the switch platform)
           
        if self.amplifier.value == 'None':
            reflectedPowerReadout = self.wattMeter.getPower(2)
            forwardPowerReadout = Power(NaN)
#            forwardPower = generatorPower * bridgeInsertionTransferAt(frequency)
#            reflectedPower = reflectedPowerReadout / bridgeCouplingFactorAt(frequency)
            insertionLoss = PowerRatio(1.5,'dB')
            reflectedAttenuation = PowerRatio(16.0 + 0.6*sin(2*pi*frequency/Frequency(12,'GHz')),'dB')

            forwardPower = generatorPower / insertionLoss
            reflectedPower = self.wattMeter.getPower(2) * reflectedAttenuation * switchAttenuation
        else:
            if self.amplifier.value == 'Prana':
                forwardAttenuation = PowerRatio(48.7 - 0.4*sin(2*pi*frequency/Frequency(1,'GHz')),'dB')
                reflectedAttenuation = forwardAttenuation / PowerRatio(0.1,'dB')            
            elif self.amplifier.value == 'Milmega 1':
                forwardAttenuation = PowerRatio(44.9 - 0.6*sin(2*pi*(frequency-Frequency(900,'MHz'))/Frequency(2,'GHz')),'dB')
                reflectedAttenuation = forwardAttenuation * PowerRatio(0.4,'dB')
            elif self.amplifier.value == 'Milmega 2':
                forwardAttenuation = PowerRatio(43.6 - 0.6*sin(2*pi*(frequency-Frequency(1.9,'GHz'))/Frequency(4,'GHz')),'dB')
                reflectedAttenuation = PowerRatio(44.4 - 1.1*sin(2*pi*(frequency-Frequency(1.9,'GHz'))/Frequency(4,'GHz')),'dB')
            else:
                raise ValueError, 'The switch platform is in an unsupported position.'
                
            (forwardPowerReadout,reflectedPowerReadout) = self.wattMeter.getPower()
            forwardPower = forwardPowerReadout * forwardAttenuation
            reflectedPower = reflectedPowerReadout * reflectedAttenuation * switchAttenuation


        result.data = {'generator power':generatorPower,
                       'forward power readout':forwardPowerReadout,
                       'reflected power readout':reflectedPowerReadout,
                       'forward power':forwardPower,
                       'reflected power':reflectedPower,
                       'transmitted power':forwardPower-reflectedPower}
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
    experiment.amplifier.setValue('Milmega 2')
    experiment.generatorFrequency = Frequency(150000,'Hz')
    experiment.generatorPower = Power(-15,'dBm')
#    experiment.rfGenerator.enableOutput()
    
    print experiment.measure()
