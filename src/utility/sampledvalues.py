import numpy
from result.persistance import SmartDommable 

def complexInterp(x,xp,fp):
    return numpy.interp(x,xp,fp.real) + 1j*numpy.interp(x,xp,fp.imag)

class SampledValues(SmartDommable):   
    def __init__(self,frequencies=None,values=None):
        self.frequencies = frequencies
        self.values = values
    def __repr__(self):
        return str(self.frequencies) + ',' + str(self.values)
    @property
    def minimumFrequency(self):
        return self.frequencies[0]
    @property
    def maximumFrequency(self):
        return self.frequencies[-1]
        
    def __div__(self,other):
        (selfResampled,otherResampled) = self.alignFrequencies(other)
        return SampledValues(selfResampled.frequencies,selfResampled.values/otherResampled.values)
    
    def combinedFrequencies(self,other):
        minimumFrequency = max(self.minimumFrequency,other.minimumFrequency)
        maximumFrequency = min(self.maximumFrequency,other.maximumFrequency)
        allFrequencies = numpy.unique(numpy.hstack([self.frequencies,other.frequencies]))
        return allFrequencies[(allFrequencies >= minimumFrequency) &
                              (allFrequencies <= maximumFrequency)]
    def _interpolateToFrequencies(self,frequencies):
        return SampledValues(frequencies,
                             complexInterp(frequencies,self.frequencies,self.values))
    def alignFrequencies(self,other):
        return (self._interpolateToFrequencies(self.combinedFrequencies(other)),
                other._interpolateToFrequencies(self.combinedFrequencies(other)))

if __name__ == '__main__':
    a = SampledValues(numpy.arange(1.0,6),10*numpy.arange(1.0,6))
    b = SampledValues(numpy.arange(1.0,6)+0.5,(100.1+200.1j)*(numpy.arange(1.0,6)+0.5))
    print a
    print b
    
    (A,B) = a.alignFrequencies(b)
    print A
    print B    
    
    print b/a
    
    loopThrough = SampledValues.fromXml(b.toXml())
    print loopThrough
    