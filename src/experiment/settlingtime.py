"""
Created on 11 janv. 2011
Quick test to measure the settling time of the Prana amplifier

@author: Sjoerd Op 't Land
"""
import numpy
import time
from matplotlib import pyplot


import device
from utility.quantities import Amplitude


class SettlingTime:
    frequency = 900e6
        
    def __init__(self):
        self.wattMeter = device.AgilentE4419b()
        self.spectrumAnalyser = device.Hp8591a()
        self.generator = device.AgilentN5181a()

    def powerSweep(self,startPower,stopPower):
        startTime = time.clock()
        sampleTime = numpy.array([])
        inputPower = numpy.array([])
        outputPower = numpy.array([])
        
        stepStimulus = numpy.array([numpy.arange(-80,-20,12),-20*numpy.ones(5)]).flatten(1)
        
        for dBmPower in numpy.concatenate((stepStimulus,stepStimulus,stepStimulus,stepStimulus,stepStimulus,stepStimulus,stepStimulus,stepStimulus,stepStimulus)):
            self.generator.setWaveform(SettlingTime.frequency,Amplitude(dBmPower,'dBm'))
            self.generator.enableOutput(True)
            
            for powerSample in range(20):
                currentOutputPower = self.wattMeter.getPower('A')
                #currentOutputPower = self.spectrumAnalyser.powerAt(SettlingTime.frequency)
                outputPower = numpy.append(outputPower,currentOutputPower.dBm())
                sampleTime = numpy.append(sampleTime,time.clock()-startTime)
                inputPower = numpy.append(inputPower,float(dBmPower))
                
        self.generator.enableOutput(False)
        
        sampleTime.size
        
        return numpy.vstack((sampleTime,inputPower)),numpy.vstack((sampleTime,outputPower))

            
if __name__ == '__main__':
    print 'Start settling time test'
    test = SettlingTime()
    inputPowers,outputPowers = test.powerSweep(-20,0)
    
    
    pyplot.plot(inputPowers[0,:],inputPowers[1,:],'b.-',label='Input power')
    pyplot.plot(outputPowers[0,:],outputPowers[1,:]-23.,'r.-',label='Output power-23dB')
    
    pyplot.title('Prana at 900 MHz with 20 dB attenuator (spectrum analyser)')
    pyplot.xlabel('Time (s)')
    pyplot.ylabel('Power (dBm)')
    pyplot.legend()
    
    pyplot.show()