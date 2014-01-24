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
from utility import quantities


import device
# from utility.quantities import Amplitude


import os
import datetime

class NearFieldMode:
    def __init__(self):
        self.oscilloscope = device.agilent86100a.Agilent86100a()
        self.robot = device.newportesp300.NewportEsp300()
        
        self.powerSupply = device.agilentn6700b.AgilentN6700b()
        self.powerSupply.setChannelParameters(3,12.0,0.8)
        

    def sweep(self):
        self.powerSupply.turnChannelOn(3)
        
        xRange = numpy.arange(50,235,5) #(0,20,10) #
        yRange = numpy.arange(25,35,5)
        zPosition = 10
        moments = []
        voltages = []
        for xPosition in xRange:
            for yPosition in yRange:
                print [xPosition,yPosition,zPosition]
                self.robot.setLocation(quantities.Position([xPosition,yPosition,zPosition], 'mm'))
                waveform = self.oscilloscope.getChannelWaveform(2)
                moments = waveform[0,:]
                voltages.append(waveform[1,:])
                            
        self.powerSupply.turnChannelOff(3)        
        
        return ([xRange,yRange,zPosition],moments,numpy.vstack(voltages))
        
 
if __name__ == '__main__':
    print 'Start mode scan'
    test = NearFieldMode()
    ([xRange,yRange,zPosition],moments,voltages) = test.sweep()

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