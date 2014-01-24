from device import knownDevices
from experiment import Experiment,ExperimentSlot,Property,SweepRange
from utility.quantities import Power,PowerRatio,Frequency,Integer
from result import persistance
import numpy
from gui import log
from copy import deepcopy
import StringIO

from result.resultset import ResultSet,exportFunction

import csv
import sys

def inclusiveRange(start,stop,step):
    if start != stop:
        return numpy.concatenate((numpy.arange(start,stop,step),[stop]))
    else:
        return numpy.array([stop])

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

    @exportFunction('CSV one point per frequency, skipping non-failing points',['xls','csv'])
    def exportAsCsvAShortHoles(self,fileName):
        self._writeToCsv(fileName,onlyLimits=True,passHoles=True)
    
    @exportFunction('CSV one point per frequency',['xls','csv'])
    def exportAsCsvBShort(self,fileName):
        self._writeToCsv(fileName,onlyLimits=True,passHoles=False)  

    @exportFunction('CSV all measurement points',['xls','csv'])    
    def exportAsCsvCLong(self,fileName):    
        self._writeToCsv(fileName,onlyLimits=False,passHoles=False)        

    def _writeToCsv(self,fileName,onlyLimits,passHoles):
        if not fileName:
            fileHandle = StringIO.StringIO()
        else:
            try:
                fileHandle = open(fileName,'wb',buffering=4096)
            except:
                log.LogItem(sys.exc_info()[1],log.error)
        tableHeaders = ['frequency (Hz)','forward (dBm)','reflected (dBm)','transmitted (dBm)','generator (dBm)','amplifier','fail']
        if not(onlyLimits):
            tableHeaders.append(['limit'])
        writer = csv.DictWriter(fileHandle,tableHeaders,dialect='excel-tab')
        writer.writeheader()
        

        
        for result in self.byRow():
            if not(onlyLimits) or result['limit']:
                row = {'frequency (Hz)':self.formatFloatLocale(result['injection frequency'].Hz()),
                       'fail':(0 if result['pass'] else 1) }
                if not(passHoles) or not(result['pass']):
                    row.update({'generator (dBm)':self.formatFloatLocale(result['generator power'].dBm()),
                         'forward (dBm)':self.formatFloatLocale(result['forward power'].dBm()),
                         'reflected (dBm)':self.formatFloatLocale(result['reflected power'].dBm()),
                         'transmitted (dBm)':self.formatFloatLocale(result['transmitted power'].dBm()),
                         'amplifier':numpy.asscalar(result['amplifier']) })
                if not(onlyLimits):
                    row.update({'limit':(1 if result['limit'] else 0)})
                writer.writerow(row)
        if fileName:
            fileHandle.close()
        else:
            return fileHandle

        
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
        self.passCriterion = ExperimentSlot(parent=self) #,defaultValue='VoltageCriterion')
        self.transmittedPower = ExperimentSlot(parent=self) #,defaultValue='TransmittedPower')
        self.powerMinimum = Property(Power(-30.,'dBm'),changedSignal=self.settingsChanged)

        self.powerMaximum = Property(Power(+15.,'dBm'),changedSignal=self.settingsChanged)
        self.frequencies = SweepRange(Frequency(10e6),Frequency(4200e6),101,changedSignal=self.settingsChanged) 
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
        self.passCriterion.value.prepare()
        self.transmittedPower.value.prepare()

    def run(self):

        result = DpiResult(Power([self.powerMinimum.value,self.powerMaximum.value]),deepcopy(self.frequencies))
        self.emitResult(result)        
        
        guessPower = self.powerMinimum.value
        stepSizes = [5.0,1.0,0.5,.25] # dB

        def findFailureFromBelow(startPower,stepIndex=0):
            def measureAndSavePass(tryPower):
#                self.transmittedPower.value.rfGenerator._enableOutput(False)            
#                self.passCriterion.value.prepare()                  
                
                self.transmittedPower.value.generatorPower = tryPower                
                
                passData = {'injection frequency':frequency,
                             'limit':False}
                passData.update(self.transmittedPower.value.statusData())
                passData.update(self.passCriterion.value.measure())
                result.append( passData )
                return passData['pass']
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
                
        
        self.transmittedPower.value.rfGenerator._enableOutput(False)            
        self.passCriterion.value.prepare()        
        
        self.progressed.emit(0)
        for number,frequency in enumerate(self.frequencies.values):
            if self.stopRequested:
                break
            
            self.transmittedPower.value.rfGenerator._enableOutput(False) 
            self.transmittedPower.value.generatorFrequency = frequency
            log.LogItem('Passing to {frequency}'.format(frequency=frequency),log.debug)
            
#            self.transmittedPower.value.generatorPower = Power(0,'W')
           
#            self.passCriterion.value.prepare()
            
            guessPower = Power(findFailureFromBelow(guessPower).dBm() - stepSizes[0],'dBm')
            measurement = self.transmittedPower.value.measure()
            measurement.update({'limit':True})
            result.updateRow(-1,measurement)

            self.progressed.emit(int(float(number+1)/self.frequencies.numberOfPoints.value*100.))
            
        self.transmittedPower.value.tearDown()
        
        self.finished.emit()
        log.LogItem('Finished DPI',log.success)
        
        self.stopRequested = False
        

        
        
if __name__ == '__main__':
#    import copy
#    a = Dpi()
#    print a.powerMaximum.value
#    b = copy.deepcopy(a)
#    print b.powerMaximum.value
    from voltagecriterion import VoltageCriterion
    from transmittedpower import TransmittedPower
    
    
    log.LogModel.Instance().gui = False


    experiment = Dpi()
    result = None
    def catchResult(theNewResult):
        global result
        result = theNewResult
    experiment.newResult.connect(catchResult)
    experiment.frequencies.start.value = Frequency(10,'MHz')
    experiment.frequencies.stop.value = Frequency(1,'GHz')    
    experiment.frequencies.numberOfPoints.value = Integer(2)    
    
    experiment.passCriterion.value = VoltageCriterion
    experiment.transmittedPower.value = TransmittedPower

    experiment.connect()
    experiment.prepare()
    experiment.run()
    
    limitCsv = result._writeToCsv(fileName=None,onlyLimits=False)
    expectedFileContents = u'''frequency (Hz)	generator (dBm)	forward (dBm)	reflected (dBm)	transmitted (dBm)	fail	limit
10000000,0	-30,0	nan	nan	nan	0	0
10000000,0	-25,0	nan	nan	nan	0	0
10000000,0	-20,0	nan	nan	nan	0	0
10000000,0	-15,0	nan	nan	nan	0	0
10000000,0	-10,0	nan	nan	nan	0	0
10000000,0	-5,0	nan	nan	nan	0	0
10000000,0	0,0	nan	nan	nan	0	0
10000000,0	5,0	nan	nan	nan	0	0
10000000,0	10,0	nan	nan	nan	1	0
10000000,0	5,0	nan	nan	nan	0	0
10000000,0	6,0	nan	nan	nan	0	0
10000000,0	7,0	nan	nan	nan	0	0
10000000,0	8,0	nan	nan	nan	0	0
10000000,0	9,0	nan	nan	nan	1	0
10000000,0	8,0	nan	nan	nan	0	0
10000000,0	8,5	nan	nan	nan	0	0
10000000,0	9,0	nan	nan	nan	1	0
10000000,0	8,5	nan	nan	nan	0	0
10000000,0	8,75	7,25	1,26081122819	5,9900915638	1	1
1000000000,0	-30,0	nan	nan	nan	0	0
1000000000,0	-25,0	nan	nan	nan	0	0
1000000000,0	-20,0	nan	nan	nan	0	0
1000000000,0	-15,0	nan	nan	nan	0	0
1000000000,0	-10,0	nan	nan	nan	0	0
1000000000,0	-5,0	nan	nan	nan	0	0
1000000000,0	0,0	nan	nan	nan	0	0
1000000000,0	5,0	nan	nan	nan	0	0
1000000000,0	10,0	nan	nan	nan	1	0
1000000000,0	5,0	nan	nan	nan	0	0
1000000000,0	6,0	nan	nan	nan	0	0
1000000000,0	7,0	nan	nan	nan	0	0
1000000000,0	8,0	nan	nan	nan	0	0
1000000000,0	9,0	nan	nan	nan	1	0
1000000000,0	8,0	nan	nan	nan	0	0
1000000000,0	8,5	nan	nan	nan	0	0
1000000000,0	9,0	nan	nan	nan	1	0
1000000000,0	8,5	nan	nan	nan	0	0
1000000000,0	8,75	7,25	1,62669649888	5,8596715417	1	1
'''.replace('\n','\r\n')
    actualFileContents = limitCsv.getvalue()
    assert actualFileContents == expectedFileContents
#    for (actual,expected) in zip(actualFileContents,expectedFileContents):
#        if actual != expected:
#            print 'Err',ord(actual),ord(expected)
#            break
        