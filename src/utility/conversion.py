import numpy

def dB(linearValues):
    return 20.0*numpy.log10(abs(linearValues))
def stoz(s11Values,z0):
    return z0*(1+s11Values)/(1-s11Values)