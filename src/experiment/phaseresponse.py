'''
Created on 18 janv. 2011

@author: optland
'''
from matplotlib import pyplot
import time
import numpy
from phaselag import PhaseLag
from device import Agilent33
from utility.metaarray import MetaArray,axis

experiment = PhaseLag()
generator = Agilent33()

inputFrequencies = numpy.arange(16.0e6,27.0e6,.1e6)
experimentNames = ['No interference',
				'VCO VDD, 50 MHz (+5 dBm)',
				'VCO VDD, 25 MHz (+5 dBm)',
				'PH VDD, 50 MHz (+5 dBm)',
				'PH VDD, 25 MHz (+5 dBm)',
				'DIV VDD, 50 MHz (+5 dBm)',
				'DIV VDD, 25 MHz (+5 dBm)'
				]
experimentColumns = []
for experimentName in experimentNames:
	experimentColumns.append((experimentName,'phi',experimentName))

results = MetaArray((len(inputFrequencies),len(experimentNames)), info=[
			axis('f', values=inputFrequencies, units='Hz',title='Input frequency'), 
			axis('experiment', cols=experimentColumns),
		])

for experimentName in experimentNames:
	dump = raw_input('Press enter to start experiment "%s"' % experimentName)
	
	sweepResults = numpy.array([])
#		capture range chip 1 (type 5)
#		capture range chip 2 (type 6) 17.8 26.5
#		for inputFrequency in numpy.arange(16.5e6,24.9e6,.1e6):	  
	startTime = time.time()	  
	for inputFrequency in inputFrequencies:
		generator.setWaveform(inputFrequency, 2.5,2.5,'SQU')
		time.sleep(.4) # .3 should be safe
		phaseShift,frequency = experiment.measurePhaseAndFrequency()
		sweepResults = numpy.append(sweepResults,[phaseShift],axis=1)
	print 'Sweep took %f s' % (startTime-time.time())
	
	unwrappedResults = numpy.unwrap(sweepResults)
	halfwayAngle = unwrappedResults[len(unwrappedResults)/2]
	correction = (numpy.trunc(halfwayAngle / (2*numpy.pi)) +1)*-2*numpy.pi
	unwrappedResults = unwrappedResults + correction


	results['experiment':experimentName] = numpy.rad2deg(unwrappedResults)
		
	pyplot.plot(inputFrequencies,numpy.rad2deg(unwrappedResults),'.-',label=experimentName)
	
	results.writeToExcel('../../results/pllSweepResults.xls')
	results.write('../../results/pllSweepResults.ma')
	



pyplot.xlabel('PLL input frequency (Hz)')
pyplot.ylabel('phi_out - phi_in (degrees)')
pyplot.legend()
pyplot.show()
