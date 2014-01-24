from device import knownDevices
from experiment import Experiment,Property,ScalarProperty
from result.resultset import DictResult
from result import persistance
from utility import quantities

from gui import log

class VoltageCriterion(Experiment,persistance.Dommable):
    name = 'Voltage offset criterion'
    def __init__(self):
        Experiment.__init__(self)
        self.undisturbedOutputVoltage = ScalarProperty(quantities.Voltage(0.,'V'),changedSignal=self.settingsChanged,minimum=quantities.Voltage(-500.,'V'),maximum=quantities.Voltage(500.,'V'))
        self.voltageMargin = ScalarProperty(quantities.Voltage(200.,'uV'),changedSignal=self.settingsChanged,minimum=quantities.Voltage(0.,'V'),maximum=quantities.Voltage(500.,'V'))
    def asDom(self,parent):
        element = persistance.Dommable.asDom(self,parent)
        self.appendChildObject(element,self.undisturbedOutputVoltage.value,'undisturbed output voltage')
        self.appendChildObject(element,self.voltageMargin.value,'voltage margin')        
        return element
        
    def connect(self):
        self.voltMeter = knownDevices['multimeter']
    def prepare(self):
        self.undisturbedOutputVoltage.value = self.measure()['voltage']
        log.LogItem('Acquired undisturbed voltage: {:.6f} V'.format(self.undisturbedOutputVoltage.value.asUnit('V')),log.debug)
    def measure(self):
        #        result = ScalarResult()
        outputVoltage = self.voltMeter.measure()
#        result.data = outputVoltage
        result = DictResult()
        result.data = {'pass':abs(outputVoltage -self.undisturbedOutputVoltage.value) <= self.voltageMargin.value,
                'voltage':outputVoltage}
#        self.result.value = {'pass':abs(outputVoltage -self.undisturbedOutputVoltage.value) <= self.voltageMargin.value,
#                'outputVoltage (V)':outputVoltage}
        self.emitResult(result)
        return result
    def run(self):
        self.measure()
        
        
        
if __name__ == '__main__':
    experiment = VoltageCriterion()
    experiment.connect()
    experiment.prepare()
    print experiment.measure().data
