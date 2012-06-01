'''
@author: Sjoerd Op 't Land
'''

import visa
from pyvisa import vpp43

import time
from gui import logging
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
        logging.LogItem(str(self)+' has no putOnline implementation.',logging.warning)
        return False
    def drawAttention(self):
        logging.LogItem(str(self)+' has no drawAttention implementation.',logging.warning)
    
class ScpiDevice(Device):
    def __init__(self,visaAddress=None,name=None):
        super(ScpiDevice,self).__init__(name)
        if visaAddress == None:
            visaAddress = self.defaultAddress
        self.visaAddress = visaAddress
        self._deviceHandle = None
    @property
    def detailedInformation(self):
        return self.defaultName  + ' ' + self.visaAddress
    
    def write(self,message):
        if not self._deviceHandle:
            self.putOnline()
        try:
            self._deviceHandle.write(message)
        except:
#            logging.LogItem(str(sys.exc_info()[1]),logging.error)
            logging.LogItem('Write error, {address} was offline when trying to write "{message}"'.format(message=message,address=self.visaAddress),logging.error)
#            raise             
            
    def ask(self,message):
        self.write(message)
        return self._deviceHandle.read()
            
    def ask_for_values(self,message):
        self.write(message)
        return self._deviceHandle.read_values(message)
    
    def _putOffline(self):
        if self._deviceHandle:
            self._deviceHandle.close()
            self._deviceHandle = None
        self.online = False
        
    def putOnline(self):
        self._putOffline() #TODO: find a way of checking the status of a connection, disconnecting every time is a bit expensive
        logging.LogItem('Trying to connect to '+self.visaAddress+'...',logging.debug)
        if self._deviceHandle == None:
            try:
                self._deviceHandle = visa.instrument(self.visaAddress)
            except Exception:
                pass
        if self._deviceHandle:
            logging.LogItem('Connected, verifiying identity of '+self.visaAddress+'...',logging.debug)
            self.online = self.identify()
        else:
            logging.LogItem(self.visaAddress+' was offline',logging.info)
            self.online = False
        
            
    def popError(self):
        return self.ask('SYSTem:ERRor?')

    def __del__(self):
        self._putOffline()
    def reset(self):
        self.write('*RST')
    def clear(self):
        self.write('CLR')
    def askIdentity(self):
        return self.ask('*IDN?')
    def identify(self):
        identityString = self.askIdentity()
        if identityString.startswith(self.visaIdentificationStartsWith):
            logging.LogItem('Identify succes, got "'+identityString+'".',logging.debug)
            return True
        else:
            logging.LogItem('Failed to identify, got "'+identityString+'", expected it to start with "'+self.visaIdentificationStartsWith+'"',logging.warning)
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