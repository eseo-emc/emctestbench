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


class FrequencySweepResult(ResultSet):
    name = 'Frequency Sweep result'
    
    def __init__(self,generatorPower,frequencyRange):
        self.generatorPower = generatorPower
        self.frequencyRange = frequencyRange
        ResultSet.__init__(self,{\
            'frequency':Frequency,
            'forward power':Power,
            'reflected power':Power,
            'reflection coefficient':PowerRatio,
            'transmitted power':Power})
    def asDom(self,parent):
        element = ResultSet.asDom(self,parent)
        self.appendChildObject(element,self.generatorPower,'generator power')   
        self.appendChildObject(element,self.frequencyRange,'frequency range')
        return element
    
    @exportFunction('CSV all measurement points',['xls','csv'])    
    def exportAsCsvBLong(self,fileName):    
        self._writeToCsv(fileName)        

    def _writeToCsv(self,fileName):
        try:
            fileHandle = open(fileName,'wb')
        except:
            log.LogItem(sys.exc_info()[1],log.error)
        tableHeaders = ['frequency (Hz)','forward (dBm)','reflected (dBm)','S11 (dB)']
        writer = csv.DictWriter(fileHandle,tableHeaders,dialect='excel-tab')
        writer.writeheader()
        

        
        for result in self.byRow():
            writer.writerow({'frequency (Hz)':self.formatFloatLocale(result['frequency'].Hz()),
                             'forward (dBm)':self.formatFloatLocale(result['forward power'].dBm()),
                             'reflected (dBm)':self.formatFloatLocale(result['reflected power'].dBm()),
                             'S11 (dB)':self.formatFloatLocale(result['reflection coefficient'].asUnit('dB')) })
        fileHandle.close()
        fileHandle = None

        
    @classmethod
    def fromDom(cls,dom):
        newResult = super(FrequencySweepResult,cls).fromDom(dom)
        newResult.generatorPower = cls.childObjectById(dom,'generator power')
        newResult.frequencyRange = cls.childObjectById(dom,'frequency range')
        return newResult

class FrequencySweep(Experiment,persistance.Dommable):
    name = 'Frequency Sweep'    
        
    def __init__(self):
        Experiment.__init__(self)
        self.generatorPower = Property(Power(-10.,'dBm'),changedSignal=self.settingsChanged)
        self.frequencies = SweepRange(Frequency(100e3),Frequency(20e9),21,changedSignal=self.settingsChanged) 

        self.transmittedPower = ExperimentSlot(parent=self) #,defaultValue='TransmittedPower')
    def asDom(self,parent):
        element = persistance.Dommable.asDom(self,parent)
        self.appendChildObject(element,self.transmittedPower.value,'transmitted power')
        self.appendChildObject(element,self.generatorPower.value,'generated power')
        
        return element
    
    def connect(self):
        self.rfGenerator = knownDevices['rfGenerator']   
        self.switchPlatform = knownDevices['switchPlatform'] 
        
        self.transmittedPower.value.connect()
    def prepare(self):
        self.transmittedPower.value.prepare()

    def run(self):

        result = FrequencySweepResult(self.generatorPower.value,deepcopy(self.frequencies))
        self.emitResult(result)        
        
        self.transmittedPower.value.generatorPower = self.generatorPower.value

          
        self.progressed.emit(0)
        for number,frequency in enumerate(self.frequencies.values):
            if self.stopRequested:
                break
            self.transmittedPower.value.generatorFrequency = frequency
            
            print frequency   
            log.LogItem('Passing to {frequency}'.format(frequency=frequency),log.debug)
            measurement = self.transmittedPower.value.measure()
            result.append({'frequency':frequency,
                             'reflected power':measurement['reflected power'],
                             'forward power':measurement['forward power'],
                             'transmitted power':measurement['transmitted power'],
                             'reflection coefficient':measurement['reflection coefficient']})

            self.progressed.emit(int(float(number+1)/self.frequencies.numberOfPoints.value*100.))
            
        self.transmittedPower.value.tearDown()
        
        self.finished.emit()
        log.LogItem('Finished frequency sweep',log.success)
        
        self.stopRequested = False
        
        

        
        
if __name__ == '__main__':
    from transmittedpower import TransmittedPower
    
    
    log.LogModel.Instance().gui = False




    import numpy
    experiment = FrequencySweep()
    experiment.transmittedPower.value = TransmittedPower

    experiment.connect()
    experiment.prepare()
    results = experiment.run()
    print results._data
    
        
                        