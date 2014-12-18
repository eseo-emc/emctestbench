
from device import Device
from rangefinder import RangeFinder
from utility import quantities
import time
import numpy
import llt

class ScanControl2600(RangeFinder,Device):
    defaultName = 'ScanControl 2600'
    documentation = {'Programmers Manual':''}
    
    widthToY = +1.0
    distanceToZ = +1.0

    
    def __init__(self):
        self._deviceHandle = llt.Llt(llt.INTF_TYPE_ETHERNET)
        Device.__init__(self)
        
        
    
    def putOnline(self):
        interfaceNumber = self._deviceHandle.getDeviceInterfaces(fast=True)
        self._deviceHandle.setDeviceInterface(interfaceNumber)
        self._deviceHandle.connect()
        self._online = True        
        self.laserOn = False
        

    def prepare(self):
        if not self._online:
            self.putOnline()
        self._deviceHandle.resolution = 640
        self._deviceHandle.profileConfiguration = llt.PROFILE
        self._deviceHandle.configureRight()
        self._deviceHandle.bufferCount = 2
        self._deviceHandle.holdBuffersForPolling = 1
        
        self._deviceHandle.transferProfiles(llt.SHOT_TRANSFER,True)
#        time.sleep(0.5)
    
    def tearDown(self):
        self._deviceHandle.transferProfiles(llt.SHOT_TRANSFER,False)
        self._deviceHandle.close()
    

    @property
    def laserOn(self):
        return self._deviceHandle.laserOn
    @laserOn.setter
    def laserOn(self,value):
        self._deviceHandle.laserOn = value
        
    def getProfile(self):
        oldLaserOn = self.laserOn
        if not oldLaserOn:
            self.laserOn = True
            time.sleep(0.1)
        
        #horrible workaround to cope with network (?) delays, for the driver buffers are already limited to 1 frame...
        self._deviceHandle.multiShot(1)
        pollCount = 0
        while True:        
            try:       
                profile = self._deviceHandle.actualProfile()
            except Exception,e:
                if '-104' in str(e):
                    pollCount += 1
                    continue
                else:
                    raise
            else:
                break
#        print 'Had to wait',pollCount,'buffers before receiving anything'

        


        self.laserOn = oldLaserOn
        validSamples = (profile['z'] != 0)
        profile['x'][validSamples == False] = numpy.NaN 
        profile['z'][validSamples == False] = numpy.NaN
        
        return {'y':quantities.Position(self.widthToY*profile['x'],'mm'),
                'z':quantities.Position(self.distanceToZ*profile['z'],'mm'),
                'm0':profile['m0'],
                'validSamples':validSamples}
            
if __name__ == '__main__':
    device = ScanControl2600()
    device.prepare()
    profile = device.getProfile()
    device.tearDown()
    
    import pylab
    pylab.axis('equal')
#    pylab.plot(profile['y'],profile['m0'],'-')
    pylab.plot(profile['y'].asUnit('mm'),profile['z'].asUnit('mm'),'x-')
    pylab.xlabel('y (mm)')
    pylab.ylabel('z (mm)')
    pylab.show()
    
