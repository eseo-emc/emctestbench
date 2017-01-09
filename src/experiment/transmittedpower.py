from device import knownDevices
from utility.quantities import Power,Frequency
from experiment import Experiment,EnumerateProperty
from result import persistance
from copy import copy


from calibration.bench import BestBenchCorrections

from result.resultset import DictResult

class TransmittedPower(Experiment,persistance.Dommable):
    name = 'Transmitted Power Calculation'
    
    def __init__(self):
        Experiment.__init__(self)
        persistance.Dommable.__init__(self)

        self._physicalAmplifier = None
        
        self.amplifierSwitchPositions = {
            'None (773D)':                  'coupler', 
            'Amplifier 1 (Prana)':          'Amplifier 1', 
            'Amplifier 2 (Milmega band 1)': 'Amplifier 2', 
            'Amplifier 2 (Milmega band 2)': 'Amplifier 2'}
        self.amplifierDevices = {
            'None (773D)':                  None, 
            'Amplifier 1 (Prana)':          knownDevices['Prana'], 
            'Amplifier 2 (Milmega band 1)': knownDevices['Milmega'], 
            'Amplifier 2 (Milmega band 2)': knownDevices['Milmega']}
            
        self.amplifier = EnumerateProperty('Automatic (coupler)',['Automatic (coupler)','Automatic (amplifier)'] + self.amplifierSwitchPositions.keys())
        self.amplifier.changed.connect(self.setAmplifier)

        self.amplifierCorrections = {}        
        for amplifier in self.amplifierSwitchPositions.keys():
            self.amplifierCorrections.update({amplifier:BestBenchCorrections(amplifier)})
    
    def connect(self):
        self.wattMeter = knownDevices['wattMeter']
        self.rfGenerator = knownDevices['rfGenerator']
        
        self.switchPlatform = knownDevices['switchPlatform']
        self.physicalAmplifier = 'None (773D)'        
        
        self.setAmplifier()

    def prepare(self):
        self.wattMeter.reset()
    
    @property
    def generatorFrequency(self):
        return self.rfGenerator.getFrequency()
    @generatorFrequency.setter
    def generatorFrequency(self,value):
        self.rfGenerator.setFrequency(value)
        self.setAmplifier()
    
    @property
    def generatorPower(self): 
        return self.rfGenerator.getPower()
    @generatorPower.setter
    def generatorPower(self,newPower):    
        self.rfGenerator.setPower(newPower)
        if self.physicalAmplifier and not self.physicalAmplifier.startswith('None'):
            self.amplifierDevices[self.physicalAmplifier].rfOn = not(newPower.negligible)
    
    def setAmplifier(self):
        if self.amplifier.value == 'Automatic (coupler)':
            frequency = self.generatorFrequency
#            if frequency <= Frequency(2,'GHz'):
#                self.physicalAmplifier = 'None (86205A)'
#            else:
            self.physicalAmplifier = 'None (773D)'
        elif self.amplifier.value == 'Automatic (amplifier)':
            frequency = self.generatorFrequency
            if frequency <= Frequency(1,'GHz'):
                self.physicalAmplifier = 'Amplifier 1 (Prana)'
            elif frequency <= Frequency(2,'GHz'):
                self.physicalAmplifier = 'Amplifier 2 (Milmega band 1)'
            else:
                self.physicalAmplifier = 'Amplifier 2 (Milmega band 2)'
        else:
            self.physicalAmplifier = self.amplifier.value
            
    @property
    def physicalAmplifier(self):
        if self._physicalAmplifier:
            correctPosition = self.amplifierSwitchPositions[self._physicalAmplifier]
            assert self.switchPlatform.checkPreset(correctPosition),'The switch platform is not in the {position} position'.format(position=correctPosition)
        return self._physicalAmplifier   
    @physicalAmplifier.setter         
    def physicalAmplifier(self,newAmplifierName):
        if self.physicalAmplifier == newAmplifierName:
            return
        
        oldPower = self.generatorPower
        self.generatorPower = Power(0,'W')
        
        self.switchPlatform.setPreset(self.amplifierSwitchPositions[newAmplifierName])
        if newAmplifierName == 'Amplifier 2 (Milmega band 1)':
            self.amplifierDevices[newAmplifierName].switchToBand1()
        elif newAmplifierName == 'Amplifier 2 (Milmega band 2)':
            self.amplifierDevices[newAmplifierName].switchToBand2()
        
        self._physicalAmplifier = newAmplifierName
        self.generatorPower = oldPower

        
    def statusData(self):
        return {'amplifier':self.physicalAmplifier,
                'generator power':self.rfGenerator.getPower()}
        
    def measure(self):
        result = DictResult()  
        result.data = self.statusData()
        generatorPower = result.data['generator power']
        physicalAmplifier = result.data['amplifier']
        
        frequency = self.rfGenerator.getFrequency()        
          
        (forwardPowerReadout,reflectedPowerReadout) = self.wattMeter.getPower()
        
        reflectedImage = reflectedPowerReadout        
        if physicalAmplifier.startswith('None'):
            forwardImage = generatorPower
        else:
            forwardImage = forwardPowerReadout

        (forwardCorrection,reflectedCorrection) = self.amplifierCorrections[physicalAmplifier].corrections(frequency)                
            
        forwardPower = forwardImage * forwardCorrection
        reflectedPower = reflectedImage * reflectedCorrection


        result.data.update({'forward power image':forwardImage,
                       'reflected power image':reflectedPowerReadout,
                       'forward power':forwardPower,
                       'reflected power':reflectedPower,
                       'transmitted power':forwardPower-reflectedPower,
                       'reflection coefficient':reflectedPower/forwardPower})
        self.emitResult(result)
        return result
        

    def run(self):
        self.measure()  
    def tearDown(self):
        self.generatorPower = Power(0)    
        
            
#    def tryTransmittedPower(self,nominalPower):
#        generatorMaximum = Power(20,'dBm')
#        tryForwardPower = copy(nominalPower)
#        for tryNumber in range(4):
##            print tryForwardPower
#            self.rfGenerator.setPower(tryForwardPower)
#            self.rfGenerator.enableOutput()
#            realTransmittedPower = self.measure()['transmitted power']
#            realTransmittedPower = realTransmittedPower.max(Power(-40,'dBm'))
#
#            gain = nominalPower/realTransmittedPower
#
#            tryForwardPower *= gain
#            tryForwardPower = tryForwardPower.min(generatorMaximum)
#
#        return self.measure()['transmitted power']

        
    
if __name__ == '__main__':
    experiment = TransmittedPower()
    experiment.connect()
    experiment.prepare()
#    experiment.switchPlatform.setPreset('bridge')
#    print experiment.tryTransmittedPower(Power(0,'dBm'))
    experiment.amplifier.setValue('None (773D)')
    experiment.generatorFrequency = Frequency(150000,'Hz')
    experiment.generatorPower = Power(-60,'dBm')
#    experiment.rfGenerator.enableOutput()
    
    print experiment.measure()
