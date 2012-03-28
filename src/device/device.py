'''
@author: Sjoerd Op 't Land
'''

import visa
import time

class Device(object):
    '''
    Abstract superclass for all physical measurement device agents.
    '''
    def __init__(self,name=None):
        if not name:
            self.name = self.defaultName
        else:
            self.name = name
    def __str__(self):
        return self.name
    @property
    def detailedInformation(self):
        return self.__class__.__name__
    @property
    def iconName(self):
        return 'Stimulator'
    
class ScpiDevice(Device):
    def __init__(self,visaAddress=None,name=None):
        super(ScpiDevice,self).__init__(name)
        if visaAddress == None:
            visaAddress = self.defaultAddress
        self.visaAddress = visaAddress
        self.connected = False
        self._deviceHandle = None
    @property
    def detailedInformation(self):
#        return super(ScpiDevice,self).detailedInformation + ' ' + self.visaAddress
        return self.defaultName  + ' ' + self.visaAddress
    
    def write(self,message):
        if not self._deviceHandle:
            assert self.tryConnect()
#        else:
#            print 'Would write to {address}: "{message}"'.format(message=message,address=self.visaAddress)
        self._deviceHandle.write(message)
    def ask(self,message):
        if not self._deviceHandle:
            assert self.tryConnect()
#        else:
#            print 'Would ask from {address}: "{message}"'.format(message=message,address=self.visaAddress)
        return self._deviceHandle.ask(message)
            
    def ask_for_values(self,message):
        return self._deviceHandle.ask_for_values(message)
    
    def tryConnect(self):
        if self._deviceHandle == None:
            try:
                self._deviceHandle = visa.instrument(self.visaAddress)
            except Exception:
                pass
        if self._deviceHandle:
            self.connected = self.identify()
        else:
            self.connected = None
        return self.connected
    def popError(self):
        return self.ask('SYSTem:ERRor?')
    def __str__(self):
        return self.name + (' (Offline)' if not(self.connected) else '')
    def __del__(self):
        if self.connected:
            self._deviceHandle.close()
    def reset(self):
        self.write('*RST')
    def askIdentity(self):
        return self.ask('*IDN?')
    def identify(self):
        return self.askIdentity().startswith(self.visaIdentificationStartsWith)
        
    def drawAttention(self):
        if self.connected:
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
    testDevice.tryConnect()
    print testDevice
    testDevice.drawAttention()