import numpy

from device import ScpiDevice
from oscilloscope import Oscilloscope

class Agilent86100a(Oscilloscope,ScpiDevice):
    defaultName = 'Agilent 86100A Oscilloscope'
    visaIdentificationStartsWith = 'Agilent Technologies,86100A,'
    documentation = {'Programmers Manual':'http://cp.literature.agilent.com/litweb/pdf/86100-90131.pdf'}
        
    def tryConnect(self):
        if super(Agilent86100a,self).tryConnect():
            firmwareString = self.askIdentify().split(',')[-1]
            assert firmwareString.startswith('A.')
            self.firmwareVersion = float(firmwareString[2:])
            assert self.firmwareVersion < 5.0
            
            # Prepare for downloading waveforms
            self.deviceHandle.timeout = 30.0
            #visa.vpp43.gpib_control_ren(self.deviceHandle, visa.VI_GPIB_REN_ASSERT_ADDRESS_LLO)
            return True
        else:
            return False

        
    def getChannelWaveform(self,channel,response=False):
        '''
        Acquire one waveform from a channel.
        
        @return 2xN array The first row contains the sample instants, the second
                row contains the values.
        '''
        if response:
            self.deviceHandle.write(':WAVeform:SOURce RESPonse%d' % channel)
        else:
            self.deviceHandle.write(':WAVeform:SOURce CHANnel%d' % channel)
        self.deviceHandle.write(':WAVeform:FORMat WORD')
        dataType = numpy.dtype('>i2')
        
        if response:
            self.deviceHandle.write(':DIGitize RESPonse%d' % channel)
        else:
            self.deviceHandle.write(':DIGitize Channel%d' % channel)
            self.deviceHandle.write(':CHANnel%d:DISPlay ON' % channel) # turn on channel display which is turned of by DIGitize

        
#         self.deviceHandle.write(':DIGitize CHAN%d' % channel) # essential!
#         #self.deviceHandle.write(':DIGitize')
#         self.deviceHandle.write(':WAVeform:SOURce CHANnel%d' % channel)
        
        rawData = self.deviceHandle.ask(':WAVeform:DATA?')
                
        # Extract useful data bytes
        assert rawData[0] == '#'
        numberOfLengthDigits = (int)(rawData[1])
        numberOfDataBytes = (int)(rawData[2:2+numberOfLengthDigits])
        
        if len(rawData) != 2+numberOfLengthDigits+numberOfDataBytes:
            print 'Received %d bytes, but expected %d' % (len(rawData),2+numberOfLengthDigits+numberOfDataBytes)
        rawDataArray = numpy.fromstring(rawData[2+numberOfLengthDigits:],
                                dtype=dataType)
        
        # Convert to real voltages
        def shiftAndScale(axisName,axisData):
            '''
            Request and apply oscilloscope axis shift and scale parameters.
            @param axisName Name of the axis (i.e. 'X' or 'Y')
            @param axisData Numpy array of points on this axis.
            '''
            increment = (float)(self.deviceHandle.ask(':WAVeform:%sINCrement?' % axisName))
            reference = (float)(self.deviceHandle.ask(':WAVeform:%sREFerence?' % axisName))
            origin = (float)(self.deviceHandle.ask(':WAVeform:%sORIgin?' % axisName))
            return ((axisData - reference)*increment) + origin

        # Construct sample instant array
        numberOfSamples = (int)(self.deviceHandle.ask(':WAVeform:POINts?'))
        sampleNumbers = numpy.arange(0,numberOfSamples)
        assert len(sampleNumbers) == len(rawDataArray)
        
        return numpy.vstack((shiftAndScale('X',sampleNumbers),
                            shiftAndScale('Y',rawDataArray)))
        
    
if __name__ == '__main__':
    from matplotlib import pyplot
    import time
    device = Agilent86100a()
    device.tryConnect()
    
    for iteration in range(1):
        #time.sleep(1)
        print iteration
        calibratedResponse = device.getChannelWaveform(1,response=True)
        rawSignal = device.getChannelWaveform(1)
#        signal2 = device.getChannelWaveform(2)
#         signal,signal2 = device.getChannelWaveforms()
        
        
    pyplot.plot(rawSignal[0,:],rawSignal[1,:],'b-')
    pyplot.plot(calibratedResponse[0,:],calibratedResponse[1,:],'r-')
    pyplot.show()



    
    