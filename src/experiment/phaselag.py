# -*- coding:utf-8 -*-
"""
Created on 11 janv. 2011

@author: Administrateur
"""
import device
import numpy

class PhaseLag:
    '''
    Experiment that determines the phase shift of oscilloscope channel 2 with
    respect to channel 1
    '''
    
    def __init__(self):
        self.device = device.Hp54520a()
        
    def measurePhaseAndFrequency(self):
        # Capture and display waveforms
#        referenceSignal = self.device.getChannelWaveform(1)
#        dividerOutput = self.device.getChannelWaveform(2)
        referenceSignal,dividerOutput = self.device.getChannelWaveforms()
    #    pyplot.plot(referenceSignal[0,:],referenceSignal[1,:],'b',dividerOutput[0,:],dividerOutput[1,:],'r')
    #    pyplot.show()
        return calculatePhaseAndFrequency(referenceSignal,dividerOutput)
        

def calculatePhaseAndFrequency(referenceSignal,dividerOutput):
    '''
    Find the phase of dividerOutput with respect to referenceSignal, as well as 
    the average frequency of both signals.
    @param timeSignal 2xN array (sample instants and values)
    @param dividerOutput 2xN array (sample instants and values)
    @return phaseShift,frequency (radians and Hz)
    '''
    
    def findLeadingEdges(timeSignal): 
        '''
        Find the time instants of crossing the average value.
        @param timeSignal 2xN array (sample instants and values)
        @return Array of times
        '''
        squareWave = numpy.sign(timeSignal[1,:] - numpy.average(timeSignal[1,:]))
        leadingEdgeIndices = squareWave[1:]-squareWave[:-1] > 0
        #pyplot.plot(sampleTime[1:],leadingEdges)
        truncatedTimes = timeSignal[0,1:]
        return truncatedTimes[leadingEdgeIndices]
    
    # Find zero crossings              
    referenceEdges = findLeadingEdges(referenceSignal)
    dividerEdges = findLeadingEdges(dividerOutput)
    
    # Find time shift of divider with respect to reference
    numberOfCorrespondingEdges = min(len(dividerEdges),len(referenceEdges))
    timeShifts = dividerEdges[:numberOfCorrespondingEdges] -referenceEdges[:numberOfCorrespondingEdges]
    
    # Find the frequency
    def findPeriod(leadingEdges):
        '''Find the average distance between leading edges.'''
        return numpy.average(leadingEdges[1:]-leadingEdges[:-1])
    averagePeriod = numpy.average(findPeriod(referenceEdges),findPeriod(dividerEdges))

    # Report phase shift and frequency
    phaseShift = -1*numpy.average(timeShifts)/averagePeriod*2*numpy.pi
    frequency = 1/averagePeriod
    
    return phaseShift,frequency


 
if __name__ == '__main__':
   
    pass