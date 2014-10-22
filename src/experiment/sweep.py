from device import knownDevices
from experiment import Experiment,ExperimentSlot,Property,SweepRange
from utility.quantities import Power,PowerRatio,Frequency
from result import persistance
import numpy
from gui import log
from copy import deepcopy

from result.resultset import ResultSet,exportFunction

import csv
import sys

import time


class SweepResult(ResultSet):
    name = 'Sweep result'

class Sweep(Experiment,persistance.Dommable):
    name = 'Sweep'    
        
    def __init__(self):
        Experiment.__init__(self)
        self.stimulusRange = SweepRange(Frequency(100e3),Frequency(20e9),21,changedSignal=self.settingsChanged) 

        self.stimulus = ExperimentSlot(parent=self)
        self.measurement = ExperimentSlot(parent=self) #,defaultValue='TransmittedPower')
    def asDom(self,parent):
        element = persistance.Dommable.asDom(self,parent)
        self.appendChildObject(element,self.stimulus.value,'stimulus')
        self.appendChildObject(element,self.measurement.value,'measurement')
        
        return element
    
    def connect(self):
        self.stimulus.value.connect()
        self.measurement.value.connect()
    def prepare(self):
        self.stimulus.value.prepare()
        self.measurement.value.prepare()

    def run(self):
        result = SweepResult(deepcopy(self.stimulusRange))
        self.emitResult(result)        
        
        self.progressed.emit(0)
        for number,stimulusValue in enumerate(self.sweepRange.values):
            if self.stopRequested:
                break
            self.stimulus.value.stimulus = stimulusValue
            
            log.LogItem('Passing to {value}'.format(value=stimulusValue),log.debug)
            measurement = self.measurement.value.measure()
            sample = {'stimulus':stimulusValue}
            sample.update(measurement)
            result.append(sample)

            self.progressed.emit(int(float(number+1)/self.sweepRange.numberOfPoints.value*100.))
            
        self.stimulus.value.tearDown()
        self.measurement.value.tearDown()
        
        result.finish()
        self.finished.emit()
        log.LogItem('Finished sweep',log.success)
        
        self.stopRequested = False
        
        

        
#        
#if __name__ == '__main__':
#    from transmittedpower import TransmittedPower
#    
#    
#    log.LogModel.Instance().gui = False
#
#
#
#
#    import numpy
#    experiment = FrequencySweep()
#    experiment.transmittedPower.value = TransmittedPower
#
#    experiment.connect()
#    experiment.prepare()
#    results = experiment.run()
#    print results._data
#    
#        
#                        