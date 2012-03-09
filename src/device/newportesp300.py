import time
import numpy

from device import ScpiDevice
from positioner import Positioner

class NewportEsp300Error(object):
    def __init__(self,errorCode,errorDescription,timeStamp):
        self.errorCode = errorCode
        self.errorDescription = errorDescription
        self.timeStamp = timeStamp
    def __repr__(self):
        return 'Newport error {errorCode}: "{errorDescription}"'.format(errorCode=self.errorCode,errorDescription=self.errorDescription)

class NewportEsp300(Positioner,ScpiDevice):
    defaultName = 'Newport ESP300 Motion Controller'
    visaIdentificationStartsWith = 'M-IMS300PP, '
    documentation = {'Programmers Manual':'http://phubner.eng.ua.edu/Files/ESP300.pdf'}
        
#    def __init__(self,initialize=True):
#        #self.deviceHandle = visa.instrument('TCPIP0::172.20.1.202::inst0::INSTR')
#        self.deviceHandle = visa.instrument('GPIB1::1::INSTR', timeout = 10)
    def askIdentity(self):
        return self.deviceHandle.ask('1 ID ?')

    def createGroup(self):
        self.writeSafe('1 HN 1,2,3',acceptErrorDescription="GROUP NUMBER ALREADY ASSIGNED") # create group 1, all axes together
        self.writeSafe('1 HV 50') # max velocity, must be defined!
        self.writeSafe('1 HA 30') # max acceleration
        self.writeSafe('1 HD 10') # max deceleration
        self.writeSafe('1 HO') # activate
    def deleteGroup(self):
        self.writeSafe('1 HX')
    def initialize(self):
        self.turnOnAndHome()
            
    def __del__(self):
        print 'Closing the %s...' % self.__class__.__name__
        self.deviceHandle.close()
    def popError(self):
        lastErrorMessage = self.deviceHandle.ask('TB?').split(', ')
        
        errorCode = int(lastErrorMessage[0])
        if errorCode != 0:
            timeStamp = int(lastErrorMessage[1])
            errorDescription = lastErrorMessage[2]      
            return NewportEsp300Error(errorCode,errorDescription,timeStamp)
        else:
            return None
    def writeSafe(self,command,acceptErrorDescription=""):
        self.deviceHandle.write(command)
        error = self.popError()
        if error and error.errorDescription != acceptErrorDescription:
            raise Exception, '{error} upon command "{command}"'.format(error=error,command=command)
    def turnOnAndHome(self,axis=None):
        if axis:
            self.writeSafe('{axis} MO'.format(axis=axis))
            self.writeSafe('{axis} OR'.format(axis=axis))
            self.waitUntilMotionDone(axis)
        else:
            self.turnOnAndHome(3)
            self.turnOnAndHome(2)
            self.turnOnAndHome(1)
    def motionDone(self,axis):
        if axis:
            query = '{axis} MD?'.format(axis=axis)
            motionDoneString = self.deviceHandle.ask(query)
            if motionDoneString == '1':
                return True
            elif motionDoneString == '0':
                return False
            else:
                raise ValueError, "{query} resulted in '{motionDoneString}'".format(query=query,motionDoneString=motionDoneString)
        else:
            return self.motionDone(1) and self.motionDone(2) and self.motionDone(3)
    def waitUntilMotionDone(self,axis=None):
        # # using '1 WS 0' method only works sometimes, because the deviceHandle.timeout doesn't always seem to be observed
        # self.writeSafe('1 WS 0') # wait for motion stop
        # checkLocation = self.getLocation()# dirty hack to actually wait for Newports wait...
                
        # # therefore we use 200 ms polling :(
        # while abs(self.getLocation()-newLocation) > 0.001:
        #     time.sleep(0.2)
        while not(self.motionDone(axis)):
            time.sleep(0.2)
        error = self.popError()
        if error:
            raise Exception, '{error} occured while waiting for the motion to be done.'.format(error=error)
        
    def getLocation(self):
        self.createGroup()
        coordinateStrings = self.deviceHandle.ask('1 HP?').split(', ')
        self.deleteGroup()
        return numpy.array([float(coordinateStrings[0]),float(coordinateStrings[1]),float(coordinateStrings[2])])

    def setLocation(self,newLocation):
        self.createGroup()
        test.writeSafe('1 HL {newLocation[0]:f}, {newLocation[1]:f}, {newLocation[2]:f}'.format(newLocation=newLocation))
        self.deleteGroup()
        self.waitUntilMotionDone()
        return self.getLocation()
        
if __name__ == '__main__':
    test = NewportEsp300()
    assert test.tryConnect()
#     test.initialize()
#     while True:
#         test.initialize()
#         for x in numpy.linspace(0,140,15):
#             test.setLocation([65.+x,-23.,35.])
#         test.setLocation([0.,0.,0.])
#     while True:
#         
#         for x in numpy.linspace(128,116,15):
#             test.setLocation([x,-38.,35.])
#         test.setLocation([0.,0.,0.])
 
#     print 'Go'
#     print test.setLocation(51)
# #     test.setLocation(test.getLocation()-100)
#     print 'Returned'