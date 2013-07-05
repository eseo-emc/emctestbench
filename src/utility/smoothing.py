import numpy

# http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
def smoothBoxcar(unsmoothedSamples,windowSize):
    assert windowSize % 2 == 1, 'windowSize needs to be odd'
    middleSamples = numpy.convolve(unsmoothedSamples,numpy.ones((windowSize,))/windowSize,mode='valid')
    def firstSamples(unsmoothedSamples):
        outputSamples = []
        for sample in range(0,(windowSize-1)/2):
            averagingSamples = sample*2+1
            outputSamples += [unsmoothedSamples[0:averagingSamples].sum()/averagingSamples]
        return outputSamples
    return numpy.concatenate((firstSamples(unsmoothedSamples),middleSamples,firstSamples(unsmoothedSamples[::-1])[::-1]))
    
if __name__ == '__main__':   
    from pylab import *
    from numpy import *
    
    xOriginal = arange(0,5,0.1)
    plot(xOriginal,label='original')
    plot(smoothBoxcar(xOriginal,5),'x',label='smoothed')
    
    legend()
    show()