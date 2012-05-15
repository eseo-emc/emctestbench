from device import knownDevices
from utility.quantities import Power
from experiment import Experiment
from result import persistance
import numpy
from copy import copy

from calibration.bridge import bridgeInsertionTransferAt,bridgeCouplingFactorAt

from result.resultset import DictResult

class TransmittedPower(Experiment,persistance.Dommable):
    name = 'Transmitted Power Calculation'
    
    def connect(self):
        self.switchPlatform = knownDevices['switchPlatform']
        self.wattMeter = knownDevices['wattMeter']
        self.rfGenerator = knownDevices['rfGenerator']

    def prepare(self):
        self.wattMeter.reset()
    def measure(self):
        if self.switchPlatform.checkPreset('bridge'):
            result = DictResult()
            generatorPower = self.rfGenerator.getPower()
            frequency = self.rfGenerator.getFrequency()
            forwardPower = generatorPower * bridgeInsertionTransferAt(frequency)
         
            reflectedPower = self.wattMeter.getPower(2) / bridgeCouplingFactorAt(frequency)
            result.data = {'Generator power':generatorPower,
                           'Transmitted power':forwardPower-reflectedPower,
                           'Forward power':forwardPower,
                           'Reflected power':reflectedPower}
            self.emitResult(result)
            return result
            
        else:
            raise ValueError, 'The switch platform is in an unsupported position.'
    def run(self):
        self.measure()            
            
    def tryTransmittedPower(self,nominalPower):
        generatorMaximum = Power(20,'dBm')
        tryForwardPower = copy(nominalPower)
        for tryNumber in range(4):
#            print tryForwardPower
            self.rfGenerator.setPower(tryForwardPower)
            self.rfGenerator.enableOutput()
            realTransmittedPower = self.measure()['transmittedPower']
            realTransmittedPower = realTransmittedPower.max(Power(-40,'dBm'))

            gain = nominalPower/realTransmittedPower

            tryForwardPower *= gain
            tryForwardPower = tryForwardPower.min(generatorMaximum)

        return self.measure()['transmittedPower']

        
    
if __name__ == '__main__':
    experiment = TransmittedPower()
    experiment.connect()
    experiment.prepare()
    experiment.switchPlatform.setPreset('bridge')
#    print experiment.tryTransmittedPower(Power(0,'dBm'))

    experiment.rfGenerator.setFrequency(150000.)
    experiment.rfGenerator.setPower(Power(8.2,'dBm'))
    experiment.rfGenerator.enableOutput()
    
    print experiment.measure()
