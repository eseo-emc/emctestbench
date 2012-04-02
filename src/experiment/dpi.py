from device import knownDevices
from experiment import Experiment
from transmittedpower import TransmittedPower
from utility import Power
import numpy
from gui import logging

class VoltageCriterion(Experiment):
    name = 'Voltage offset criterion'
    def connect(self):
        self.voltMeter = knownDevices['multimeter']        
        self.undisturbedOutputVoltage = None
    def prepare(self,voltageMargin=0.05):
        self.voltageMargin = voltageMargin
        self.undisturbedOutputVoltage = self.voltMeter.measure()
    def measure(self):
        outputVoltage = self.voltMeter.measure()
        return {'pass':abs(outputVoltage -self.undisturbedOutputVoltage) <= self.voltageMargin,
                'outputVoltage (V)':outputVoltage}


class Dpi(Experiment):
    name = 'Direct Power Injection'
    def connect(self):
        self.rfGenerator = knownDevices['rfGenerator']   
        self.switchPlatform = knownDevices['switchPlatform'] 
        
        self.transmittedPower = TransmittedPower()
        self.transmittedPower.connect()
        self.passCriterion = VoltageCriterion()        
        self.passCriterion.connect()
    def prepare(self,frequencies=[300e3],dBmForwardPowerLimits=(-30,+0)):
        self.frequencies = frequencies
        self.dBmForwardPowerLimits = dBmForwardPowerLimits        
        
        
        self.switchPlatform.setPreset('bridge')
        self.rfGenerator.enableOutput(False)
        
        self.passCriterion.prepare()
        self.transmittedPower.connect()
        
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
                logging.LogItem('Try to make it work with {tryPower:.1f} dBm...'.format(tryPower=tryPower),logging.debug)
                if self.passCriterion.measure()['pass']:
                    break
            else:
                #TODO: not being able to get it to work while descending down to the minimum forward power is a bad sign, this error should be handled or reported somewhere                        
                return tryPower
                
            # make it fail
            for tryPower in inclusiveRange(tryPower+stepSizes[stepIndex],self.dBmForwardPowerLimits[1],stepSizes[stepIndex]):
                self.rfGenerator.setPower(Power(tryPower,'dBm'))
                logging.LogItem('Try to make it fail with {tryPower:.1f} dBm...'.format(tryPower=tryPower),logging.debug)
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
            logging.LogItem('Passing to {frequency:.2e} Hz'.format(frequency=frequency),logging.debug)
            generatorPower = findFailureFromBelow(guessPower)
            measurement = self.transmittedPower.measure()
            measurement.update({'frequency':frequency,'pass':self.passCriterion.measure()['pass'],'generatorPower':Power(generatorPower,'dBm')})
            measurements.append(measurement)
        self.rfGenerator.enableOutput(False)
        return measurements
        
        
if __name__ == '__main__':
    logging.LogModel.Instance().gui = False
#    experiment = VoltageCriterion()
#    experiment.prepare()
#    print experiment.measure()


    import numpy
    experiment = Dpi()
    experiment.connect()
    experiment.prepare(numpy.arange(300e3,150e6,100e6),(-30,+15))
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
    
                        