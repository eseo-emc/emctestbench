from device import knownDevices
from experiment import Experiment,BooleanProperty,ScalarProperty,EnumerateProperty
from result.resultset import DictResult
from result import persistance
from utility import quantities
import time

from gui import log

class SupplyController(Experiment,persistance.Dommable):
    name = 'Supply Controller'
    def __init__(self):
        Experiment.__init__(self)
        self.outputVoltage = ScalarProperty(quantities.Voltage(3.3,'V'),changedSignal=self.settingsChanged,minimum=quantities.Voltage(0.,'V'),maximum=quantities.Voltage(20.,'V'))
        self.outputCurrent = ScalarProperty(quantities.Current(100,'mA'),changedSignal=self.settingsChanged,minimum=quantities.Current(0.,'A'),maximum=quantities.Current(10.,'A'))
        self.outputChannel = EnumerateProperty('1',['1','2','3','4'],changedSignal=self.settingsChanged)
        self.offOnTime = ScalarProperty(quantities.Time(0.5,'s'),minimum=quantities.Time(0.,'s'),maximum=quantities.Time(10.,'s'))
        self.startupTime = ScalarProperty(quantities.Time(0.5,'s'),minimum=quantities.Time(0.,'s'),maximum=quantities.Time(10.,'s'))
        self.outputOn = BooleanProperty(False,changedSignal=self.onOffChanged)
    def asDom(self,parent):
        element = persistance.Dommable.asDom(self,parent)
        self.appendChildObject(element,self.outputVoltage.value,'output voltage')
        self.appendChildObject(element,self.outputCurrent.value,'output current limit')
        self.appendChildObject(element,self.outputChannel.value,'output channel')
        self.appendChildObject(element,self.offOnTime.value,'off/on time')
        self.appendChildObject(element,self.startupTime.value,'startup time')
         
        return element
        
    def connect(self):
        self.supply = knownDevices['powerSupply']
    def settingsChanged(self):
        outputWasOn = self.outputOn.value
        self.outputOn.value = False
        self.supply.setChannelParameters( \
            self.outputChannel.value,
            self.outputVoltage.value,
            self.outputCurrent.value)
        self.outputOn.value = outputWasOn
        
    def onOffChanged(self):
        if self.outputOn.value:
            self.supply.turnChannelOn(self._channelNumber)
        else:
            self.supply.turnChannelOff(self._channelNumber)
            
    @property
    def _channelNumber(self):
        return int(self.outputChannel.value)
    def _turnOn(self):
        self.outputOn.value = True
        time.sleep(self.startupTime.value)
    def _turnOff(self):
        self.outputOn.value = False
        time.sleep(self.offOnTime.value)
#        
    def prepare(self):
        self._turnOn()
#        self.undisturbedOutputVoltage.value = self.measure()['voltage']
#        log.LogItem('Acquired undisturbed voltage: {:.6f} V'.format(self.undisturbedOutputVoltage.value.asUnit('V')),log.debug)
    def measure(self):
        result = DictResult()
        result.data = {'current':self.supply.getCurrent(self._channelNumber),
                       'voltage':self.supply.getVoltage(self._channelNumber)}
        self.emitResult(result)
        return result
    def run(self):
        self.measure()
        
    def interrupt(self):
        self._turnOff()
        self._turnOn()
    def tearDown(self):
        self._turnOff()
        
        
if __name__ == '__main__':
    experiment = SupplyController()
    experiment.connect()
    
    experiment.offOnTime.value = quantities.Time(3.0)
    experiment.startupTime.value = quantities.Time(2.0)
    experiment.outputVoltage.value = quantities.Voltage(3.3)    
    
    experiment.prepare()
    experiment.interrupt()
    print experiment.measure().data
    experiment.tearDown()
