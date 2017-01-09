import numpy
from scipy import interpolate
import pylab

substrateHeight = 1.55
probeSpotHeight = 5.0
yCenter = 21.55

def printFieldStrenght(field,component):
    X,Y,Z,fieldXReal,fieldYReal,fieldZReal,fieldXImag,fieldYImag,fieldZImage = numpy.loadtxt('microstrip_standard-'+field.lower()+'-600MHz.txt',skiprows=2,unpack=True)
    
    xValues = numpy.unique(X)
    yValues = numpy.unique(Y)-yCenter
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
    
    #Maximum calculation
    maxIndex = numpy.abs(fieldCut).argmax()
    maxField = fieldCut[maxIndex]
    maxY = yValues[maxIndex]
    print 'max({fieldTitle}): {maxField:.3f} {unit} at y = {maxY} mm (z = {z} mm)'.format(
        fieldTitle = fieldTitle,
        maxField = abs(maxField),
        maxY = maxY,
        unit = fieldUnits,
        z = probeSpotHeight)

    
    
    pylab.plot(yValues,fieldCut)
    pylab.plot([maxY],[maxField],'ro')    
    pylab.title('{field} at {height} mm above substrate'.format(field=fieldTitle, height=probeSpotHeight))
    pylab.xlabel('y (mm)')
    pylab.ylabel(fieldUnits)
    pylab.show()
    
    

#printFieldStrenght('E','y')
printFieldStrenght('E','z')
printFieldStrenght('H','y')
printFieldStrenght('H','z')