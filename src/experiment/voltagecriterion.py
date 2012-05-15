from device import knownDevices
from experiment import Experiment,Property
from result.resultset import DictResult
from result import persistance

class VoltageCriterion(Experiment,persistance.Dommable):
    name = 'Voltage offset criterion'
    def __init__(self):
        Experiment.__init__(self)
        self.undisturbedOutputVoltage = Property(0.,changedSignal=self.settingsChanged)
        self.voltageMargin = Property(0.1,changedSignal=self.settingsChanged)
#        self.laresult = Result(self,0.)
    def asDom(self,parent):
        element = persistance.Dommable.asDom(self,parent)
        self.appendChildObject(element,self.undisturbedOutputVoltage.value,'Undisturbed Output Voltage')
        self.appendChildObject(element,self.voltageMargin.value,'Voltage Margin')        
        return element
        
    def connect(self):
        self.voltMeter = knownDevices['multimeter']
    def prepare(self):
        self.undisturbedOutputVoltage.value = self.measure()['Voltage']
    def measure(self):
        #        result = ScalarResult()
        outputVoltage = self.voltMeter.measure()
#        result.data = outputVoltage
        result = DictResult()
        result.data = {'Pass':abs(outputVoltage -self.undisturbedOutputVoltage.value) <= self.voltageMargin.value,
                'Voltage':outputVoltage}
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
