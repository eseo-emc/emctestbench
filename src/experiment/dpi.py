from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QApplication

from device import knownDevices
from experiment import Experiment,Property
from transmittedpower import TransmittedPower
from utility import Power
import numpy
from gui import logging

from result import ResultSet

class DpiResultSet(ResultSet):
    def __init__(self,powerLimits):
        self.powerLimits = powerLimits
        ResultSet.__init__(self,{\
            'frequency':float,
            'generatorPower':Power,
            'pass':bool,
            'forwardPower':Power,
            'reflectedPower':Power,
            'transmittedPower':Power })

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

class SweepRange(object):
    def __init__(self,startValue=0,stopValue=1,numberOfPoints=101,logarithmic=False,changedSignal=None):
        self.start = Property(startValue,changedSignal=changedSignal)
        self.stop = Property(stopValue,changedSignal=changedSignal)
        self.numberOfPoints = Property(numberOfPoints,changedSignal=changedSignal,castTo=int)
        self.logarithmic = Property(logarithmic,changedSignal=changedSignal)
    @property
    def values(self):
        if self.logarithmic.value:
            return numpy.exp(numpy.linspace(numpy.log(self.start.value),numpy.log(self.stop.value),self.numberOfPoints.value))
        else:
            return numpy.linspace(self.start.value,self.stop.value,self.numberOfPoints.value)

class Dpi(Experiment):
    name = 'Direct Power Injection'    
        
    settingsChanged = pyqtSignal()
    resultAdded = pyqtSignal(dict)
    resultChanged = pyqtSignal()
    progressed = pyqtSignal(int)
    finished = pyqtSignal()        
    
    def __init__(self):
        Experiment.__init__(self)
        self.powerMinimum = Property(-30.,changedSignal=self.settingsChanged)
        self.powerMaximum = Property(+15.,changedSignal=self.settingsChanged)
        self.frequencies = SweepRange(300e3,150e6,11,changedSignal=self.settingsChanged) 
        
        self._result = None
    
    def result(self):
        return self._result
        
    def connect(self):
        self.rfGenerator = knownDevices['rfGenerator']   
        self.switchPlatform = knownDevices['switchPlatform'] 
        
        self.transmittedPower = TransmittedPower()
        self.transmittedPower.connect()
        self.passCriterion = VoltageCriterion()        
        self.passCriterion.connect()
    def prepare(self):
        self.switchPlatform.setPreset('bridge')
        self.rfGenerator.enableOutput(False)
        
        self.passCriterion.prepare()
        self.transmittedPower.connect()

    def run(self):
        guessPower = self.powerMinimum.value
        stepSizes = [5.0,1.0,0.5,.25]
        def inclusiveRange(start,stop,step):
            if start != stop:
                return numpy.concatenate((numpy.arange(start,stop,step),[stop]))
            else:
                return numpy.array([stop])
        def findFailureFromBelow(startPower,stepIndex=0):
            # make it work
            for tryPower in inclusiveRange(startPower,self.powerMinimum.value,-stepSizes[stepIndex]):
                self.rfGenerator.setPower(Power(tryPower,'dBm'))
                logging.LogItem('Try to make the test pass with {tryPower:.1f} dBm...'.format(tryPower=tryPower),logging.debug)
                if self.passCriterion.measure()['pass']:
                    break
            else:
                logging.LogItem('Did not succeed to make the test pass with {tryPower:.1f} dBm...'.format(tryPower=tryPower),logging.warning)

                return tryPower
                
            # make it fail
            for tryPower in inclusiveRange(tryPower+stepSizes[stepIndex],self.powerMaximum.value,stepSizes[stepIndex]):
                self.rfGenerator.setPower(Power(tryPower,'dBm'))
                logging.LogItem('Try to make the test fail with {tryPower:.1f} dBm...'.format(tryPower=tryPower),logging.debug)
                self.rfGenerator.enableOutput()
                if not self.passCriterion.measure()['pass']:
                    break
            else:
                return tryPower

            if stepIndex < len(stepSizes)-1:                
                return findFailureFromBelow(tryPower-stepSizes[stepIndex],stepIndex+1)
            else:
                return tryPower
                
        self._result = DpiResultSet((self.powerMinimum.value,self.powerMaximum.value))
        self._result.changed.connect(self.resultChanged)
        self._result.added.connect(self.resultAdded)
        
        self.progressed.emit(0)
        for number,frequency in enumerate(self.frequencies.values):
            if self.stopRequested:
                break
            self.rfGenerator.setFrequency(frequency)
            logging.LogItem('Passing to {frequency:.2e} Hz'.format(frequency=frequency),logging.debug)
            generatorPower = findFailureFromBelow(guessPower)
            measurement = self.transmittedPower.measure()
            self._result.append({'frequency':frequency,
                                 'generatorPower':Power(generatorPower,'dBm'),
                                 'pass':self.passCriterion.measure()['pass'],
                                 'reflectedPower':measurement['reflectedPower'],
                                 'forwardPower':measurement['forwardPower'],
                                 'transmittedPower':measurement['transmittedPower'] })

#            self.resultChanged.emit()

            self.progressed.emit(int(float(number+1)/self.frequencies.numberOfPoints.value*100.))
            
        self.rfGenerator.enableOutput(False)
        
        self.finished.emit()
        logging.LogItem('Finished DPI',logging.success)
        self.stopRequested = False
        
        
if __name__ == '__main__':
    logging.LogModel.Instance().gui = False
#    experiment = VoltageCriterion()
#    experiment.prepare()
#    print experiment.measure()


    import numpy
    experiment = Dpi()
    experiment.connect()
    experiment.prepare()
    experiment.run()
    results = experiment.result()
    print results
    
        
                        