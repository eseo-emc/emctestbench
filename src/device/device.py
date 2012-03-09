'''
@author: Sjoerd Op 't Land
'''

import visa

class Device(object):
    '''
    Abstract superclass for all physical measurement device agents.
    '''
    def __init__(self,name=None):
        if not name:
            self.name = self.defaultName
        else:
            self.name = name
    @property
    def detailedInformation(self):
        return self.__class__.__name__
    @property
    def iconName(self):
        return 'Stimulator'
    
class ScpiDevice(Device):
    def __init__(self,visaAddress,name=None):
        super(ScpiDevice,self).__init__(name)
        self.visaAddress = visaAddress
        self.connected = False
        self.deviceHandle = None
    @property
    def detailedInformation(self):
#        return super(ScpiDevice,self).detailedInformation + ' ' + self.visaAddress
        return self.defaultName  + ' ' + self.visaAddress
        
    def tryConnect(self):
        if self.deviceHandle == None:
            try:
                self.deviceHandle = visa.instrument(self.visaAddress)
            except Exception:
                pass
        if self.deviceHandle:
            self.connected = self.identify()
        else:
            self.connected = None
        return self.connected
        
    def __str__(self):
        return self.name + (' (Offline)' if not(self.connected) else '')
    def __del__(self):
        if self.connected:
            self.deviceHandle.close()
            
    def askIdentity(self):
        return self.deviceHandle.ask('*IDN?')
    def identify(self):
        return self.askIdentity().startswith(self.visaIdentificationStartsWith)