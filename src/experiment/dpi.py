from PyQt4.QtGui import QApplication

from device import knownDevices
from experiment import Experiment,Property,SweepRange
from utility.quantities import Power,PowerRatio
import numpy
from gui import logging
from copy import deepcopy

from result.resultset import ResultSet

class DpiResult(ResultSet):
    def __init__(self,powerLimits,frequencyRange):
        self.powerLimits = powerLimits
        self.frequencyRange = frequencyRange
        ResultSet.__init__(self,{\
            'frequency':float,
            'generatorPower':Power,
            'pass':bool,
            'forwardPower':Power,
            'reflectedPower':Power,
            'reflectionCoefficent':PowerRatio,
            'transmittedPower':Power,
            'limit':bool})




class Dpi(Experiment):
    name = 'Direct Power Injection'    
        
    def __init__(self):
        Experiment.__init__(self)
        self.powerMinimum = Property(-30.,changedSignal=self.settingsChanged)
        self.powerMaximum = Property(+15.,changedSignal=self.settingsChanged)
        self.frequencies = SweepRange(150e3,6000e6,11,changedSignal=self.settingsChanged) 
        
    def connect(self):
        self.rfGenerator = knownDevices['rfGenerator']   
        self.switchPlatform = knownDevices['switchPlatform'] 
        
        self.transmittedPower.connect()
        self.passCriterion.connect()
    def prepare(self):
        self.switchPlatform.setPreset('bridge')
        self.rfGenerator.enableOutput(False)
        
        self.passCriterion.prepare()
        self.transmittedPower.prepare()

    def run(self):
        result = DpiResult(Power([self.powerMinimum.value,self.powerMaximum.value],'dBm'),deepcopy(self.frequencies))
        self.newResult.emit(result)        
        
        guessPower = self.powerMinimum.value
        stepSizes = [5.0,1.0,0.5,.25]
        def inclusiveRange(start,stop,step):
            if start != stop:
                return numpy.concatenate((numpy.arange(start,stop,step),[stop]))
            else:
                return numpy.array([stop])
        def findFailureFromBelow(startPower,stepIndex=0):
            def measureAndSavePass(tryPower):
                self.rfGenerator.setPower(Power(tryPower,'dBm'))
                self.rfGenerator.enableOutput()
                passNotFail = self.passCriterion.measure()['Pass']
                result.append( {'frequency':frequency,
                             'generatorPower':Power(tryPower,'dBm'),
                             'pass':passNotFail,
                             'limit':False} )
                return passNotFail
            # make it work
            for tryPower in inclusiveRange(startPower,self.powerMinimum.value,-stepSizes[stepIndex]):
                logging.LogItem('Try to make the test pass with {tryPower:.1f} dBm...'.format(tryPower=tryPower),logging.debug)
                if measureAndSavePass(tryPower):
                    break
            else:
                logging.LogItem('Did not succeed to make the test pass with {tryPower:.1f} dBm...'.format(tryPower=tryPower),logging.warning)
                return tryPower
                
            # make it fail
            for tryPower in inclusiveRange(tryPower+stepSizes[stepIndex],self.powerMaximum.value,stepSizes[stepIndex]):
                logging.LogItem('Try to make the test fail with {tryPower:.1f} dBm...'.format(tryPower=tryPower),logging.debug)
                if not measureAndSavePass(tryPower):
                    break
            else:
                return tryPower

            if stepIndex < len(stepSizes)-1:                
                return findFailureFromBelow(tryPower-stepSizes[stepIndex],stepIndex+1)
            else:
                return tryPower
                
        
#        self._result.changed.connect(self.resultChanged)
#        self._result.added.connect(self.resultAdded)
        
        self.progressed.emit(0)
        for number,frequency in enumerate(self.frequencies.values):
            if self.stopRequested:
                break
            self.rfGenerator.setFrequency(frequency)
            logging.LogItem('Passing to {frequency:.2e} Hz'.format(frequency=frequency),logging.debug)
            generatorPower = findFailureFromBelow(guessPower)
            measurement = self.transmittedPower.measure()
            result.append({'frequency':frequency,
                             'generatorPower':Power(generatorPower,'dBm'),
                             'pass':self.passCriterion.measure()['Pass'],
                             'reflectedPower':measurement['Reflected power'],
                             'forwardPower':measurement['Forward power'],
                             'transmittedPower':measurement['Transmitted power'],
                             'limit':True})

#            self.resultChanged.emit()

            self.progressed.emit(int(float(number+1)/self.frequencies.numberOfPoints.value*100.))
            
        self.rfGenerator.enableOutput(False)
        
        self.finished.emit()
        logging.LogItem('Finished DPI',logging.success)
        self.stopRequested = False
        
        return result
        
        
if __name__ == '__main__':
    from voltagecriterion import VoltageCriterion
    from transmittedpower import TransmittedPower
    
    
    logging.LogModel.Instance().gui = False




    import numpy
    experiment = Dpi()
    experiment.passCriterion = VoltageCriterion()
    experiment.transmittedPower = TransmittedPower()

    experiment.connect()
    experiment.prepare()
    results = experiment.run()
    print results._data
    
        
                        