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


class DpiResult(ResultSet):
    name = 'DPI result'
    
    def __init__(self,powerLimits,frequencyRange):
        self.powerLimits = powerLimits
        self.frequencyRange = frequencyRange
        ResultSet.__init__(self,{\
            'injection frequency':Frequency,
            'generator power':Power,
            'pass':bool,
            'forward power':Power,
            'reflected power':Power,
            'reflection coefficent':PowerRatio,
            'transmitted power':Power,
            'limit':bool})
    def asDom(self,parent):
        element = ResultSet.asDom(self,parent)
        self.appendChildObject(element,self.powerLimits,'power limits')   
        self.appendChildObject(element,self.frequencyRange,'frequency range')
        return element
    
    @exportFunction('CSV one point per frequency',['xls','csv'])
    def exportAsCsvAShort(self,fileName):
        self._writeToCsv(fileName,onlyLimits=True)  

    @exportFunction('CSV all measurement points',['xls','csv'])    
    def exportAsCsvBLong(self,fileName):    
        self._writeToCsv(fileName,onlyLimits=False)        

    def _writeToCsv(self,fileName,onlyLimits):
        try:
            fileHandle = open(fileName,'wb')
        except:
            log.LogItem(sys.exc_info()[1],log.error)
        tableHeaders = ['frequency (Hz)','generator (dBm)','forward (dBm)','reflected (dBm)','transmitted (dBm)','fail']
        writer = csv.DictWriter(fileHandle,tableHeaders,dialect='excel-tab')
        writer.writeheader()
        
        for result in self.byRow():
            if not(onlyLimits) or result['limit']:
                writer.writerow({'frequency (Hz)':result['injection frequency'].Hz(),
                                 'generator (dBm)':result['generator power'].dBm(),
                                 'forward (dBm)':result['forward power'].dBm(),
                                 'reflected (dBm)':result['reflected power'].dBm(),
                                 'transmitted (dBm)':result['transmitted power'].dBm(),
                                 'fail':(0 if result['pass'] else 1) })
        fileHandle.close()
        fileHandle = None

        
    @classmethod
    def fromDom(cls,dom):
        newResult = super(DpiResult,cls).fromDom(dom)
        newResult.powerLimits = cls.childObjectById(dom,'power limits')
        newResult.frequencyRange = cls.childObjectById(dom,'frequency range')
        return newResult

class Dpi(Experiment,persistance.Dommable):
    name = 'Direct Power Injection'    
        
    def __init__(self):
        Experiment.__init__(self)
        self.passCriterion = ExperimentSlot(parent=self,defaultValue='VoltageCriterion')
        self.transmittedPower = ExperimentSlot(parent=self,defaultValue='TransmittedPower')
        self.powerMinimum = Property(Power(-30.,'dBm'),changedSignal=self.settingsChanged)

        self.powerMaximum = Property(Power(+15.,'dBm'),changedSignal=self.settingsChanged)
        self.frequencies = SweepRange(Frequency(150e3),Frequency(1500e6),21,changedSignal=self.settingsChanged) 
    def asDom(self,parent):
        element = persistance.Dommable.asDom(self,parent)
        self.appendChildObject(element,self.passCriterion.value,'pass criterion')
        self.appendChildObject(element,self.transmittedPower.value,'transmitted power')
        

        self.appendChildObject(element,self.powerMinimum.value,'power minimum')
        

        self.appendChildObject(element,self.powerMaximum.value,'power maximum')
        return element
    
    def connect(self):
        self.rfGenerator = knownDevices['rfGenerator']   
        self.switchPlatform = knownDevices['switchPlatform'] 
        
        self.transmittedPower.value.connect()
        self.passCriterion.value.connect()
    def prepare(self):
        self.switchPlatform.setPreset('bridge')
        self.rfGenerator.enableOutput(False)
        
        self.passCriterion.value.prepare()
        self.transmittedPower.value.prepare()

    def run(self):

        result = DpiResult(Power([self.powerMinimum.value,self.powerMaximum.value]),deepcopy(self.frequencies))
        self.emitResult(result)        
        
        guessPower = self.powerMinimum.value
        stepSizes = [5.0,1.0,0.5,.25] # dB
        def inclusiveRange(start,stop,step):
            if start != stop:
                return numpy.concatenate((numpy.arange(start,stop,step),[stop]))
            else:
                return numpy.array([stop])
        def findFailureFromBelow(startPower,stepIndex=0):
            def measureAndSavePass(tryPower):
                self.rfGenerator.setPower(tryPower)
                self.rfGenerator.enableOutput()
                passNotFail = self.passCriterion.value.measure()['pass']
                result.append( {'injection frequency':frequency,
                             'generator power':tryPower,
                             'pass':passNotFail,
                             'limit':False} )
                return passNotFail
            # make it work
            for tryPower in Power(inclusiveRange(startPower.dBm(),self.powerMinimum.value.dBm(),-stepSizes[stepIndex]),'dBm'):
                log.LogItem('Try to make the test pass with {tryPower}...'.format(tryPower=tryPower),log.debug)
                if measureAndSavePass(tryPower):
                    break
            else:
                log.LogItem('Did not succeed to make the test pass with {tryPower}...'.format(tryPower=tryPower),log.warning)
                return tryPower
                
            # make it fail
            for tryPower in Power(inclusiveRange(tryPower.dBm()+stepSizes[stepIndex],self.powerMaximum.value.dBm(),stepSizes[stepIndex]),'dBm'):
                log.LogItem('Try to make the test fail with {tryPower}...'.format(tryPower=tryPower),log.debug)
                if not measureAndSavePass(tryPower):
                    break
            else:
                return tryPower

            if stepIndex < len(stepSizes)-1:                
                return findFailureFromBelow(Power(tryPower.dBm()-stepSizes[stepIndex],'dBm'),stepIndex+1)
            else:
                return tryPower
                
        
        self.progressed.emit(0)
        for number,frequency in enumerate(self.frequencies.values):
            if self.stopRequested:
                break
            self.rfGenerator.setFrequency(frequency)
            log.LogItem('Passing to {frequency}'.format(frequency=frequency),log.debug)
            generatorPower = findFailureFromBelow(guessPower)
            measurement = self.transmittedPower.value.measure()
            result.append({'injection frequency':frequency,
                             'generator power':generatorPower,
                             'pass':self.passCriterion.value.measure()['pass'],
                             'reflected power':measurement['reflected power'],
                             'forward power':measurement['forward power'],
                             'transmitted power':measurement['transmitted power'],
                             'limit':True})

            self.progressed.emit(int(float(number+1)/self.frequencies.numberOfPoints.value*100.))
            
        self.rfGenerator.enableOutput(False)
        
        self.finished.emit()
        log.LogItem('Finished DPI',log.success)
        
        self.stopRequested = False
        

        
        
if __name__ == '__main__':
    import copy
    a = Dpi()
    print a.powerMaximum.value
    b = copy.deepcopy(a)
    print b.powerMaximum.value
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
    
        
                        