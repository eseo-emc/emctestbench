"""
Quick test to scan a single tone along the X-axis in nearfield

Manual:
- power on the preamp (12V/0.5A)
- route the preamp to the VSA
- set the VSA to basic I/Q
- center the VSA on the tone

preamp
http://www.everythingrf.com/rf-microwave-amplifiers/p/Planar-Monolithics-Industries-82_PEC_60_0R14R0_5R0_10_12_SFF

@author: Sjoerd Op 't Land
"""
import numpy
import time
from matplotlib import pyplot


import device
from utility.quantities import Amplitude
import device

class NearFieldMode:
    def __init__(self):
        self.analyser = device.AgilentN9010a()
        self.robot = device.NewportEsp300()
        
        self.powerSupply = device.AgilentN6700b()
        self.powerSupply.setChannelParameters(4,12.0,0.45)
        
        self.switchPlatform = device.AgilentL4490a()
        self.switchPlatform.closeSwitch('DUTtoSAorVNA')
        

    def xSweep(self):
        self.powerSupply.turnChannelOn(4)
        self.analyser.align()
        
        xRange = numpy.arange(115.,0,-10)
        xRange = numpy.hstack((xRange,xRange[::-1]))
        complexVoltages = []
        for xPosition in xRange:
            
            print xPosition
            self.robot.setLocation(xPosition)
            self.analyser.waitUntilReady()
            time.sleep(1)
            complexVoltages.append(self.analyser.averageComplexVoltage())
                
        self.powerSupply.turnChannelOff(4)        
        
        return numpy.vstack((xRange,complexVoltages))
        
 
if __name__ == '__main__':
    print 'Start mode scan'
    test = NearFieldMode()
    voltages = test.xSweep()
## show magnitude
pyplot.plot(abs(voltages[0,:]),numpy.abs(voltages[1,:]))
pyplot.ylabel('Voltage at VSA input (V)')
pyplot.xlabel('x position (mm)')
 
pyplot.show()

## show phase
pyplot.plot(abs(voltages[0,:]),numpy.rad2deg(numpy.angle(voltages[1,:])))
pyplot.ylabel('Phase (degrees)')
pyplot.xlabel('x position (mm)')
pyplot.show()