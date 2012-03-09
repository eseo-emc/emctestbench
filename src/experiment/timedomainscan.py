"""
Quick test to scan a step response along the X-axis in nearfield

Manual:
- connect channel 1 to DUT
- configure the TDT to measure the probe step response on channel 2
- power the preamp from channel 4 of the N6700B

preamp
http://www.everythingrf.com/rf-microwave-amplifiers/p/Planar-Monolithics-Industries-82_PEC_60_0R14R0_5R0_10_12_SFF

@author: Sjoerd Op 't Land
"""
import numpy
import time
from matplotlib import pyplot


import device
# from utility.quantities import Amplitude


import os
import datetime

class NearFieldMode:
    def __init__(self):
        self.oscilloscope = device.Agilent86100a()
        self.robot = device.NewportEsp300()
        
        self.powerSupply = device.AgilentN6700b()
        self.powerSupply.setChannelParameters(4,12.0,0.45)
        

    def xSweep(self):
        self.powerSupply.turnChannelOn(4)
        
        xRange = numpy.arange(50,235,5) #(0,20,10) #
#         xRange = numpy.hstack((xRange,xRange[::-1]))
        moments = []
        voltages = []
        for xPosition in xRange:
            print xPosition
            self.robot.setLocation(xPosition)
            waveform = self.oscilloscope.getChannelWaveform(2)
            moments = waveform[0,:]
            voltages.append(waveform[1,:])
                            
        self.powerSupply.turnChannelOff(4)        
        
        return (xRange,moments,numpy.vstack(voltages))
        
 
if __name__ == '__main__':
    print 'Start mode scan'
    test = NearFieldMode()
    (xRange,moments,voltages) = test.xSweep()

## plot at time instant n
theFigure = pyplot.figure()
theAxes = theFigure.add_subplot(111)
yLimits = (numpy.min(voltages),numpy.max(voltages))

safeDateString = datetime.datetime.isoformat(datetime.datetime.now()).replace(':','')
# safeDateString = '2'
imageDirectory = '../results/TDT%s' % safeDateString
os.makedirs(imageDirectory)

for timeIndex in numpy.arange(0,moments.size,5):
    theAxes.cla()
    
    fileName = '%s/%05d.png' % (imageDirectory,timeIndex)

    print 'Saving frame', fileName
    relativeMoment = moments[timeIndex]-moments[0]
    pyplot.title('50 Ohms terminated line at %d ps' % (relativeMoment/1e-12))
    pyplot.plot(xRange,voltages[:,timeIndex])
    pyplot.ylabel('Voltage at TDT input (V)')
    pyplot.xlabel('Position (mm)')
    pyplot.ylim(yLimits)
#     theFigure.show()
    theFigure.savefig(fileName)

# ## measure waveform
# waveform = test.oscilloscope.getChannelWaveform(2)
# pyplot.plot(abs(waveform[0,:]),numpy.abs(waveform[1,:]))
# pyplot.ylabel('Voltage at TDT input (V)')
# pyplot.xlabel('Time (s)')
# pyplot.show()

# ## show magnitude
# pyplot.plot(abs(voltages[0,:]),numpy.abs(voltages[1,:]))
# pyplot.ylabel('Voltage at VSA input (V)')
# pyplot.xlabel('x position (mm)')
#  
# pyplot.show()
# 
# ## show phase
# pyplot.plot(abs(voltages[0,:]),numpy.rad2deg(numpy.angle(voltages[1,:])))
# pyplot.ylabel('Phase (degrees)')
# pyplot.xlabel('x position (mm)')
# pyplot.show()