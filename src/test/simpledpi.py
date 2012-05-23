from device import Device
from device.multimeter import Multimeter
from device.rfgenerator import RfGenerator
from device.wattmeter import WattMeter
from device.switch import SwitchPlatform
from utility.quantities import Power,PowerRatio,Voltage
from calibration.bridge import bridgeInsertionTransferAt,bridgeCouplingFactorAt
import time
from random import gauss

class DummyMultimeter(Multimeter,Device):
    defaultName = 'Dummy Multimeter'
    standardDeviation = 0.01
    def __init__(self,rfGenerator,switchPlatform):
        self.rfGenerator = rfGenerator
        self.switchPlatform = switchPlatform
        Device.__init__(self)
    def measure(self):
        time.sleep(0.1)
        if incidentPower() > Power(+7.1,'dBm'):
            return Voltage(gauss(4.7,self.standardDeviation),'V')
        else:
            return Voltage(gauss(4.9,self.standardDeviation),'V')

class DummyRfGenerator(RfGenerator,Device):
    defaultName = 'Dummy RF Generator'
    def __init__(self):
        self._power = Power(-130.,'dBm')
        self._enableOutput = False
        self._frequency = 300e3
        Device.__init__(self)
    def setPower(self,newPower):
        self._power = newPower
    def setFrequency(self,newFrequency):
        self._frequency = newFrequency
    def getFrequency(self):
        return self._frequency
    def enableOutput(self,enable=True):
        self._enableOutput = enable
    def getOutputEnable(self):
        if self._enableOutput:
            return 1.0
        else:
            return 0.0   
    def getPower(self):
        return self._power * self.getOutputEnable()

class DummySwitchPlatform(SwitchPlatform,Device):
    defaultName = 'Dummy Switchplatform'
    def __init__(self):

        self.preset = ''
        Device.__init__(self)
    def setPreset(self,presetName):
        self.preset = presetName
    @property
    def valid(self):
        if self.preset == 'bridge':
            return 1.0
        else:
            return 0.0
    def checkPreset(self,presetName):
        return self.preset == presetName
        
class DummyWattMeter(WattMeter,Device):
    defaultName = 'Dummy Wattmeter'
    def putOnline(self):
        time.sleep(.5)
        self.online = True
    
    def __init__(self,rfGenerator,switchPlatform):
        Device.__init__(self)
        WattMeter.__init__(self)
        self.rfGenerator = rfGenerator
        self.switchPlatform = switchPlatform
        self._wasReset = 0.0

    def reset(self):
        self._wasReset = 1.0
    def getPower(self,channel=None):
        time.sleep(.5)
        channel1Power = Power(0,'W') *self._wasReset
        channel2Power = reflectedPower()*self._wasReset
        if channel == 1:
            return channel1Power
        elif channel == 2:
            return channel2Power
        else:
            return (channel1Power,channel2Power)
        

rfGenerator = DummyRfGenerator()
switchPlatform = DummySwitchPlatform()
switchPlatform.setPreset('bridge')
knownDevices = { \
    'multimeter' : DummyMultimeter(rfGenerator,switchPlatform),
    'rfGenerator' : rfGenerator,
    'wattMeter' : DummyWattMeter(rfGenerator,switchPlatform),
    'switchPlatform' : switchPlatform \
}

def incidentPower():
    assert switchPlatform.preset == 'bridge'
    return rfGenerator.getPower() * bridgeInsertionTransferAt(rfGenerator.getFrequency())
def reflectedPower():
    assert switchPlatform.preset == 'bridge'
    return incidentPower() * PowerRatio(-6,'dB') * bridgeCouplingFactorAt(rfGenerator.getFrequency())