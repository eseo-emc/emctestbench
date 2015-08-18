from device import ScpiDevice
from amplifier import Amplifier

class RfpaAmp4g18g(Amplifier,ScpiDevice):
    terminationCharacters = {'read':'\r\n', 'write':''}
    defaultName = 'RFPA AMP4G18G Power Amplifier'
    defaultAddress = 'TCPIP0::192.168.18.189::10001::SOCKET'
    visaIdentificationStartsWith = 'rf65211111'
    
    def askIdentity(self):
        return self.ask('rf65211111')
           
    @property
    def temperature(self):
        temperatureString = self.ask('rf70100000')
        assert temperatureString.startswith('rf701')
        return float(temperatureString[5:])/10
        
    @property
    def rfOn(self):
        return {'rf80100010':True,
                'rf80100000':False}[self.ask('rf80100000')] 
    @rfOn.setter
    def rfOn(self,newValue):
        if newValue:
            self._turnRfOn()
        else:
            self._turnRfOff()
    
    def _turnRfOn(self):
        assert self.ask('rf81100010') == 'rf81100010', 'RFPA should echo this command literally'

    def _turnRfOff(self):
        assert self.ask('rf81100000') == 'rf81100000', 'RFPA should echo this command literally'

    def reset(self):
        assert self.ask('rf78100000') == 'rf78100000', 'RFPA should echo this command literally'

        
  
if __name__ == '__main__':
    import time    
    
    amplifier = RfpaAmp4g18g()
#    amplifier._deviceHandle.timeout = 10000
    
    print amplifier.askIdentity()
    
    amplifier.rfOn = True
    print 'On:',amplifier.rfOn    
    time.sleep(2)
    amplifier.rfOn = False
    print 'On:',amplifier.rfOn    
    
    print 'Temperature:',amplifier.temperature
    amplifier.reset()