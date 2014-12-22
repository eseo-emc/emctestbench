"""
Quick test to scan a single tone along the X-axis in nearfield

Manual:
- power on the preamp (12V/0.5A)
- route the preamp to the VSA
- set the VSA to basic I/Q
- center the VSA on the tone

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
import device
from probecalibration import LaserPositioner,ProbeCalibration
from nfsfile import NfsFile

import vtk
from enthought.traits import api


class HorizontalRectangle(api.HasTraits):
    topRight = api.Array(shape=(2,))
    bottomLeft = api.Array(shape=(2,))
    height = api.Float()
    displayZOffset = api.Float(0.0)
    
    @property
    def meshCoordinates(self):
        (x,y) = numpy.meshgrid(numpy.array([self.topRight[0],self.bottomLeft[0]]),
                               numpy.array([self.topRight[1],self.bottomLeft[1]]),
                               indexing='ij')
        z = numpy.ones(x.shape)*self.height + self.displayZOffset
        return {'x':x,'y':y,'z':z}

    def __init__(self,color,*args,**kwargs):
        super(HorizontalRectangle,self).__init__(*args,**kwargs)
        self.plot = mlab.mesh(self.meshCoordinates['x'],
                              self.meshCoordinates['y'],
                              self.meshCoordinates['z'],
                              opacity=0.3,color=color)
                              
    def _topRight_changed(self, old, new):
        self._updatePlot()
    def _bottomLeft_changed(self, old, new):
        self._updatePlot()
    def _height_changed(self,old,new):
        self._updatePlot()
    def _updatePlot(self):
        if hasattr(self,'plot'):
            self.plot.mlab_source.set(**self.meshCoordinates)
    def sort(self):
        top =    max(self.topRight[1],self.bottomLeft[1])
        bottom = min(self.topRight[1],self.bottomLeft[1])
        right =  max(self.topRight[0],self.bottomLeft[0])
        left =   min(self.topRight[0],self.bottomLeft[0])
        self.topRight = (right,top)
        self.bottomLeft = (left,bottom)


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
        
#        self.powerSupply = None
        self.powerSupply = device.knownDevices['powerSupply']
        self.powerSupply.setChannelParameters(4,Voltage(12.0,'V'),Current(0.7,'A'))
        self.powerSupply.setChannelParameters(3,Voltage(9.0,'V'),Current(0.25,'A'))
        self.powerSupply.setChannelParameters(2,Voltage(5.0,'V'),Current(1.00,'A'))
        self.powerSupply.setChannelParameters(1,Voltage(3.3,'V'),Current(0.7,'A'))
        
        
#        self.switchPlatform = device.knownDevices['switchPlatform']
#        self.switchPlatform.closeSwitch('DUTtoSAorVNA')
    def prepare(self):
        self.laserPositioner.prepare()
    def tearDown(self):
        if hasattr(self,'_parkPosition'):
            self.laserPositioner.robot.setLocation(self._parkPosition)
        self.laserPositioner.tearDown()            

    def scanRelief(self):    
        self.laserPositioner.robot.getLocation()            
        self.laserPositioner.laser.laserOn = True
        raw_input('Move to start position and press enter...')
        startPosition = self.laserPositioner.robot.getLocation()
        self._parkPosition = self.laserPositioner.robot.getLocation()
        self._parkPosition[2] = self.laserPositioner.robot.safePosition[2]
        raw_input('Move to finish position and press enter...')
        
        self.laserPositioner.robot._setLocationStart(startPosition,
                                                     safeMovementZ=False,
                                                     highSpeed=False,
                                                     lowSpeed=True,
                                                     waitUntilDone=False)
        profiles = []
        while not(self.laserPositioner.robot._motionDone(None)):    
            profiles += [self.laserPositioner.getProfile()]
            
        self.laserPositioner.robot._setLocationFinish(startPosition)
        self.laserPositioner.laser.laserOn = False
            
        # rearrange and interpolate
        profiles = profiles[::-1] ## depends on x-direction, strangely...
        allRawProfiles = numpy.hstack(profiles)
        allRawProfiles = allRawProfiles[:,numpy.isfinite(allRawProfiles[2])]
        
        xValues = numpy.array(map(lambda profile: profile[0][0],profiles))
        newYValues = numpy.linspace(allRawProfiles[1].min(),allRawProfiles[1].max(),500)
        newZ = []
        for profile in profiles:
            validIndices = numpy.isfinite(profile[2])
            newZ += [numpy.interp(newYValues,profile[1][validIndices][::-1],profile[2][validIndices][::-1])]
        
        z = numpy.vstack(newZ)
        (x,y) = numpy.meshgrid(xValues,newYValues,indexing='ij')
        
        return (x,y,z)

    def estimateSubstrateHeight(self,z):
        return numpy.median(z)        
#        heightBins = numpy.arange(z.min(),z.max(),0.0001)
#        heightCounts = numpy.histogram(z,heightBins)[0]
#        modalIndex = numpy.argmax(heightCounts)
#        substrateHeight = numpy.mean(heightBins[modalIndex-1:modalIndex+1])
#        return substrateHeight
        
    def pickOriginAndZone(self,x,y,z,substrateHeightGuess,altitude):
        # dirty hack to suppress VTK errors when setting origin's mlab_data
        output=vtk.vtkFileOutputWindow()
        output.SetFileName("log.txt")
        vtk.vtkOutputWindow().SetInstance(output)          
        
        s = mlab.mesh(x, y, z)
        s.components[1].property.lighting = False
        maximumHeight = z.max()   
        safeHeight = maximumHeight+0.01
        
        origin = mlab.points3d(float(x.min()), float(y.min()), 0.0, mode='axes',
                               color=(1, 0, 0),
                               scale_factor=0.03) 
        scanZone = HorizontalRectangle((0,0,0),height=0,displayZOffset=self.laserPositioner.calibration.mechanical.spotZ.asUnit('m'))                                              
        substrateHeightZone = HorizontalRectangle((1,0,0),height=0)

        def updateSubstrateHeight(newHeight):
            colorRangeHeight = altitude-self.laserPositioner.calibration.mechanical.spotZ.asUnit('m')
            s.module_manager.scalar_lut_manager.data_range = (newHeight-colorRangeHeight,newHeight+colorRangeHeight)
            origin.mlab_source.set(z = newHeight)
            scanZone.height = newHeight+float(altitude)
            substrateHeightZone.height = newHeight
            
        updateSubstrateHeight(float(substrateHeightGuess))
                        
        def originSelectorCallBack(picker):
            origin.mlab_source.set(x = picker.pick_position[0],
                                   y = picker.pick_position[1])
            
            selectedPosition = Position(picker.pick_position,unit='m')
            self.laserPositioner.setProbeLocation(Position([selectedPosition[0],selectedPosition[1],safeHeight],'m'))    
            self.laserPositioner.setProbeLocation(selectedPosition + Position([0,0,0.002],'m'))    
      
        picker = mlab.gcf().on_mouse_pick(originSelectorCallBack,
                                          type='cell',
                                          button='Middle')
            
        def zoneSelectorCallback(picker,zone):
            pickedPosition = picker.pick_position[0:2]
            if picker.topRightPicked:
                zone.bottomLeft = pickedPosition
            else:
                zone.topRight = pickedPosition
            picker.topRightPicked = not(picker.topRightPicked)
        def scanZoneSelectorCallback(picker):  
            return zoneSelectorCallback(picker,scanZone)
        def substrateHeightZoneSelectorCallback(picker):
            zoneSelectorCallback(picker,substrateHeightZone)
            if not(picker.topRightPicked):
                substrateHeightZone.sort()
                zValuesInZone = z[(x > substrateHeightZone.bottomLeft[0]) &
                                  (x < substrateHeightZone.topRight[0]) &
                                  (y > substrateHeightZone.bottomLeft[1]) &
                                  (y < substrateHeightZone.topRight[1])]
                print 'Estimating subtrate height based on',zValuesInZone.shape,'values...'
                if len(zValuesInZone) > 0:                
                    heightEstimate = self.estimateSubstrateHeight(zValuesInZone)
                    updateSubstrateHeight(heightEstimate)
            
            
        picker = mlab.gcf().on_mouse_pick(scanZoneSelectorCallback,
                                          type='cell',
                                          button='Right')
        picker.add_trait('topRightPicked',api.Bool(False))

        picker = mlab.gcf().on_mouse_pick(substrateHeightZoneSelectorCallback,
                                          type='cell',
                                          button='Left')
        picker.add_trait('topRightPicked',api.Bool(False))
        
        mlab.orientation_axes()
        mlab.view(azimuth=0,elevation=0)
        mlab.show()   
        scanZone.sort()
        
        lastProbeLaserPosition = self.laserPositioner.getProbeLocation()
        lastProbeLaserPosition[2] = safeHeight
        self.laserPositioner.setProbeLocation(lastProbeLaserPosition)        
        
        originPosition = Position(origin.mlab_source.points[0][:],'m')  
        
        return (originPosition,scanZone)
    

    def sweep(self,origin,probeZone,resultPath):
        if self.powerSupply:
            self.powerSupply.turnChannelOn(1)
            self.powerSupply.turnChannelOn(2)
            self.powerSupply.turnChannelOn(3)
            self.powerSupply.turnChannelOn(4)
            
        if isinstance(self.analyzer,SpectrumAnalyzer):
            self.analyzer.measure() # just to check that it responds
            self.analyzer.align()  
        else:
            self.analyzer.measure(1,0) # just to check that it responds
        frequencies = self.analyzer.frequency.f  
                
        pitch = 0.001
        (xGrid,yGrid) = numpy.meshgrid(numpy.arange(probeZone.bottomLeft[0],probeZone.topRight[0],pitch),
                                       numpy.arange(probeZone.bottomLeft[1],probeZone.topRight[1],pitch))                                       
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
                for (pointNumber,xPosition,yPosition) in zip(range(xGrid.size),xGrid.flat,yGrid.flat):
                    pointStart = time.clock()                
                    newPosition = Position(numpy.array([xPosition,yPosition,zPosition]),'m')
                    self.laserPositioner.setProbeLocation(newPosition, highSpeed=True)
                    if isinstance(self.analyzer,SpectrumAnalyzer):
                        naturalPowers = numpy.power(10.0,self.analyzer.measure()/10.0)
                        naturalVoltages = numpy.sqrt(naturalPowers * 50.0)
                    else:
                        naturalVoltages = numpy.sqrt(50.0) * self.analyzer.measure(1,0).s[:,0,0]
                    complexVoltages.append(naturalVoltages)
                        
                    nfsFile.writePoint(newPosition-origin,naturalVoltages)
                    
                    pointDuration = time.clock() - pointStart
                    remainingTime = pointDuration * (xGrid.size - (pointNumber+1))
                    sys.stdout.write('\r{0:.1f}m remaining...'.format(remainingTime/60.0))
                        
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
    print 'Start mode scan'
    test = NearFieldMode('Hy-5mm.xml',analyser='SA')
    test.prepare()
    
    (x,y,z) = test.scanRelief()
    substrateHeight = test.estimateSubstrateHeight(z)
    scanHeight = 0.010
    (origin,scanZone) = test.pickOriginAndZone(x,y,z,substrateHeight,scanHeight)

    (xGrid,yGrid,zPosition,complexVoltagesGrid,frequencies) = \
        test.sweep(origin,scanZone,'Z:/Measurements/NFSE-in/D3-FAQ15-Hy-'+time.strftime('%H%M%S'))

    test.tearDown()



#%% export XML
#resultFolder = 'Z:/Measurements/NFSE-in'
#fileName = 'D2-Hy-2'
#imageName = 'D2'
#
#xGridUserOrigin = xGrid -origin.points[0][0]
#yGridUserOrigin = yGrid - origin.points[0][1]
#zPositionUserOrigin = zPosition - origin.points[0][2]
#


### create simple XML
#samplesList = ''
#for (xCoordinate,yCoordinate,complexVoltage) in zip(xGridUserOrigin.flat,yGridUserOrigin.flat,complexVoltagesGrid.reshape(xGridUserOrigin.size,frequencies.size).tolist()):
#    samplesList += '{x:.6f} {y:.6f} {z:.6f}'.format(x=xCoordinate,y=yCoordinate,z=zPositionUserOrigin)
#    complexVoltageArray = numpy.array(complexVoltage)
#    for (realVoltage,imaginaryVoltage) in zip(complexVoltageArray.real.flat,complexVoltageArray.imag.flat):
#        samplesList += ' {realVoltage:.6e} {imaginaryVoltage:.6e}'.format(realVoltage=realVoltage,imaginaryVoltage=imaginaryVoltage)
#    samplesList += '\n'
#    
#   
#xmlText = '''<?xml version="1.0" encoding="UTF-8"?>
#<EmissionScan>
#  <Nfs_ver>0.4</Nfs_ver>
#  <Filename>'''+fileName+'''</Filename>
#  <File_ver>1.0</File_ver>
#  <Date>24 avr. 2014</Date>
#  <Source>ESEO-EMC</Source>
#  <Disclaimer>This file saves result of near field measurement. Others using is not guaranteed.</Disclaimer>
#  <Copyright>This document is the property of ESEO</Copyright>
#  <Notes>Built by EMC TestBench</Notes>
#'''+test.laserPositioner.calibration.electrical.nfsXml()+'''
#  <Component>
#    <Name>'''+fileName+'''</Name>
#    '''+dutImages[fileName.split('-')[0]].nfsXml()+'''
#  </Component>
#  <Data>
#    <Coordinates>xyz</Coordinates>
#    <X0>0</X0>
#    <Y0>0</Y0>
#    <Z0>0</Z0>
#    <Frequencies>
#      <Unit>Hz</Unit>
#      <List>''' + ' '.join(map(str,frequencies.tolist())) + '''</List>
#    </Frequencies>
#    <Measurement>
#      <Unit>v</Unit>
#      <Unit_x>m</Unit_x>
#      <Unit_y>m</Unit_y>
#      <Unit_z>m</Unit_z>
#      <Format>ri</Format>
#      <List>'''+samplesList+'''</List>
#    </Measurement>
#  </Data>
#</EmissionScan>
#'''
#
### writeout
#fileHandle = open(resultFolder + '/' + fileName+'.xml','w')
#fileHandle.write(xmlText)
#fileHandle.close()

#    import tables
#    nfsFile = tables.openFile('D1C-common-50Ohm-3GHz-sticker-quick.h5', mode='w', title="Near-Field Scan")
#    root = nfsFile.root
#    nfsFile.createArray(root,"voltage_dB",20.0*numpy.log10(numpy.abs(complexVoltagesGrid)))
#    nfsFile.createArray(root,"voltage",complexVoltagesGrid)
#    nfsFile.createArray(root,"xCoords",xGrid)
#    nfsFile.createArray(root,"yCoords",yGrid)
#    nfsFile.close()
#    
#    print "Done"




  
## show magnitude
#pyplot.plot(numpy.real(voltages[0,:]),numpy.abs(voltages[1,:]),label='Open')
##pyplot.plot(numpy.real(voltages_load[0,:]),numpy.abs(voltages_load[1,:]),label='Loaded')
#pyplot.ylabel('Transfer magnitude (1)')
#pyplot.xlabel('x position (mm)')
#pyplot.legend()
#pyplot.show()
#    
## show phase
#pyplot.plot(numpy.real(voltages[0,:]),numpy.rad2deg(numpy.angle(voltages[1,:])),label='Open')
##pyplot.plot(numpy.real(voltages_load[0,:]),numpy.rad2deg(numpy.angle(voltages_load[1,:])),label='Loaded')
#pyplot.ylabel('Phase (degrees)')
#pyplot.xlabel('x position (mm)')
#pyplot.legend()
#pyplot.show()
