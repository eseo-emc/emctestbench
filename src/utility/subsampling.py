# -*- coding:utf-8 -*-
"""
Created on 12 janv. 2011

@author: Sjoerd Op 't Land and Richard Perdriau
"""
import numpy

def subsamplingFrequency(injectionFrequency,targetFrequency=1000e3):
    '''
    Calculate the sampling clock frequency that shifts injectionFrequency to 
    targetFrequency by subsampling.
    @param injectionFrequency Injection frequency in Hertz
    @param targetFrequency Frequency at which the injection should appear in Hertz
    @return Subsampling clock frequency
    '''
    sensorBandwidth = 2e6
    frequencyStep = -5
    for samplingFrequency in numpy.arange(sensorBandwidth+frequencyStep,sensorBandwidth/2,frequencyStep):
        if injectionFrequency % samplingFrequency == targetFrequency:
            return samplingFrequency
        
    
        
if __name__ == '__main__':
    print subsamplingFrequency(500e6)