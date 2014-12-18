import numpy
from scipy import interpolate
import pylab

substrateHeight = 1.55
probeSpotHeight = 5.0

def printFieldStrenght(field,component):
    X,Y,Z,fieldXReal,fieldYReal,fieldZReal,fieldXImag,fieldYImag,fieldZImage = numpy.loadtxt('microstrip_standard-'+field.lower()+'-600MHz.txt',skiprows=2,unpack=True)
    
    xValues = numpy.unique(X)
    yValues = numpy.unique(Y)
    zValues = numpy.unique(Z)
    
    newShape = (len(xValues),len(yValues),len(zValues))
#    
#    X = numpy.reshape(X,newShape,order='F')
#    Y = numpy.reshape(X,newShape,order='F')
#    Z = numpy.reshape(X,newShape,order='F')
    
    if component == 'y':
        fieldValues = fieldYReal
    elif component == 'z':
        fieldValues = fieldZReal
    else:
        raise ValueError
    fieldValues = numpy.reshape(fieldValues,newShape,order='F')
    interpolator = interpolate.RectBivariateSpline(yValues,zValues,fieldValues[0,:,:])
    fieldCut = interpolator.ev(yValues,substrateHeight+probeSpotHeight)
    fieldTitle = field+component
    fieldUnits = ('V/m' if field=='E' else 'A/m') + '/sqrt(W)'
    
    pylab.plot(yValues,fieldCut)
    pylab.title(fieldTitle)
    pylab.xlabel('y (mm)')
    pylab.ylabel(fieldUnits)
    pylab.show()
    
    print 'max('+fieldTitle+'):',numpy.abs(fieldCut).max(),fieldUnits

print 'Height above substrate',probeSpotHeight,'mm'
printFieldStrenght('E','y')
printFieldStrenght('E','z')
printFieldStrenght('H','y')
printFieldStrenght('H','z')