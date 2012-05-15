from device import knownDevices
from experiment import Experiment,ExperimentSlot,Property,SweepRange
from utility.quantities import Power,PowerRatio,Frequency
from result import persistance
import numpy
from gui import logging
from copy import deepcopy

from result.resultset import ResultSet,exportFunction

import csv



class DpiResult(ResultSet):
    name = 'DPI result'
    
    def __init__(self,powerLimits,frequencyRange):
        self.powerLimits = powerLimits
        self.frequencyRange = frequencyRange
        ResultSet.__init__(self,{\
            'frequency':Frequency,
            'generatorPower':Power,
            'pass':bool,
            'forwardPower':Power,
            'reflectedPower':Power,
            'reflectionCoefficent':PowerRatio,
            'transmittedPower':Power,
            'limit':bool})
    def asDom(self,parent):
        element = ResultSet.asDom(self,parent)
        self.appendChildObject(element,self.powerLimits,'Power limits')   
        self.appendChildObject(element,self.frequencyRange,'Frequency range')
        return element
    
    @exportFunction('CSV one point per frequency',['xls','csv'])
    def exportAsCsvAShort(self,fileName):
        self._writeToCsv(fileName,onlyLimits=True)  

    @exportFunction('CSV all measurement points',['xls','csv'])    
    def exportAsCsvBLong(self,fileName):    
        self._writeToCsv(fileName,onlyLimits=False)        

    def _writeToCsv(self,fileName,onlyLimits):
        fileHandle = open(fileName,'wb')
        tableHeaders = ['frequency (Hz)','generator (dBm)','forward (dBm)','reflected (dBm)','transmitted (dBm)','fail']
        writer = csv.DictWriter(fileHandle,tableHeaders,dialect='excel-tab')
        writer.writeheader()
        
        for result in self.byRow():
            if not(onlyLimits) or result['limit']:
                writer.writerow({'frequency (Hz)':result['frequency'],
                                 'generator (dBm)':result['generatorPower'].dBm(),
                                 'forward (dBm)':result['forwardPower'].dBm(),
                                 'reflected (dBm)':result['reflectedPower'].dBm(),
                                 'transmitted (dBm)':result['transmittedPower'].dBm(),
                                 'fail':(0 if result['pass'] else 1) })
        fileHandle.close()
        fileHandle = None

        
    @classmethod
    def fromDom(cls,dom):
        newResult = super(DpiResult,cls).fromDom(dom)
        newResult.powerLimits = cls.childObjectById(dom,'Power limits')
        newResult.frequencyRange = cls.childObjectById(dom,'Frequency range')
        return newResult

class Dpi(Experiment,persistance.Dommable):
    name = 'Direct Power Injection'    
        
    def __init__(self):
        Experiment.__init__(self)
        self.passCriterion = ExperimentSlot(parent=self,defaultValue='VoltageCriterion')
        self.transmittedPower = ExperimentSlot(parent=self,defaultValue='TransmittedPower')
        self.powerMinimum = Property(-30.,changedSignal=self.settingsChanged)
        self.powerMaximum = Property(+15.,changedSignal=self.settingsChanged)
        self.frequencies = SweepRange(150e3,1500e6,11,changedSignal=self.settingsChanged) 
    def asDom(self,parent):
        element = persistance.Dommable.asDom(self,parent)
        self.appendChildObject(element,self.passCriterion.value,'Pass Criterion')
        self.appendChildObject(element,self.transmittedPower.value,'Transmitted Power')
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
        result = DpiResult(Power([self.powerMinimum.value,self.powerMaximum.value],'dBm'),deepcopy(self.frequencies))
        self.emitResult(result)        
        
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
                passNotFail = self.passCriterion.value.measure()['Pass']
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
                
        
        self.progressed.emit(0)
        for number,frequency in enumerate(self.frequencies.values):
            if self.stopRequested:
                break
            self.rfGenerator.setFrequency(frequency)
            logging.LogItem('Passing to {frequency:.2e} Hz'.format(frequency=frequency),logging.debug)
            generatorPower = findFailureFromBelow(guessPower)
            measurement = self.transmittedPower.value.measure()
            result.append({'frequency':frequency,
                             'generatorPower':Power(generatorPower,'dBm'),
                             'pass':self.passCriterion.value.measure()['Pass'],
                             'reflectedPower':measurement['Reflected power'],
                             'forwardPower':measurement['Forward power'],
                             'transmittedPower':measurement['Transmitted power'],
                             'limit':True})

            self.progressed.emit(int(float(number+1)/self.frequencies.numberOfPoints.value*100.))
            
        self.rfGenerator.enableOutput(False)
        
        self.finished.emit()
        logging.LogItem('Finished DPI',logging.success)
        self.stopRequested = False
        

        
        
if __name__ == '__main__':
    print DpiResult.exportTypes
#    from voltagecriterion import VoltageCriterion
#    from transmittedpower import TransmittedPower
#    
#    
#    logging.LogModel.Instance().gui = False
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
    
        
                        