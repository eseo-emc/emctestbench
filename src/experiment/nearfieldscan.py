from device import knownDevices
from experiment import Experiment,ExperimentSlot,Property,ScalarProperty,SweepRange
from utility.quantities import Power,Position,Frequency,Integer
from result import persistance
import numpy
from gui import log
from copy import deepcopy

from result.resultset import ResultSet,exportFunction

import csv
import sys

class NearFieldScanResult(ResultSet):
    def __init__(self):
        ResultSet.__init__(self,{'position':Position})

class NearFieldScan(Experiment,persistance.Dommable):
    name = 'Near Field Scan'    
        
    def __init__(self):
        Experiment.__init__(self)
        self.transmittedPower = ExperimentSlot(parent=self,defaultValue='TransmittedPower')
        self.measurement = ExperimentSlot(parent=self,defaultValue='ReceivedPower') #,defaultValue='VoltageCriterion')
        
        self.generatorPower = Property(Power(+10,'dBm'),changedSignal=self.settingsChanged)
        self.generatorFrequency = ScalarProperty(Frequency(1,'GHz'),changedSignal=self.settingsChanged,minimum=Frequency(1,'Hz'))

        self.startPosition = ScalarProperty(Position(-5,'mm'),changedSignal=self.settingsChanged)
        self.stopPosition = ScalarProperty(Position(5,'mm'),changedSignal=self.settingsChanged)
        self.xPosition = ScalarProperty(Position(113,'mm'),changedSignal=self.settingsChanged)
        self.zPosition = ScalarProperty(Position(84,'mm'),changedSignal=self.settingsChanged)
        
        self.numberOfSteps = ScalarProperty(Integer(11),minimum=Integer(1),maximum=Integer(10001),changedSignal=self.settingsChanged)
        
#    def asDom(self,parent):
#        element = persistance.Dommable.asDom(self,parent)
#        self.appendChildObject(element,self.passCriterion.value,'pass criterion')
#        self.appendChildObject(element,self.transmittedPower.value,'transmitted power')
#        
#
#        self.appendChildObject(element,self.powerMinimum.value,'power minimum')
#        
#
#        self.appendChildObject(element,self.powerMaximum.value,'power maximum')
#        return element
    
    def positions(self):
        def linearSteps(start,stop,steps):
            path = stop - start
            return start + numpy.outer(numpy.linspace(0,1,steps),path)
        startPosition = Position([self.xPosition.value,self.startPosition.value,self.zPosition.value])            
        stopPosition = Position([self.xPosition.value,self.stopPosition.value,self.zPosition.value])                    
        
        return linearSteps(startPosition,stopPosition,self.numberOfSteps.value)
    
    def readStartPosition(self):
        location = self.positioner.getLocation()
        self.startPosition.value = location[1]
        self.xPosition.value = location[0]
        self.zPosition.value = location[2]
    
    def connect(self):
        self.rfGenerator = knownDevices['rfGenerator']   
        self.switchPlatform = knownDevices['switchPlatform'] 
        self.positioner = knownDevices['positioner']
        
        
        self.transmittedPower.value.connect()
        self.measurement.value.connect()
    def prepare(self):
        self.positioner.prepare()
        
        self.transmittedPower.value.prepare()
#        self.measurement.value.prepare()

    def run(self):
        result = NearFieldScanResult() 
        self.emitResult(result)   

        self.transmittedPower.value.generatorFrequency = self.generatorFrequency.value
        self.transmittedPower.value.generatorPower = self.generatorPower.value

        self.progressed.emit(0)
        for number,position in enumerate(self.positions()):
            if self.stopRequested:
                break
            
            log.LogItem('Passing to {position}'.format(position=position),log.debug)
            location = self.positioner.setLocation(position)
            measurement = {'position':location}
            measurement.update( self.transmittedPower.value.measure().data )
#            measurement.update( {'received power':self.spectrumAnalyzer.powerAt(self.generatorFrequency.value)})
            measurement.update( self.measurement.value.measure().data )
            result.append(measurement)

            self.progressed.emit(int(float(number+1)/self.numberOfSteps.value*100.))
            
        self.transmittedPower.value.tearDown()
        self.positioner.tearDown()
        
        self.finished.emit()
        log.LogItem('Finished Near Field Scan',log.success)
        
        self.stopRequested = False
        

        
        
if __name__ == '__main__':
    import copy
    a = NearFieldScan()
   
#    from voltagecriterion import VoltageCriterion
#    from transmittedpower import TransmittedPower
#    
#    
#    log.LogModel.Instance().gui = False
#
#
#
#
#    import numpy
#    experiment = Dpi()
#    experiment.passCriterion.value = VoltageCriterion
#    experiment.transmittedPower.value = TransmittedPower
#
#    experiment.connect()
#    experiment.prepare()
#    results = experiment.run()
#    print results._data
    
        
                        