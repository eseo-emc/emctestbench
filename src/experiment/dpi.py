from device import knownDevices
from experiment import Experiment
from transmittedpower import TransmittedPower
from utility import Power
import numpy

class VoltageCriterion(Experiment):
    def __init__(self,voltageMargin=0.05):
        self.voltMeter = knownDevices['multimeter']
        self.voltageMargin = voltageMargin
        
        self.undisturbedOutputVoltage = None
    def prepare(self):
        self.undisturbedOutputVoltage = self.voltMeter.measure()
    def measure(self):
        outputVoltage = self.voltMeter.measure()
        return {'pass':abs(outputVoltage -self.undisturbedOutputVoltage) <= self.voltageMargin,
                'outputVoltage (V)':outputVoltage}


class Dpi(Experiment):
    def __init__(self,frequencies,dBmForwardPowerLimits):
        self.frequencies = frequencies
        self.dBmForwardPowerLimits = dBmForwardPowerLimits        
        
        self.rfGenerator = knownDevices['rfGenerator']   
        self.switchPlatform = knownDevices['switchPlatform'] 
                
        self.transmittedPower = TransmittedPower()
        self.switchPlatform.setPreset('bridge')
        
        self.passCriterion = VoltageCriterion()
        

    def prepare(self):
        self.rfGenerator.enableOutput(False)
        self.passCriterion.prepare()
        
    def measure(self):
        guessPower = self.dBmForwardPowerLimits[0]
        stepSizes = [5.0,1.0,0.5,.25]
        def inclusiveRange(start,stop,step):
            if start != stop:
                return numpy.concatenate((numpy.arange(start,stop,step),[stop]))
            else:
                return numpy.array([stop])
        def findFailureFromBelow(startPower,stepIndex=0):
            # make it work
            for tryPower in inclusiveRange(startPower,self.dBmForwardPowerLimits[0],-stepSizes[stepIndex]):
                self.rfGenerator.setPower(Power(tryPower,'dBm'))
#                print tryPower
                if self.passCriterion.measure()['pass']:
                    break
            else:
                #TODO: not being able to get it to work while descending down to the minimum forward power is a bad sign, this error should be handled or reported somewhere                        
                return tryPower
                
            # make it fail
            for tryPower in inclusiveRange(tryPower+stepSizes[stepIndex],self.dBmForwardPowerLimits[1],stepSizes[stepIndex]):
                self.rfGenerator.setPower(Power(tryPower,'dBm'))
#                print tryPower
                self.rfGenerator.enableOutput()
                if not self.passCriterion.measure()['pass']:
                    break
            else:
                return tryPower

            if stepIndex < len(stepSizes)-1:                
                return findFailureFromBelow(tryPower-stepSizes[stepIndex],stepIndex+1)
            else:
                return tryPower
                
        measurements = []
        for frequency in self.frequencies:
            self.rfGenerator.setFrequency(frequency)
            generatorPower = findFailureFromBelow(guessPower)
            measurement = self.transmittedPower.measure()
            measurement.update({'frequency':frequency,'pass':self.passCriterion.measure()['pass'],'generatorPower':Power(generatorPower,'dBm')})
            measurements.append(measurement)
        self.rfGenerator.enableOutput(False)
        return measurements
        
        
if __name__ == '__main__':
#    experiment = VoltageCriterion()
#    experiment.prepare()
#    print experiment.measure()
    import numpy
    experiment = Dpi(numpy.arange(300e3,1e9,100e6),(-30,+15))
    experiment.prepare()
    results = experiment.measure()
    print results
    
    import csv
    import datetime
    fileName = 'Y:/emctestbench/results/dpi'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.xls'
    tableHeaders = ['frequency (Hz)','generator (dBm)','forward (dBm)','reflected (dBm)','transmitted (dBm)','fail']
    writer = csv.DictWriter(open(fileName,'wb'),tableHeaders,dialect='excel-tab')
    writer.writeheader()
    for result in results:
        writer.writerow({'frequency (Hz)':result['frequency'],
                         'generator (dBm)':result['generatorPower'].dBm(),
                         'forward (dBm)':result['forwardPower'].dBm(),
                         'reflected (dBm)':result['reflectedPower'].dBm(),
                         'transmitted (dBm)':result['transmittedPower'].dBm(),
                         'fail':(0 if result['pass'] else 1) })
    
                        