import time
import numpy

from device import ScpiDevice
from positioner import Positioner
from utility import quantities

class NewportEsp300Error(object):
    def __init__(self,errorCode,errorDescription,timeStamp):
        self.errorCode = errorCode
        self.errorDescription = errorDescription
        self.timeStamp = timeStamp
    def __repr__(self):
        return 'Newport error {errorCode}: "{errorDescription}"'.format(errorCode=self.errorCode,errorDescription=self.errorDescription)

class NewportEsp300(Positioner,ScpiDevice):
    defaultName = 'Newport ESP300 Motion Controller'
    defaultAddress = 'GPIB1::1::INSTR'
    visaIdentificationStartsWith = 'M-IMS300PP, '
    documentation = {'Programmers Manual':'http://phubner.eng.ua.edu/Files/ESP300.pdf'}
        
    def __init__(self):
        Positioner.__init__(self)
        ScpiDevice.__init__(self)

        self.axesGrouped = None
        self.homed = None
#        #self.deviceHandle = visa.instrument('TCPIP0::172.20.1.202::inst0::INSTR')
#        self.deviceHandle = visa.instrument('GPIB1::1::INSTR', timeout = 10)
    def askIdentity(self):
        return self.ask('1 ID ?')
    def reset(self):
        self.write('RS')
        time.sleep(12)
        self.clear()
    def clear(self):
        for errorNumber in range(10):
            error = self._popError()
            if error == None:
                break
        else:
            raise Exception, 'Popping 10 errors was not enough to empty the Newport error queue'

    def _createGroup(self):
        if self.axesGrouped is not True:
            self._writeAndCheckError('1 HN 1,2,3',acceptErrorDescription="GROUP NUMBER ALREADY ASSIGNED") # create group 1, all axes together
            self._writeAndCheckError('1 HV 50.0') # max velocity, must be defined!
            self._writeAndCheckError('1 HA 30.0') # max acceleration
            self._writeAndCheckError('1 HD 10.0') # max deceleration
            self._writeAndCheckError('1 HO') # activate
            self.axesGrouped = True
    def _deleteGroup(self):
        if self.axesGrouped is not False:
            self._writeAndCheckError('1 HX')
            self.axesGrouped = False

    def putOnline(self):
        ScpiDevice.putOnline(self)
#        self._deviceHandle.term_chars = '\r'
        if self._deviceHandle:
            self.clear()
#        self.reset()
#        self._turnOnAndHome()
    def prepare(self):
        pass

    def tearDown(self):
        self._deleteGroup()
            
    def _popError(self):
        lastErrorMessage = self.ask('TB?').split(', ')
#        print 'Got error:',lastErrorMessage
        errorCode = int(lastErrorMessage[0])
        if errorCode != 0:
            timeStamp = int(lastErrorMessage[1])
            errorDescription = lastErrorMessage[2]      
            return NewportEsp300Error(errorCode,errorDescription,timeStamp)
        else:
            return None
    def _raiseIfError(self,acceptErrorDescription=None):
        error = self._popError()
        if error and error.errorDescription != acceptErrorDescription:
            raise Exception, '{error} upon command "{command}"'.format(error=error,command=command)
            
            
    def write(self,command):
#        print 'Newport300.write',command
        ScpiDevice.write(self,command + '; RQ')
        self._deviceHandle.wait_for_srq(15)
    def _writeAndCheckError(self,command,acceptErrorDescription=""):
        self.write(command)
        self._raiseIfError(acceptErrorDescription)
    def _turnOnAndHome(self,axis=None):
        self._deleteGroup()
        def homeAxis(axis):
            if axis:
                self._writeAndCheckError('{axis} MO'.format(axis=axis))
                self._writeAndCheckError('{axis} OR'.format(axis=axis))
                self._waitUntilMotionDone(axis)
            else:
                homeAxis(3)
                homeAxis(2)
                homeAxis(1)
        homeAxis(axis)
        self.homed = True
    def _motionDone(self,axis):
        if axis:
            query = '{axis} MD?'.format(axis=axis)
            motionDoneString = self.ask(query)
            if motionDoneString == '1':
                return True
            elif motionDoneString == '0':
                return False
            else:
                raise ValueError, "{query} resulted in '{motionDoneString}'".format(query=query,motionDoneString=motionDoneString)
        else:
            return self._motionDone(1) and self._motionDone(2) and self._motionDone(3)
    def _waitUntilMotionDone(self,axis=None):
        if axis:     
#            self.write('{axis:d} WS 0'.format(axis=axis)) # wait for motion stop
            while not(self._motionDone(axis)):
                time.sleep(0.2)
            self._raiseIfError()
        else:
            self._waitUntilMotionDone(1)
            self._waitUntilMotionDone(2)
            self._waitUntilMotionDone(3)
                
   
    def getLocation(self):
        if self.homed is not True:
            self._turnOnAndHome()
        self._createGroup()
        coordinateStrings = self.ask('1 HP?').split(', ')
        self._deleteGroup()
        return quantities.Position([float(coordinateStrings[0]),float(coordinateStrings[1]),float(coordinateStrings[2])],'mm')

    def setLocation(self,newLocation):
        if self.homed is not True:
            self._turnOnAndHome()
        self._createGroup()
        self.write('1 HL {newLocation[0]:f}, {newLocation[1]:f}, {newLocation[2]:f}'.format(newLocation=newLocation.asUnit('mm')))
        self._waitUntilMotionDone()
        self._deleteGroup()
        return self.getLocation()
        
if __name__ == '__main__':
    test = NewportEsp300()
#    test.reset()
#    for x in numpy.linspace(10,20,11):
#        test.setLocation(quantities.Position([0+x,0,0],'mm'))
#    test.tearDown()
#    test.putOnline()
    
#    print test.askIdentity()
#    for repetition in range(1000):
#        print 'Try',repetition
#        test._turnOnAndHome()
#     test.setLocation([0.,0.,0.])     
     
    while True:
        for x in numpy.linspace(0,140,15):
            print test.setLocation(quantities.Position([65.+x,-23.,35.],'mm'))
        print test.setLocation(quantities.Position([0.,0.,0.],'mm'))
#     while True:
#         
#         for x in numpy.linspace(128,116,15):
#             test.setLocation([x,-38.,35.])
#         test.setLocation([0.,0.,0.])
# 
#     print 'Go'
#     print test.setLocation(51)
# #     test.setLocation(test.getLocation()-100)
#     print 'Returned'