import numpy

from device import ScpiDevice
from oscilloscope import Oscilloscope

class Hp54520a(Oscilloscope,ScpiDevice):
    defaultName = 'HP 54520A Oscilloscope'
    visaIdentficationStartsWith = 'HEWLETT-PACKARD,54520A'
              
    def getChannelWaveform(self,channel):
        '''
        Acquire one waveform from a channel.
        
        @return 2xN array The first row contains the sample instants, the second
                row contains the values.
        '''
        #TODO: use DIGitize somewhere
        
        self.deviceHandle.write(':ACQuire:TYPE NORMal')
#        self.deviceHandle.write(':WAVeform:FORMat ASCII')
#        self.deviceHandle.write(':WAVeform:SOURce CHANnel%d' % channel)
#        return self.deviceHandle.ask_for_values(':WAVeform:DATA?',visa.ascii)
 
        self.deviceHandle.write(':WAVeform:FORMat WORD')
        dataType = numpy.dtype('>H')
        
        self.deviceHandle.write(':DIGitize CHAN%d' % channel) # essential!
        #self.deviceHandle.write(':DIGitize')
        self.deviceHandle.write(':WAVeform:SOURce CHANnel%d' % channel)
        rawData = self.deviceHandle.ask(':WAVeform:DATA?')
                
        # Extract useful data bytes
        assert rawData[0] == '#'
        numberOfLengthDigits = (int)(rawData[1])
        numberOfDataBytes = (int)(rawData[2:2+numberOfLengthDigits])
        
#        print rawData[:20]
#        print numberOfLengthDigits
#        print numberOfDataBytes
#
        #assert len(rawData) == 2+numberOfLengthDigits+numberOfDataBytes, 'Received %d bytes, but expected %d, received:\n%s' % (len(rawData),2+numberOfLengthDigits+numberOfDataBytes,rawData)
        if len(rawData) != 2+numberOfLengthDigits+numberOfDataBytes:
            print 'Received %d bytes, but expected %d, received:\n%s' % (len(rawData),2+numberOfLengthDigits+numberOfDataBytes,rawData)
            moreData = self.deviceHandle.read()
            print moreData
            print len(moreData)
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
        
    def getChannelWaveforms(self):
        '''
        Acquire all channel waveforms
        
        @return tuple of 2xN arrays The first row contains the sample instants, the second
                row contains the values.
        '''
        #TODO: use DIGitize somewhere
        
        self.deviceHandle.write(':ACQuire:TYPE NORMal')
#        self.deviceHandle.write(':WAVeform:FORMat ASCII')
#        self.deviceHandle.write(':WAVeform:SOURce CHANnel%d' % channel)
#        return self.deviceHandle.ask_for_values(':WAVeform:DATA?',visa.ascii)
 
        self.deviceHandle.write(':WAVeform:FORMat WORD')
        dataType = numpy.dtype('>H')
        
        
        self.deviceHandle.write('DISPlay:SCReen OFF')
        self.deviceHandle.write(':DIGitize CHANNEL1,CHANNEL2') # essential!
        #self.deviceHandle.write(':DIGitize')
        
        def getChannelData(channel):
            self.deviceHandle.write(':WAVeform:SOURce CHANnel%d' % channel)
            rawData = self.deviceHandle.ask(':WAVeform:DATA?')
                    
            # Extract useful data bytes
            assert rawData[0] == '#'
            numberOfLengthDigits = (int)(rawData[1])
            numberOfDataBytes = (int)(rawData[2:2+numberOfLengthDigits])
            
    #        print rawData[:20]
    #        print numberOfLengthDigits
    #        print numberOfDataBytes
    #
            #assert len(rawData) == 2+numberOfLengthDigits+numberOfDataBytes, 'Received %d bytes, but expected %d, received:\n%s' % (len(rawData),2+numberOfLengthDigits+numberOfDataBytes,rawData)
            if len(rawData) != 2+numberOfLengthDigits+numberOfDataBytes:
                print 'Received %d bytes, but expected %d, received:\n%s' % (len(rawData),2+numberOfLengthDigits+numberOfDataBytes,rawData)
                moreData = self.deviceHandle.read()
                print moreData
                print len(moreData)
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
        return getChannelData(1),getChannelData(2)
    
if __name__ == '__main__':
    from matplotlib import pyplot
    import time
    device = Hp54520a()
    assert device.tryConnect()
    
    
    for iteration in range(1):
        #time.sleep(1)
        print iteration
#        signal = device.getChannelWaveform(1)
#        signal2 = device.getChannelWaveform(2)
        signal,signal2 = device.getChannelWaveforms()
        
        
    pyplot.plot(signal[0,:],signal[1,:],'b.-')
    pyplot.plot(signal2[0,:],signal2[1,:],'r.-')
    pyplot.show()



    
    