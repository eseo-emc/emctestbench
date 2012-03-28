import numpy
import time
from matplotlib import pyplot


import device
from utility.quantities import Amplitude,Power
from transmittedpower import TransmittedPower


class JitterInjection(object):
    '''
    Manual steps: 
        route and amplify the signal from the RF generator. 
        correctly set the input impedance of the jitter meter
        set-up the LF input signal
    '''
    def __init__(self):
        self.jitterMeter = device.Agilent86100a()
        #device.Agilent53220a('TCPIP0::172.20.1.206::inst0::INSTR')        
        assert self.jitterMeter.tryConnect()

        self.transmittedPower = TransmittedPower()
        self.rfGenerator = self.transmittedPower.rfGenerator
        self.switchPlatform = self.transmittedPower.switchPlatform
        
        self.switchPlatform.setPreset('bridge')

    def frequencySweep(self,frequencies,transmittedTargetPower):
        startTime = time.clock()
        rmsJitters = numpy.array([])
        transmittedPowers = numpy.array([])
       
        
        for frequency in frequencies:
            self.rfGenerator.setFrequency(frequency)
            attainedTransmittedPower = self.transmittedPower.tryTransmittedPower(transmittedTargetPower)
            transmittedPowers = numpy.append(transmittedPowers,attainedTransmittedPower)
            
            jitter = self.jitterMeter.measureJitter()
            print 'f={frequency:.2e}'.format(frequency=frequency)
            rmsJitters = numpy.append(rmsJitters,jitter)
#            peakToPeakJitters = numpy.append(peakToPeakJitters,jitter[1])
                
        self.rfGenerator.enableOutput(False)
        backgroundJitter = self.jitterMeter.measureJitter()
        
        return rmsJitters,backgroundJitter,transmittedPowers

            
if __name__ == '__main__':
    print JitterInjection.__doc__
    test = JitterInjection()
    frequencies = numpy.arange(90e6,3e9,50e6)
    (rmsJitters,backgroundJitter,transmittedPowers) = test.frequencySweep(frequencies,Power(.01,'W'))
    
    pyplot.plot(frequencies,rmsJitters*1e12,label='RMS Jitter')
#    pyplot.plot(frequencies,peakToPeakJitters,label='Peak to peak Jitter')
    pyplot.plot([frequencies[0],frequencies[-1]],[backgroundJitter*1e12,backgroundJitter*1e12],label='Background RMS jitter')
    
#    pyplot.title('Prana at 900 MHz with 20 dB attenuator (spectrum analyser)')
    pyplot.xlabel('Perturbation frequency (Hz)')
    pyplot.ylabel('Jitter (ps)')
    pyplot.legend()
    pyplot.show()
    
    pyplot.plot(frequencies,transmittedPowers)
    pyplot.xlabel('Frequency (Hz)')
    pyplot.ylabel('Transmitted power (W)')    
    pyplot.show()
    
    from utility.metaarray import MetaArray,axis
    resultArray = MetaArray((len(frequencies),2), info=[
                    axis('Frequency', values=frequencies, units='Hz',title='Time'), 
                    axis('Measurement', cols=[('j', 'ps', 'RMS jitter'),('P_trans', 'W', 'Transmitted power')])
                    ])

    resultArray['Measurement':'j'] = rmsJitters
    resultArray['Measurement':'P_trans'] = transmittedPowers
    resultArray.writeToExcel('Y:/emctestbench/results/jitter/jitterC1.xls')