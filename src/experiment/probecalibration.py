"""

preamp
http://www.everythingrf.com/rf-microwave-amplifiers/p/Planar-Monolithics-Industries-82_PEC_60_0R14R0_5R0_10_12_SFF

@author: Sjoerd Op 't Land
"""
import numpy
import time
from matplotlib import pyplot
import sys
from utility.sampledvalues import SampledValues
from result.persistance import SmartDommable
import pylab

import device
from device.spectrumanalyzer import SpectrumAnalyzer
from utility.quantities import Amplitude,Voltage,Current,Position,Frequency,PowerRatio,Power


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
        self.robot.setLocation(pointLaserPosition-self.calibration.mechanical.probeSpotLaser,*args,**kwargs)
    def getProbeLocation(self):
        return self.robot.getLocation()+self.calibration.mechanical.probeSpotLaser
        
        
    def getProfile(self):
        positionJustBefore = self.robot.getLocation()
        profile = self.laser.getProfile()
        positionJustAfter = self.robot.getLocation()
#        print positionJustAfter-positionJustBefore  
        
        averagePosition = ((positionJustAfter+positionJustBefore)/2)
        return Position([numpy.zeros(profile['y'].shape)+averagePosition[0],
                                            profile['y']+averagePosition[1],
                                            profile['z']+averagePosition[2]],unit='m')
                        
    def pickLaserPosition(self,targetDescription,dataCallBack=None):   
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
        self.powerSupply.setChannelParameters(4,Voltage(12.0,'V'),Current(0.7,'A'))
        self.powerSupply.turnChannelOn(4)
        
    def tearDown(self):
        self.powerSupply.turnChannelOff(4)
        LaserPositioner.tearDown(self)
        
    def findSampleCentreLaserPosition(self):
        return self.pickLaserPosition('the top of the center of the trace')        

    def findSampleCentreXYPosition(self):
        raw_input('Put probe just above sample for electrical maximum y-search')
        startPosition = self.robot.getLocation()
        
        yPositions = []
        fieldMagnitudes = []
        for deviation in numpy.arange(-0.007,0.007,0.0005):
            tryPosition = startPosition.copy()
            tryPosition[1] += deviation
            yPositions.append(tryPosition[1])
            self.robot.setLocation(tryPosition)
            fieldMagnitudes.append(self.analyzer.measure(1,0).s[-1,-1,-1])
            
        yPositions = numpy.array(yPositions)
        fieldMagnitudes = numpy.abs(numpy.array(fieldMagnitudes))
        yCenterGuess = fieldMagnitudes.dot(yPositions)/numpy.sum(fieldMagnitudes)
        
        self._guess = None
        def onclick(event):
            if event.button == 2:
                self._guess = event.xdata
                startPosition[1] = Position(self._guess,'m')
                self.robot.setLocation(startPosition)
        pylab.gcf().canvas.mpl_connect('button_press_event', onclick)
        
        pylab.plot(yPositions,fieldMagnitudes)
        pylab.axvline(yCenterGuess)
        pylab.xlabel('y')
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
        ## Find y-position of standard with probe
        standardCentreXYPosition = None
        while True:
            standardCentreXYPosition = self.findSampleCentreXYPosition()  
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
        # standard:
        height = 5.0 #2.0 #mm, 1.0        
        hField = 1.48076893517 #4.75942841396 #A/m/sqrt(W), 7.55
#        eField =         
        
        self.setProbeLocation(standardCentreLaserPosition + Position([0,0,height],'mm'))
        standardToReceiverNetwork = self.analyzer.measure(1,0)
        standardToReceiverMeasurementVoltageForSquareWatt = SampledValues(standardToReceiverNetwork.f,numpy.sqrt(50.0) * standardToReceiverNetwork.s[:,-1,-1])
        print 'Measured at',standardToReceiverMeasurementVoltageForSquareWatt.frequencies[-1],'Hz: ',numpy.abs(standardToReceiverMeasurementVoltageForSquareWatt.values[-1]),'V/sqrt(W)'
        standardToFieldSimulation = SampledValues(standardToReceiverNetwork.f,numpy.array([hField]*len(standardToReceiverNetwork.f)))
          
        
        self.calibration.electrical.performanceFactor=standardToReceiverMeasurementVoltageForSquareWatt/standardToFieldSimulation


        self.tearDown()        
        
class MechanicalProbeCalibration(SmartDommable):
    def __init__(self,spotZ = 0.0):
        self.probeSpotLaser = None
        self.spotZ = spotZ
    def __str__(self):
        return 'Tip in laser coordinates '+ str(self.probeSpotLaser)

class ElectricalProbeCalibration(SmartDommable):    
    def __init__(self,name='',field='Hy',performanceFactor=None):
        self.name = name
        self.field = field
        self.performanceFactor = performanceFactor
        
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
        
    test = LaserPositionerCalibrator('Hy',Position(-0.0015,'m'))
    test.calibrate()
    test.calibration.toFile(test.calibration.name+'.xml')
#        
#    laserPositioner = LaserPositioner(ProbeCalibration.fromFile('Hy3.xml'))
#    print laserPositioner.calibration.electrical.nfsXml()
#    laserPositioner.testMechanicalCalibration()



