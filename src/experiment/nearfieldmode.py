"""
preamp
http://www.everythingrf.com/rf-microwave-amplifiers/p/Planar-Monolithics-Industries-82_PEC_60_0R14R0_5R0_10_12_SFF

@author: Sjoerd Op 't Land
"""
#%% start and scan
import numpy
import time
#from matplotlib import pyplot
from mayavi import mlab
import sys

import os
import shutil
import zipfile

import device
from device.spectrumanalyzer import SpectrumAnalyzer
from utility.quantities import Amplitude,Voltage,Current,Position,Frequency
from utility.gracefulinterrupthandler import GracefulInterruptHandler
import device
from probecalibration import LaserPositioner,ProbeCalibration
from nfsfile import NfsFile

class NearFieldMode:
    def __init__(self,calibrationFile,analyser='VNA'):
        self.laserPositioner = LaserPositioner(ProbeCalibration.fromFile(calibrationFile))
        
        if analyser == 'VNA':
            self.analyzer = device.knownDevices['networkAnalyzer']
            self.analyzer._hardPresetMethod = self.laserPositioner.robot.strobeLowGpio1
        elif analyser == 'SA':
            self.analyzer = device.knownDevices['spectrumAnalyzer']
            self.analyzer.reset()    
            self.analyzer.span = Frequency(1000,'MHz')
            self.analyzer.centerFrequency = Frequency(500,'MHz')
            self.analyzer.numberOfAveragingPoints = 100 #500 for D3
        else:
            raise ValueError, 'Analyser choice not recognised'
        
        self.powerSupply = None
#        self.powerSupply = device.knownDevices['powerSupply']
#        self.powerSupply.setChannelParameters(4,Voltage(12.0,'V'),Current(1.4,'A'))
#        self.powerSupply.setChannelParameters(3,Voltage(9.0,'V'),Current(0.25,'A'))
#        self.powerSupply.setChannelParameters(2,Voltage(5.0,'V'),Current(1.00,'A'))
#        self.powerSupply.setChannelParameters(1,Voltage(3.3,'V'),Current(0.7,'A'))
        if not(self.powerSupply):
            print "Warning: the power supply is not remote controlled. If you need an LNA, switch it on manually."
        
#        self.switchPlatform = device.knownDevices['switchPlatform']
#        self.switchPlatform.closeSwitch('DUTtoSAorVNA')
    def prepare(self):
        self.laserPositioner.prepare()
    def tearDown(self):
        if hasattr(self,'_parkPosition'):
            self.laserPositioner.robot.setLocation(self._parkPosition)
        self.laserPositioner.tearDown()            




        
    
    

    def sweep(self,origin,probeZone,resultPath,pitch):
        if pitch.size != 2:
            pitch = Position([pitch,pitch])
            
        if self.powerSupply:
            self.powerSupply.turnChannelOn(1)
            self.powerSupply.turnChannelOn(2)
            self.powerSupply.turnChannelOn(3)
            self.powerSupply.turnChannelOn(4)
            
        if isinstance(self.analyzer,SpectrumAnalyzer):
            self.analyzer.measure() # just to check that it responds
#            self.analyzer.align()  
        else:
            self.analyzer.measure(1,0) # just to check that it responds
        frequencies = self.analyzer.frequency.f  
                
        
        (xGrid,yGrid) = numpy.meshgrid(numpy.arange(probeZone.bottomLeft[0],probeZone.topRight[0],pitch[0].asUnit('m')),
                                       numpy.arange(probeZone.bottomLeft[1],probeZone.topRight[1],pitch[1].asUnit('m')))                                       
        zPosition = probeZone.height
        
        xGrid = xGrid.T
        yGrid = yGrid.T    
        
        
        
        try:
            for corner in [(0,0),(-1,0),(-1,-1),(0,-1)]:
                self.laserPositioner.setProbeLocation(Position(numpy.array([xGrid[corner],yGrid[corner],zPosition]),'m'))
            
            complexVoltages = []
            startTime = time.clock()
            
            (resultFolder,fileName) = os.path.split(resultPath)
            imageName = fileName.split('-')[0]
            
            with NfsFile(resultFolder,fileName,imageName=imageName,calibration=self.laserPositioner.calibration.electrical,frequencies=frequencies) as nfsFile:
                with GracefulInterruptHandler() as handler:
                    for (pointNumber,xPosition,yPosition) in zip(range(xGrid.size),xGrid.flat,yGrid.flat):            
                        newPosition = Position(numpy.array([xPosition,yPosition,zPosition]),'m')
                        self.laserPositioner.setProbeLocation(newPosition, highSpeed=True)
                        if isinstance(self.analyzer,SpectrumAnalyzer):
                            naturalPowers = numpy.power(10.0,self.analyzer.measure()/10.0)
                            naturalVoltages = numpy.sqrt(naturalPowers * 50.0)
                        else:
                            naturalVoltages = numpy.sqrt(50.0) * self.analyzer.measure(1,0).s[:,0,0]
                        complexVoltages.append(naturalVoltages)
                            
                        nfsFile.writePoint(newPosition-origin,naturalVoltages)
                        
                        pointProgress = (pointNumber+1.0)/xGrid.size
                        remainingTimeEstimation = (time.clock()-startTime)*(1/pointProgress - 1)
                        sys.stdout.write('\r{h}h{m}m remaining...'.format(h=int(remainingTimeEstimation/3600.0),m=int((remainingTimeEstimation%3600)/60)))
                        
                        if handler.interrupted:
                            break
                            
                print 'Sweep took {0:.1f}s'.format(time.clock()-startTime)
            
        finally:
            print 'Shutting down...'
            if self.powerSupply:
                self.powerSupply.turnChannelOff(2)  
                self.powerSupply.turnChannelOff(1)
                self.powerSupply.turnChannelOff(3)
                self.powerSupply.turnChannelOff(4)
#            self.laserPositioner.robot.goSafe()        
        
        complexVoltagesGrid = numpy.array(complexVoltages).reshape(xGrid.shape + frequencies.shape)                     
        return (xGrid,yGrid,zPosition,complexVoltagesGrid,frequencies)
        
        
 
if __name__ == '__main__':
    import pickle    
    
    print 'Start mode scan'
    test = NearFieldMode('Hy.xml',analyser='SA')
    test.prepare()
    
    initialAltitude = 0.005 + 0.0015
    
#    if raw_input('Re-use last zone (y/n) [n]?') != 'y':
    while True:
        (origin,scanZone) = test.laserPositioner.scanAndPickOriginAndZone(altitude=initialAltitude)
        if raw_input('Retry (y/n) [n]?') != 'y':
            break
#        with open('lastScanZone.pickled','wb') as pickledZoneFile:
#            pickle.dump((origin,scanZone),pickledZoneFile)
#    else:
#        with open('lastScanZone.pickled','rb') as pickledZoneFile:
#            (origin,scanZone) = pickle.load(pickledZoneFile)
            
    for altitude in [initialAltitude]:    
        scanZone.height = float(origin[2] + altitude)
        (xGrid,yGrid,zPosition,complexVoltagesGrid,frequencies) = \
            test.sweep(origin,scanZone,
               'D:/Measurements/NFSE-out/D2-{probe}-{altitudeMm}mm-{timestamp}'.format(
                   timestamp=time.strftime('%H%M%S'),
                   altitudeMm = altitude*1000.0,
                   probe=test.laserPositioner.calibration.name),
               pitch=Position([2,2],'mm'))

    test.tearDown()

