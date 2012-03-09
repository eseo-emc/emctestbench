from utility.metaarray import MetaArray,axis
from device import Agilent86100a

reflectrometer = Agilent86100a()

sampleTimes = reflectrometer.getChannelWaveform(1)[0,:]

experimentNames = [ 'line10mm','thru',
                    'line4mm']
experimentColumns = []
for experimentName in experimentNames:
	experimentColumns.append((experimentName+'_raw','r',experimentName+' (raw)'))
    experimentColumns.append((experimentName+'_calibrated','r',experimentName+' (calibrated)'))

results = MetaArray((len(sampleTimes),len(experimentNames)*2), info=[
			axis('t', values=sampleTimes, units='s',title='Time'), 
			axis('experiment', cols=experimentColumns),
		])

for experimentName in experimentNames:
	dump = raw_input('Press enter to start experiment "%s"' % experimentName)

    rawSignal = reflectrometer.getChannelWaveform(1)
    calibratedResponse = reflectrometer.getChannelWaveform(1)
	
# 	assert rawSignal[0,:] == sampleTimes
#     assert calibratedResponse[0,:] == sampleTimes
    
	results['experiment':(experimentName+'_raw')] = rawSignal[1,:]
	results['experiment':(experimentName+'_calibrated')] = calibratedResponse[1,:]
    
results.writeToExcel('../results/lineDelayMeasurements.xls')
# results.write('../results/reflectrometryResults.ma')
