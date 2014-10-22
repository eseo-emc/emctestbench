'''
@author: Sjoerd Op 't Land
'''

from pyvisa import visa
#import visa
from pyvisa import vpp43

import time
from gui import log
from PyQt4.QtCore import QObject,pyqtSignal
import sys

def Measurable(function):
    return 

class Device(QObject):
    changed = pyqtSignal()  
    
    def __init__(self,name=None):
        QObject.__init__(self)
        self._online = False
        if not name:
            self.name = self.defaultName
        else:
            self.name = name
    def __str__(self):
        return self.name + (' (Offline)' if not(self.online) else '')
    @property
    def detailedInformation(self):
        return self.__class__.__name__
    @property
    def iconName(self):
        return 'Stimulator'
        
    @property
    def online(self):
        return self._online
    @online.setter
    def online(self,newOnlineValue):
        if self._online != newOnlineValue:
            self._online = newOnlineValue
            self.changed.emit()
    def test(self):
        print 'Test'
    def putOnline(self):
        log.LogItem(str(self)+' has no putOnline implementation.',log.warning)
        return False
    def drawAttention(self):
        log.LogItem(str(self)+' has no drawAttention implementation.',log.warning)
    
class ScpiDevice(Device):
    def __init__(self,visaAddress=None,name=None):
        super(ScpiDevice,self).__init__(name)
        if visaAddress == None:
            visaAddress = self.defaultAddress
        self.visaAddress = visaAddress
        self._deviceHandle = None
    @property
    def detailedInformation(self):
        serialString = ''
        if self.online:        
            try:
                serialString = ' ,serial: ' + self.askIdentityItems()['serial number']
            except:
                pass
            
        return self.defaultName  + ' (' + self.visaAddress + serialString + ')'
    
    def write(self,message,logging=False,**kwargs):
        if not self._deviceHandle:
            self.putOnline()
            if self._deviceHandle == None:
                log.LogItem('Write error, {device} ({address}) is offline'.format(device=self,address=self.visaAddress),log.error)
                raise Exception        
        try:
            if logging:
                self.name, 'Writing:',message
            self._write(message,**kwargs)
        except:
#            log.LogItem(str(sys.exc_info()[1]),log.error)
            log.LogItem('Error with {device} ({address}) when trying to write "{message}"\n{moreError}'.format(device=self,message=message,address=self.visaAddress,moreError=str(sys.exc_info()[1])),log.error)
            raise             
    
    def _write(self,message):
        self._deviceHandle.write(message)
        
    def ask(self,message):
        self.write(message)
        try:
            readData = self._deviceHandle.read()
        except:
            log.LogItem('Error with {device} ({address}) when trying to ask "{message}"\n{moreError}'.format(device=self,message=message,address=self.visaAddress,moreError=str(sys.exc_info()[1])),log.error)
            raise             
#        print self.name, 'Read back:', readData
        return readData
            
    def ask_for_values(self,message,format=None):
        self.write(message)
        return self._deviceHandle.read_values(format)
    
    def _putOffline(self):
        if self._deviceHandle:
            self._deviceHandle.close()
            self._deviceHandle = None
        self.online = False
        
    def putOnline(self):
        self._putOffline() #TODO: find a way of checking the status of a connection, disconnecting every time is a bit expensive
        log.LogItem('Trying to connect to '+self.visaAddress+'...',log.debug)
        if self._deviceHandle == None:
#            try:
                self.createHandle()
#            except Exception:
#                pass
        if self._deviceHandle:
            log.LogItem('Connected, verifiying identity of '+self.visaAddress+'...',log.debug)
            self.online = self.identify()
        else:
            log.LogItem(self.visaAddress+' was offline',log.info)
            self.online = False
     
    def createHandle(self):
        self._deviceHandle = visa.instrument(self.visaAddress)
            
    def popError(self):
        return self.ask('SYSTem:ERRor?')

    def __del__(self):
        self._putOffline()
    def reset(self):
        self.write('*RST')
    def clear(self):
        self.write('CLR')
        
    def armServiceRequestOnOperationComplete(self):
        self.write('*CLS; *ESE 1; *SRE 32')   
    def waitForServiceRequest(self,poll=False,pollInterval=0.01,maxPolls=1000):
        if poll:
            for srqPollNumber in range(maxPolls):
                if self.readStatusByte() & 0x40:
                    break
            else:
                raise Exception,'Waiting for Service ReQuest bit to be set took longer than {timeOut}s'.format(timeOut=maxPolls*pollInterval)
            
            assert int(self.ask('ESR?')) & 0x01,"OPC bit of Event Status Register A should be set"

            for zeroStatusPollNumber in range(maxPolls):
                if self.readStatusByte() == 0:
                    break
            else:
                raise Exception,'Waiting for Status Byte to become NULL longer than {timeOut}s'.format(timeOut=maxPolls*pollInterval)

            
            print 'Polled',srqPollNumber,'times for SRQ, ',zeroStatusPollNumber,'times for 0 status byte.'

        else:            
            self._deviceHandle.wait_for_srq()
    def waitUntilReady(self,timeOut=15):
        self.write('*OPC') # let OPeration Complete bit be set upon finish
        if hasattr(self._deviceHandle,'wait_for_srq'):
            self.write('*ESE 1') # OPeration Complete -> Event Status sum Bit
            self.write('*SRE 32') # ESB -> Service ReQuest
            self._deviceHandle.wait_for_srq(timeOut)
        else:
            for waitingPeriod in range(timeOut*10):
                if int(self.ask('*ESR?')) & 0x01:
                    break
                time.sleep(0.1)
            else:
                raise Exception,'Waiting for OPeration Complete bit to be set took longer than {timeOut}s'.format(timeOut=timeOut)
    def readStatusByte(self):
        return self._deviceHandle._vpp43.read_stb(self._deviceHandle.vi)

    def interface(self):
        interfaceName = self._deviceHandle._vpp43.get_attribute(self._deviceHandle.vi,self._deviceHandle._vpp43.VI_ATTR_RSRC_NAME).split('::')[0] + '::INTFC'
        return visa.Interface(interfaceName)
    def printInterfaceStatus(self):
        interface = self.interface()
        vpp43 = interface._vpp43
        assertedStates = {vpp43.VI_STATE_ASSERTED : 'asserted',
                          vpp43.VI_STATE_UNASSERTED : 'unasserted',
                          vpp43.VI_STATE_UNKNOWN : 'unknown'}
        addressedStates = {vpp43.VI_GPIB_UNADDRESSED : 'unadressed',
                         vpp43.VI_GPIB_TALKER : 'talker',
                         vpp43.VI_GPIB_LISTENER : 'listener'}
        booleanStates = {vpp43.VI_TRUE : 'true',
                         vpp43.VI_FALSE : 'false'}
        print interface
        print 'Primary address:   ', vpp43.get_attribute(interface.vi,vpp43.VI_ATTR_GPIB_PRIMARY_ADDR)
        print 'Secondary address: ', vpp43.get_attribute(interface.vi,vpp43.VI_ATTR_GPIB_SECONDARY_ADDR)
        print 'Addressed:         ', addressedStates[vpp43.get_attribute(interface.vi,vpp43.VI_ATTR_GPIB_ADDR_STATE)]
        print 'System Controller: ', booleanStates[vpp43.get_attribute(interface.vi,vpp43.VI_ATTR_GPIB_SYS_CNTRL_STATE)]        
        print '- ATtentioN:            ', assertedStates[vpp43.get_attribute(interface.vi,vpp43.VI_ATTR_GPIB_ATN_STATE)]
        print '- Controller In Charge: ', booleanStates[vpp43.get_attribute(interface.vi,vpp43.VI_ATTR_GPIB_CIC_STATE)]
        print '- Not Data ACcepted:    ', assertedStates[vpp43.get_attribute(interface.vi,vpp43.VI_ATTR_GPIB_NDAC_STATE)]
        print '- Service ReQuest:      ', assertedStates[vpp43.get_attribute(interface.vi,vpp43.VI_ATTR_GPIB_SRQ_STATE)]
        print '- Remote ENable:        ', assertedStates[vpp43.get_attribute(interface.vi,vpp43.VI_ATTR_GPIB_REN_STATE)]
        
        
        
     
    def askIdentity(self):
        return self.ask('*IDN?')
    def askIdentityItems(self):
        identityItems = self.askIdentity().split(',')
        return {'mark':identityItems[0],'type':identityItems[1],'serial number':identityItems[2],'firmware version':identityItems[3]}
    def identify(self):
        identityString = self.askIdentity()
        if identityString.startswith(self.visaIdentificationStartsWith):
            log.LogItem('Identify succes, got "'+identityString+'".',log.debug)
            return True
        else:
            log.LogItem('Failed to identify, got "'+identityString+'", expected it to start with "'+self.visaIdentificationStartsWith+'"',log.warning)
            return False
        
    def drawAttention(self):
        self.displayText(self.name)
        self.beep()
        time.sleep(2)
        self.write('DISPlay:TEXT:CLEar')
        self.beep()
    def beep(self):
        self.write('SYSTem:BEEPer')
    def displayText(self,message):
        self.write('DISPlay ON')
        self.write('DISP:TEXT "'+message+'";')

if __name__ == '__main__':
    from agilent33 import Agilent33220A,Agilent33250A
    from agilentl4411a import AgilentL4411a
    from agilentn6700b import AgilentN6700b
    testDevice = Agilent33220A('TCPIP0::172.20.1.204::inst0::INSTR','33220 LF Generator top')
#    testDevice = Agilent33250A('GPIB1::10::INSTR')
#    testDevice = AgilentL4411a('TCPIP0::172.20.1.207::inst0::INSTR')
#    testDevice = AgilentN6700b('TCPIP0::172.20.1.203::inst0::INSTR')
    print testDevice
    testDevice.drawAttention()