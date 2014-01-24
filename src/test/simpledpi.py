from device import Device
from device.multimeter import Multimeter
from device.rfgenerator import RfGenerator
from device.wattmeter import WattMeter
from device.switch import SwitchPlatform
from device.positioner import Positioner
from device.spectrumanalyzer import SpectrumAnalyzer
from utility.quantities import Power,PowerRatio,Voltage,Position
from calibration.bridge import bridgeInsertionTransferAt,bridgeCouplingFactorAt
import time
from random import gauss
import numpy

slow = False

class DummyMultimeter(Multimeter,Device):
    defaultName = 'Dummy Multimeter'
    standardDeviation = 0.00000001
    def __init__(self,rfGenerator,switchPlatform):
        self.rfGenerator = rfGenerator
        self.switchPlatform = switchPlatform
        Device.__init__(self)
    def measure(self):
        if slow:
            time.sleep(0.1)
        if incidentPower() > Power(+7.1,'dBm'):
            return Voltage(gauss(4.7,self.standardDeviation),'V')
        else:
            return Voltage(gauss(4.9,self.standardDeviation),'V')

class DummyRfGenerator(RfGenerator,Device):
    defaultName = 'Dummy RF Generator'
    def __init__(self):
        self._power = Power(-130.,'dBm')
        self._outputEnabled = False
        self._frequency = 300e3
        Device.__init__(self)

    def setPower(self,newPower):
        self._power = newPower
        if newPower.negligible:
            self._enableOutput(False)
        else:
            self._enableOutput(True)
    def setFrequency(self,newFrequency):
        self._frequency = newFrequency
    def getFrequency(self):
        return self._frequency
    def _enableOutput(self,enable=True):
        self._outputEnabled = enable
    def getOutputEnable(self):
        if self._outputEnabled:
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
        if slow:
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
        if slow:
            time.sleep(.5)
        channel1Power = Power(0,'W') *self._wasReset
        channel2Power = reflectedPower()*self._wasReset
        if channel == 1:
            return channel1Power
        elif channel == 2:
            return channel2Power
        else:
            return (channel1Power,channel2Power)
        
class DummyPositioner(Positioner,Device):
    defaultName = 'Dummy Positioner'    
    
    def __init__(self):
        Device.__init__(self)
        Positioner.__init__(self)
        self._position = None
    def prepare(self):
        self._position = Position([42,42,42],'mm')
    def tearDown(self):
        pass
    def setLocation(self,position):
        if slow:
            time.sleep(numpy.linalg.norm(position-self._position)/0.1)
        self._position = position
        return self.getLocation()
    def getLocation(self):
        return self._position
    
class DummySpectrumAnalyzer(SpectrumAnalyzer,Device):
    defaultName = 'Dummy Spectrum Analyzer'
    
    def __init__(self,rfGenerator,positioner):
        SpectrumAnalyzer.__init__(self)
        Device.__init__(self)
        
        self.rfGenerator = rfGenerator
        self.positioner = positioner
    def reset(self):
        pass
    def powerAt(self,frequency):
        noiseFloor = Power(-35,'dBm')
        if frequency == self.rfGenerator.getFrequency():
            halfTraceWidth = Position(2.0,'mm')
            sincPhase = numpy.pi * self.positioner.getLocation()[1] / halfTraceWidth
            if sincPhase == 0:
                sincPhase = 0.001
            return noiseFloor + incidentPower()*(numpy.sin(sincPhase)/sincPhase)**2
        else:
            return noiseFloor

rfGenerator = DummyRfGenerator()
switchPlatform = DummySwitchPlatform()
#switchPlatform.setPreset('bridge')
positioner = DummyPositioner()
knownDevices = { \
    'multimeter' : DummyMultimeter(rfGenerator,switchPlatform),
    'rfGenerator' : rfGenerator,
    'wattMeter' : DummyWattMeter(rfGenerator,switchPlatform),
    'switchPlatform' : switchPlatform, \
    'positioner' : positioner, \
    'spectrumAnalyzer0' : DummySpectrumAnalyzer(rfGenerator,positioner) \
}

def incidentPower():
    assert switchPlatform.preset == '86205A'
    return rfGenerator.getPower() * PowerRatio(-1.5,'dB') #* bridgeInsertionTransferAt(rfGenerator.getFrequency())
def reflectedPower():
    assert switchPlatform.preset == '86205A'
    return incidentPower() * PowerRatio(-6,'dB') * PowerRatio(-16,'dB') #* bridgeCouplingFactorAt(rfGenerator.getFrequency())