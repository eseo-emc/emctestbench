"""
Quick test to plot rectification as function of frequency.

@author: Sjoerd Op 't Land
"""
import numpy
import time
from matplotlib import pyplot


import device
from utility.quantities import Amplitude


class Rectification:
    def __init__(self):
        self.voltMeter = device.AgilentL4411a()
        self.generator = device.AgilentN5181a()

    def powerSweep(self,frequency):
        self.generator.setWaveform(frequency,Amplitude(-110.,'dBm'))
        self.generator.enableOutput(True)
        
        powerRange = numpy.arange(-10,+19,2)
        dcVoltages = []
        for powerSample in powerRange:
            self.generator.setWaveform(frequency,Amplitude(powerSample,'dBm'))
            time.sleep(1)
            dcVoltages.append(self.voltMeter.voltage())
                
        self.generator.enableOutput(False)
        return numpy.vstack((powerRange,dcVoltages))
        
 
if __name__ == '__main__':
    print 'Start settling time test'
    test = Rectification()
    
    
    def plotSweep(frequency,lineSpecification):
        dcVoltages = test.powerSweep(frequency*1e6)
        pyplot.plot(dcVoltages[0,:],dcVoltages[1,:],lineSpecification,label='%d MHz' % frequency)
        
    plotSweep(10,'k-')
    time.sleep(5)
    plotSweep(100,'k--')
    time.sleep(5)
    plotSweep(200,'k-.')
    time.sleep(5)
    plotSweep(500,'k:')

    pyplot.legend()
    
    pyplot.ylabel('DC Voltage (V)')
    pyplot.xlabel('Power (dBm)')
     
    pyplot.show()