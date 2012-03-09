import skrf
import pylab
import numpy

standardPath = 'Y:\ADS\SOIC8_Fixture_Test_prj\standard_definitions'
standardFiles = skrf.load_all_touchstones(standardPath)

measuredPath = 'Y:\ADS\SOIC8_Fixture_Test_prj\standard_measurements'
measuredFiles = skrf.load_all_touchstones(measuredPath)

outputPath = 'Y:\ADS\SOIC8_Fixture_Test_prj\misc'

frequencyList = measuredFiles.values()[0].f
def makeStandard(standardName,coefficient,mirror=False):
    assert coefficient.ndim == 2
    standard = skrf.Network()
    standard.f = frequencyList
    
    repeatableCoefficient = numpy.array([coefficient])
    standard.s = repeatableCoefficient.repeat(len(standard.f),0)
    
    if mirror:
        return skrf.two_port_reflect(standard,standard)
    else:
        return standard

## SOL calibration
measured = []
for measurementName in ['open','load','short']:
    measured.append(measuredFiles[measurementName])

ideals = [makeStandard('openIdeal',numpy.array([[+1.]])),
            makeStandard('loadIdeal',numpy.array([[0.]])),
            makeStandard('shortIdeal',numpy.array([[-1.]]))]

solCalibration = skrf.Calibration(measured,ideals)
solCalibration.run()

## SOLT calibration
twoPortMeasurements = []
for measurementName in ['open','load','short','thru']:
    measurement = measuredFiles[measurementName]
    if measurement.number_of_ports == 1:
        twoPortMeasurements.append(skrf.two_port_reflect(measurement,measurement))
    elif measurement.number_of_ports == 2:
        twoPortMeasurements.append(measurement)
    else:
        print 'Error'

ideals = [makeStandard('openIdeal',numpy.array([[+1.]]),mirror=True),
            makeStandard('loadIdeal',numpy.array([[0.]]),mirror=True),
            makeStandard('shortIdeal',numpy.array([[-1.]]),mirror=True),
            makeStandard('thruIdeal',numpy.array([[0,1],[1,0]]))]

soltCalibration = skrf.Calibration(twoPortMeasurements,ideals)
soltCalibration.run()

## TRL calibrations
def trlCalibrate(name):
    measured = [measuredFiles['thru'],
                skrf.two_port_reflect(measuredFiles['short'],measuredFiles['short']),
                measuredFiles[name] ]

    ideals = [  makeStandard('thruIdeal',numpy.array([[0,1],[1,0]])),
                makeStandard('shortIdeal',numpy.array([[-1.]]),mirror=True),
                standardFiles[name] ]
                
    trlCalibration = skrf.Calibration(measured,ideals)
    trlCalibration.run()
    return trlCalibration

trlCalibration1 = trlCalibrate('line_10mm')
trlCalibration2 = trlCalibrate('line_4mm')


## plot different coefficients
def delay(coefficient,frequency):
    return -1.*numpy.unwrap(numpy.angle(coefficientValues))/(2*numpy.pi*frequency)

interestingCoefficients = solCalibration.coefs
# interestingCoefficients = calibration.coefs
calculatedCoefficients = {  'e01e10':(soltCalibration.coefs['e00']*soltCalibration.coefs['e11'])-soltCalibration.coefs['det_X'],
                            'e23e32':(soltCalibration.coefs['e22']*soltCalibration.coefs['e33'])-soltCalibration.coefs['det_Y']}
# interestingCoefficients = { 'reflection tracking':solCalibration.coefs['reflection tracking'],
#                             'e00e11-det_X':(soltCalibration.coefs['e00']*soltCalibration.coefs['e11'])-soltCalibration.coefs['det_X'],
#                             'e22e33-det_Y':(soltCalibration.coefs['e22']*soltCalibration.coefs['e33'])-soltCalibration.coefs['det_Y'], }
# interestingCoefficients = { 'k':soltCalibration.coefs['k'],
#                             'e01e10/e23e32':calculatedCoefficients['e01e10']/calculatedCoefficients['e23e32'] }
# interestingCoefficients = { 'directivity':solCalibration.coefs['directivity'],
#                             'e00':soltCalibration.coefs['e00'],
#                             'e11':soltCalibration.coefs['e11'],
#                             'source match':solCalibration.coefs['source match'],
#                             'e22':soltCalibration.coefs['e22'],
#                             'e33':soltCalibration.coefs['e33'] }
# interestingCoefficients = { 'directivity':solCalibration.coefs['directivity'],
#                             'avg(e00,33)':0.5*(soltCalibration.coefs['e00']+soltCalibration.coefs['e33']),
#                             'source match':solCalibration.coefs['source match'],
#                             'avg(e11,e22)':0.5*(soltCalibration.coefs['e11']+soltCalibration.coefs['e22']) }
interestingCoefficients = { 'e01e10 TRL1':(trlCalibration1.coefs['e00']*trlCalibration1.coefs['e11'])-trlCalibration1.coefs['det_X'],
                            'e01e10 TRL2':(trlCalibration2.coefs['e00']*trlCalibration2.coefs['e11'])-trlCalibration2.coefs['det_X'],
                            'e01e10 SOLT':calculatedCoefficients[ 'e01e10'] }

remarks = {'directivity':' (e00)', 'reflection tracking':' (e01e10)','source match':' (e11)'}
for coefficientName,coefficientValues in interestingCoefficients.items():
    if coefficientName in remarks.keys():
        coefficientName += remarks[coefficientName]
#     pylab.plot(frequencyList,20*numpy.log(numpy.abs(coefficientValues)),label=coefficientName)
#     pylab.ylabel('Magnitude (dB)')
        
#     pylab.plot(frequencyList,numpy.abs(coefficientValues),label=coefficientName)
#     pylab.ylabel('Magnitude (lin)')
        
#     pylab.plot(frequencyList,delay(coefficientValues,frequencyList)/1e-12,label=coefficientName)
#     pylab.ylabel('Delay (ps)')

    pylab.plot(frequencyList,numpy.rad2deg(numpy.unwrap(numpy.angle(coefficientValues)))-numpy.rad2deg(numpy.unwrap(numpy.angle(interestingCoefficients.values()[2]))),label=coefficientName)
    pylab.ylabel('Phase (deg)')

pylab.xlabel('Frequency (Hz)')
pylab.legend()
pylab.show()



## SOL: make up 2 port network that represents adapter
adapterModelSol = skrf.Network(name='Feed line model (SOL)')
adapterModelSol.frequency = solCalibration.frequency

e00 = solCalibration.coefs['directivity']
e01 = numpy.sqrt(solCalibration.coefs['reflection tracking'])
e10 = numpy.sqrt(solCalibration.coefs['reflection tracking'])
e11 = solCalibration.coefs['source match']

adapterModelSol.s = numpy.array([[e00,e01],[e10,e11]]).transpose((2,0,1))
adapterModelSol.write_touchstone(filename='feedModelSol',dir=outputPath)

## SOLT: make up 2 port network that represents adapter
def twoPortCalibrationToS2p(calibration,screenName,fileName):
    adapterModel = skrf.Network(name=screenName)
    adapterModel.frequency = calibration.frequency

    e10e01 = (calibration.coefs['e00']*calibration.coefs['e11'])-calibration.coefs['det_X']
    e23e32 = (calibration.coefs['e22']*calibration.coefs['e33'])-calibration.coefs['det_Y']
    reflectionTracking = 0.5*(e10e01+e23e32)

    e00 = 0.5*(calibration.coefs['e00']+calibration.coefs['e33'])
    e01 = numpy.sqrt(reflectionTracking)
    e10 = numpy.sqrt(reflectionTracking)
    e11 = 0.5*(calibration.coefs['e11']+calibration.coefs['e22'])

    adapterModel.s = numpy.array([[e00,e01],[e10,e11]]).transpose((2,0,1))
    adapterModel.write_touchstone(filename=fileName,dir=outputPath)

twoPortCalibrationToS2p(soltCalibration,'Feed line model (SOLT)','feedModelSolt')
twoPortCalibrationToS2p(trlCalibration1,'Feed line model (TRL1)','feedModelTrl1')
twoPortCalibrationToS2p(trlCalibration2,'Feed line model (TRL2)','feedModelTrl2')

## plot
# adapterModel.plot_s_re(1,0)
# pylab.show()
# 