"""

preamp
http://www.everythingrf.com/rf-microwave-amplifiers/p/Planar-Monolithics-Industries-82_PEC_60_0R14R0_5R0_10_12_SFF

@author: Sjoerd Op 't Land
"""
import numpy
import time
from matplotlib import pyplot
from mayavi import mlab
import sys
from utility.sampledvalues import SampledValues
from result.persistance import SmartDommable
import pylab

import device
from device.spectrumanalyzer import SpectrumAnalyzer
from utility.quantities import Amplitude,Voltage,Current,Position,Frequency,PowerRatio,Power


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

class ProbeCalibration(SmartDommable):
    def __init__(self,name='',spotZ=0.0):
        self.name = name
        self.mechanical = MechanicalProbeCalibration(spotZ)
        self.electrical = ElectricalProbeCalibration(self.name+'probe',field=self.name[0:2])

class LaserPositioner(object):
    def __init__(self,calibration=None):
        self.robot = device.knownDevices['positioner']
        self.laser = device.knownDevices['laser']
        
        self.calibration = calibration
        
    def prepare(self):
        self.laser.prepare()
    def tearDown(self):
        self.laser.tearDown()
        
        
    def setProbeLocation(self,pointLaserPosition,*args,**kwargs):
        if self.calibration.mechanical.calibrated:
            self.robot.setLocation(pointLaserPosition-self.calibration.mechanical.probeSpotLaser,*args,**kwargs)
        else:
            raise Warning('Cannot send probe to laserPosition, because not yet calibrated')
        
    def getProbeLocation(self):
        if self.calibration.mechanical.calibrated:
            return self.robot.getLocation()+self.calibration.mechanical.probeSpotLaser
        else:
            raise Warning('Cannot calculate laserPosition, because not yet calibrated')
        
        
    def getProfile(self):
        positionJustBefore = self.robot.getLocation()
        profile = self.laser.getProfile()
        positionJustAfter = self.robot.getLocation()
#        print positionJustAfter-positionJustBefore  
        
        averagePosition = ((positionJustAfter+positionJustBefore)/2)
        return Position([numpy.zeros(profile['y'].shape)+averagePosition[0],
                                            profile['y']+averagePosition[1],
                                            profile['z']+averagePosition[2]],unit='m')
    
    def scanAndPickOriginAndZone(self,*args,**kwargs):
        (x,y,z) = self.scanRelief()
        substrateHeight = self.estimateSubstrateHeight(z)
        return self.pickOriginAndZone(x,y,z,substrateHeight,*args,**kwargs)
    def estimateSubstrateHeight(self,z):
        return numpy.median(z)        
#        heightBins = numpy.arange(z.min(),z.max(),0.0001)
#        heightCounts = numpy.histogram(z,heightBins)[0]
#        modalIndex = numpy.argmax(heightCounts)
#        substrateHeight = numpy.mean(heightBins[modalIndex-1:modalIndex+1])
#        return substrateHeight
        
    def scanRelief(self):    
        self.robot.getLocation()            
        self.laser.laserOn = True
        raw_input('Move to start position and press enter...')
        startPosition = self.robot.getLocation()
#        self._parkPosition = self.robot.getLocation()
#        self._parkPosition[2] = self.robot.safePosition[2]
        raw_input('Move to finish position and press enter...')
        
        self.robot._setLocationStart(startPosition,
                                                     safeMovementZ=False,
                                                     highSpeed=False,
                                                     lowSpeed=True,
                                                     waitUntilDone=False)
        profiles = []
        while not(self.robot._motionDone(None)):    
            profiles += [self.getProfile()]
            
        self.robot._setLocationFinish(startPosition)
        self.laser.laserOn = False
            
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
    
    def pickOriginAndZone(self,x,y,z,substrateHeightGuess,altitude=0.001,pickZone=True):
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
        if pickZone:
            scanZone = HorizontalRectangle((0,0,0),height=0,displayZOffset=self.calibration.mechanical.spotZ.asUnit('m'))                                              
        substrateHeightZone = HorizontalRectangle((1,0,0),height=0)

        def updateSubstrateHeight(newHeight):
            colorRangeHeight = altitude-self.calibration.mechanical.spotZ.asUnit('m')
            s.module_manager.scalar_lut_manager.data_range = (newHeight-colorRangeHeight,newHeight+colorRangeHeight)
            origin.mlab_source.set(z = newHeight)
            if pickZone:
                scanZone.height = newHeight+float(altitude)
            substrateHeightZone.height = newHeight
            
        updateSubstrateHeight(float(substrateHeightGuess))
                        
        def originSelectorCallBack(picker):
            origin.mlab_source.set(x = picker.pick_position[0],
                                   y = picker.pick_position[1])
            
            selectedPosition = Position(picker.pick_position,unit='m')
            try:
                self.setProbeLocation(Position([selectedPosition[0],selectedPosition[1],safeHeight],'m'))    
                self.setProbeLocation(selectedPosition + Position([0,0,0.002],'m'))    
            except Warning:
                pass
      
        picker = mlab.gcf().on_mouse_pick(originSelectorCallBack,
                                          type='cell',
                                          button='Middle')
            
        def zoneSelectorCallback(picker,zone):
            pickedPosition = picker.pick_position[0:2]
            if pickZone:
                self.setProbeLocation(Position([pickedPosition[0],pickedPosition[1],safeHeight],'m'))
                self.setProbeLocation(Position([pickedPosition[0],pickedPosition[1],scanZone.height],'m'))

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
                print 'Estimating substrate height based on',zValuesInZone.shape,'values...'
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
        
        originPosition = Position(origin.mlab_source.points[0][:],'m')  
                       
        if pickZone:
            scanZone.sort()
            lastProbeLaserPosition = self.getProbeLocation()
            lastProbeLaserPosition[2] = safeHeight
            self.setProbeLocation(lastProbeLaserPosition)                
            return (originPosition,scanZone)    
        else:
            return originPosition
    
    def pickLaserPosition(self,targetDescription,dataCallBack=None):
        assert dataCallBack == None
        return self.scanAndPickOriginAndZone(pickZone=False)
                
    def pickLaserPositionAlongY(self,targetDescription,dataCallBack=None):   
        self.laser._deviceHandle.laserOn = True
        raw_input('Move laser at least 10cm above DUT, to see '+targetDescription)
        
        startPosition = self.robot.getLocation()
        profile = self.laser.getProfile()
            
        pylab.plot((profile['y']+startPosition[1]).asUnit('m'),
                   (profile['z']+startPosition[2]).asUnit('m'),'-',label=str(startPosition))
        
        pylab.xlabel('y')
        pylab.ylabel('z')
        
        pylab.legend()
        pylab.axis('equal')
        
        self._guess = None
        def onclick(event):
            if event.button == 2:
                self._guess = Position([startPosition[0],event.xdata,event.ydata],unit='m')
                print "Picked laserposition", self._guess
                if dataCallBack:
                    dataCallBack(self._guess)
        pylab.gcf().canvas.mpl_connect('button_press_event', onclick)
        
        pylab.title('Click with middle mouse button at '+targetDescription+' and close')
        pylab.show()
        
        if not(type(self._guess) == type(None)):
            return self._guess
        
    def testMechanicalCalibration(self):
        self.prepare()
        def goAbovePoint(point):
            point[2] += 0.002
            self.setProbeLocation(point)
        return self.pickLaserPosition('any point of interest, going 2mm above it (watch out!)',goAbovePoint)
        self.tearDown()
        

class LaserPositionerCalibrator(LaserPositioner):  
    def __init__(self,name='Ha',spotZ=0.0):
        LaserPositioner.__init__(self,ProbeCalibration(name,spotZ))
        self.analyzer = device.knownDevices['networkAnalyzer']
        self.powerSupply = device.knownDevices['powerSupply']
        
        self.analyzer._hardPresetMethod = self.robot.strobeLowGpio1
        
    def prepare(self):
        LaserPositioner.prepare(self)
        self.powerSupply.setChannelParameters(4,Voltage(12.0,'V'),Current(1.4,'A'))
        self.powerSupply.turnChannelOn(4)
        
    def tearDown(self):
        self.powerSupply.turnChannelOff(4)
        LaserPositioner.tearDown(self)
        
    def findSampleCentreLaserPosition(self):
        return self.pickLaserPosition('the top of the center of the trace')        

    def findSampleCentreXYPosition(self,sweepDirection='y'):
        sweepIndex = {'x':0, 'y':1}[sweepDirection]
        raw_input('Put probe just above sample for electrical maximum {sweepDirection}-search'.format(sweepDirection=sweepDirection))
        startPosition = self.robot.getLocation()
        
        sweepPositions = []
        fieldMagnitudes = []
        for deviation in numpy.arange(-0.007,0.007,0.0005):
            tryPosition = startPosition.copy()
            tryPosition[sweepIndex] += deviation
            sweepPositions.append(tryPosition[sweepIndex])
            self.robot.setLocation(tryPosition)
            fieldMagnitudes.append(self.analyzer.measure(1,0).s[-1,-1,-1])
            
        sweepPositions = numpy.array(sweepPositions)
        fieldMagnitudes = numpy.abs(numpy.array(fieldMagnitudes))
        centerGuess = fieldMagnitudes.dot(sweepPositions)/numpy.sum(fieldMagnitudes)
        
        self._guess = None
        def onclick(event):
            if event.button == 2:
                self._guess = event.xdata
                startPosition[sweepIndex] = Position(self._guess,'m')
                self.robot.setLocation(startPosition)
        pylab.gcf().canvas.mpl_connect('button_press_event', onclick)
        
        pylab.plot(sweepPositions,fieldMagnitudes)
        pylab.axvline(centerGuess)
        pylab.xlabel(sweepDirection)
        pylab.ylabel('magnitude')
        pylab.title('Click middle mouse button at the center of the trace and close')
        pylab.show()
        
        return (startPosition[0],startPosition[1])
        
    def findSampleCentreZPosition(self):
        oldAttenuation = self.analyzer.attenuatorPort1
        self.analyzer.attenuatorPort1 = PowerRatio(20,'dB')
        print 'Analyzer port 1 attenuator set to',self.analyzer.attenuatorPort1.asUnit('dB'),'dB'
        self.analyzer.measure(1,0)
        
        startPosition = self.robot.getLocation()
        while True:
            choice = raw_input('Press D (d) for (small) step down, U (u) for (small) step up, enter to confirm touchdown:')
            if choice == '':
                break
            elif choice == 'D':
                startPosition[2] -= 0.001
            elif choice == 'd':
                startPosition[2] -= 0.0001
            elif choice == 'U':
                startPosition[2] += 0.001
            elif choice == 'u':
                startPosition[2] += 0.0001
            else:
                print 'Choice not recognised, try again'
            self.robot.setLocation(startPosition)
#            self.analyzer.measure(1,0)
        
        self.analyzer.attenuatorPort1 = oldAttenuation
        print 'Analyzer port 1 attenuator restored to',self.analyzer.attenuatorPort1.asUnit('dB'),'dB'
        
        
        return startPosition[2]
        


        
    def calibrate(self):
        self.prepare()
        self.robot.getLocation()
        ## Find xy-position of standard with probe
        sweepDirection = {'Hx':'x', 'Hy':'y', 'Hz':'y', 'Ez':'y'}[self.calibration.name]
        standardCentreXYPosition = None
        while True:
            standardCentreXYPosition = self.findSampleCentreXYPosition(sweepDirection=sweepDirection)  
    #        standardCentreXYPosition = (Position(0.0049687,'m'), Position(-0.0251814516129,'m'))
            print 'Standard XY centre',standardCentreXYPosition
            retryAnswer = raw_input('Retry (y/n)? [n]')
            if retryAnswer != 'y':
                break
            
        
        ## Find z-position of standard with probe
        standardCentreZPosition = self.findSampleCentreZPosition()
#        standardCentreZPosition = Position(-47.533,unit='mm')
        print 'Standard-tip Z contact',standardCentreZPosition
        
        ## Find yz-laserposition of standard centre
        standardCentreLaserPosition = self.findSampleCentreLaserPosition()
#        standardCentreLaserPosition = Position([-2.7112 , -70.625 , 314.471774194],'mm')
        print 'Standard centre XYZ_laserpositioner:',standardCentreLaserPosition
        
        standardCentrePosition = Position([standardCentreXYPosition[0],
                                           standardCentreXYPosition[1],
                                           standardCentreZPosition+self.calibration.mechanical.spotZ],'m')
        self.calibration.mechanical.probeSpotLaser = standardCentreLaserPosition - standardCentrePosition

        
        #Electrical calibration
        # standard values are calculated with interpolate_fields.py:
        height = 5.0 #mm
        yOffsetMm = {'Hx':0.0,
                     'Hy':0.0,
                     'Hz':4.2,
                     'Ez':0.0}[self.calibration.name]
        
        field = {'Hx':1.48076893517,
                 'Hy':1.48076893517,
                 'Hz':1.04260360625,
                 'Ez':299.31}[self.calibration.name]
        
        
        self.setProbeLocation(standardCentreLaserPosition + Position([0,yOffsetMm,height],'mm'))
        standardToReceiverNetwork = self.analyzer.measure(1,0)
        standardToReceiverMeasurementVoltageForSquareWatt = SampledValues(standardToReceiverNetwork.f,numpy.sqrt(50.0) * standardToReceiverNetwork.s[:,-1,-1])
        print 'Measured at',standardToReceiverMeasurementVoltageForSquareWatt.frequencies[-1],'Hz: ',numpy.abs(standardToReceiverMeasurementVoltageForSquareWatt.values[-1]),'V/sqrt(W)'
        standardToFieldSimulation = SampledValues(standardToReceiverNetwork.f,numpy.array([field]*len(standardToReceiverNetwork.f)))
          
        
        self.calibration.electrical.performanceFactor=standardToReceiverMeasurementVoltageForSquareWatt/standardToFieldSimulation


        self.tearDown()        
        
class MechanicalProbeCalibration(SmartDommable):
    def __init__(self,spotZ = 0.0):
        self.probeSpotLaser = None
        self.spotZ = spotZ
    @property
    def calibrated(self):
        return bool(not type(self.probeSpotLaser) == type(None))
    def __str__(self):
        return 'Tip in laser coordinates '+ str(self.probeSpotLaser)

class ElectricalProbeCalibration(SmartDommable):    
    def __init__(self,name='',field='',performanceFactor=None):
        self.name = name
        self.field = field
        self.performanceFactor = performanceFactor
    def plot(self,*args,**kwargs):
        pylab.plot(numpy.array(self.performanceFactor.frequencies)/1e6,
                   20*numpy.log10(numpy.abs(numpy.array(self.performanceFactor.values))),*args,**kwargs)
        pylab.xlabel('$f$ (MHz)')
        pylab.ylabel('$20\log(|PF|)$ (dB$\Omega$m)')
        
    def show(self,*args,**kwargs):
        self.plot(*args,**kwargs)
        pylab.show()
        
    def nfsXml(self):    
        
        def arrayToString(array):
            return ' '.join(map(lambda x: str(x),array.tolist()))        
        
        return '''  <Probe>
    <Name>{name}</Name>
    <Field>{field}</Field>
    <Frequencies>
      <Unit>MHz</Unit>
      <List>{frequenciesMhz}</List>
    </Frequencies>
    <Perf_factor>
      <Unit_a>m</Unit_a>
      <Unit>{unit}</Unit>
      <Format>m</Format>
      <List>{values}</List>
    </Perf_factor>
  </Probe>'''.format(name=self.name,
                     field=self.field,
                     unit=('ohm.m' if self.field[0] == 'H' else 'm'),
                     frequenciesMhz=arrayToString(self.performanceFactor.frequencies/1e6),
                     values=arrayToString(20*numpy.log10(numpy.abs(self.performanceFactor.values))))






         
 
if __name__ == '__main__':
#    probeName = 'Hy'
#    spotZ = {'Ez' : Position(0),
#             'Hy' : Position(-0.0015,'m'),
#             'Hx' : Position(-0.0015,'m'),
#             'Hz' : Position(-0.0010,'m')}[probeName]        
#        
#    test = LaserPositionerCalibrator(probeName,spotZ)
#    test.calibrate()
#    test.calibration.toFile(test.calibration.name+'-candidate.xml')
        
#    laserPositioner = LaserPositioner(ProbeCalibration.fromFile('Hy3.xml'))
#    print laserPositioner.calibration.electrical.nfsXml()
#    laserPositioner.testMechanicalCalibration()
#
    def plotFile(name,label):
        calibration = ProbeCalibration.fromFile(name)
        calibration.electrical.plot(label=label)
        
    plotFile('Hy-candidate.xml','Hy (+2x 25dB)')
#    plotFile('Hy-before.xml','Hz (+2x 25dB)')
    
    pylab.title('Hz calibration check')
    pylab.legend()
    pylab.show()


