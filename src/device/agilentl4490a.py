from device import ScpiDevice
from switch import Switch

class AgilentL4490a(Switch,ScpiDevice):
    defaultName = "Agilent L4490a Switching Platform"
    visaIdentificationStartsWith = 'Agilent Technologies,L4490A,'
    
    def __init__(self,visaAddress):
        super(AgilentL4490a,self).__init__(visaAddress)

        self._switchMapping = { \
            'GeneratorToBridge':    1103, 
            'GeneratorToPrana':     1105, 
            'GeneratorToMilmega':   1106, 
            'GeneratorOpen':        1108, 
                                         
            'DUTtoSAorVNA':         1112,
            'BridgeToDUT':          1113, 
            'PranaToDUT':           1115, 
            'MilmegaToDUT':         1116, 
            'DUTOpen':              1118, 
                                         
            'PranaIncidentToPM':    1125, 
            'MilmegaIncidentToPM':  1126, 
            'IncidentOpen':         1128, 
                                         
            'BridgeReflectedToPM':  1133, 
            'PranaReflectedToPM':   1135, 
            'MilmegaReflectedToPM': 1136, 
            'ReflectedOpen':        1138 \
        }
        
    def reset(self):
        self.deviceHandle.write('ROUT:CHAN:VER:ENAB ON,(@1102:1138)') #TODO: take minimum an maximum of switchMapping
        
    def closeSwitch(self,switchName):
        self.deviceHandle.write('ROUT:CLOS (@%d)' % self._switchMapping[switchName]);
    def readSwitch(self,switchName):
        closeString = self.deviceHandle.ask('ROUT:CLOS? (@%d)' % self._switchMapping[switchName]);
        return closeString == '1'
        
  
if __name__ == '__main__':
    switchPlatform = AgilentL4490a()
    assert switchPlatform.tryConnect()
    switchPlatform.reset()
    switchPlatform.closeSwitch('DUTtoSAorVNA')
    print switchPlatform.readSwitch('DUTtoSAorVNA')
    
    

#     
#     ampli prana 5
#     * ID
#     MHF # on
#     AHF # off
#     
#     ampli milmega 6
#     OUT4 1 # LINE ON
#     OUT4 0 # LINE OFF
#     OUT1 1 # RF ON
#     OUT1 0 # RF OFF
#     OUT3 0 # Band 1
#     OUT3 1 # Band 2
#     
#     frequency meter 206
#     
#     multimeter 207
#     
#     dso 208
    
    
    