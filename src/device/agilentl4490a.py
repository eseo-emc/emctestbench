from device import ScpiDevice
from switch import SwitchPlatform,Switch
import time
    
class AgilentSwitch(Switch):
    def __init__(self,parent,mapping):
        self.parent = parent
        Switch.__init__(self,mapping)

    def setPosition(self,positionName):
        self.parent.write('ROUT:CLOS (@{positionCode:d})'.format(positionCode=self[positionName]))
    def _readPosition(self,positionName):
        closeString = self.parent.ask('ROUT:CLOS? (@{positionCode:d})'.format(positionCode=self[positionName]))
        return closeString == '1'

class AgilentL4490a(SwitchPlatform,ScpiDevice):
    defaultName = 'Agilent L4490A Switching Platform'
    defaultAddress = 'TCPIP0::192.168.18.181::inst0::INSTR'
    visaIdentificationStartsWith = 'Agilent Technologies,L4490A,'
    
    def __init__(self,*args,**kwargs):
        ScpiDevice.__init__(self,*args,**kwargs)
        SwitchPlatform.__init__(self,{ \
            'generator':AgilentSwitch(self,{ \
                'Prana':   1102,
                'coupler': 1103, 
                'Milmega':         1105, 
                'RFPA':       1106, 
                'open':          1108 \
            }),
            'DUT':AgilentSwitch(self,{ \
                'Prana':   1112,
                'coupler': 1113, 
                'Milmega':         1115, 
                'RFPA':       1116, 
                'open':          1118 \
            }),
            'powerMeterIncident':AgilentSwitch(self,{ \
                'Prana':         1122,
                'coupler':           1123,
                'Milmega':         1125, 
                'RFPA':       1126, 
                'open':          1128 \
            }),
            'powerMeterReflected':AgilentSwitch(self,{ \
                'Prana':   1132,                
                'coupler': 1133, 
                'Milmega':         1135, 
                'RFPA':       1136, 
                'open':          1138 \
            })
        })
        
        def allSamePosition(position):
            return { \
                    'DUT':position,
                    'powerMeterIncident':position,   
                    'powerMeterReflected':position,
                    'generator':position\
            }
        
        self._presets = { \
            'open'    : allSamePosition('open'),            
            'coupler' : allSamePosition('coupler'),
            'RFPA'    : allSamePosition('RFPA'),
            'Prana'   : allSamePosition('Prana'),
            'Milmega' : allSamePosition('Milmega') \
        }
        
    def setPreset(self,presetName):
        preset = self._presets[presetName]
        for switchName,switchPosition in preset.items():
            self[switchName].setPosition(switchPosition)
    def checkPreset(self,presetName):
        preset = self._presets[presetName]
        for switchName,switchPosition in preset.items():
            if self[switchName].getPosition() != switchPosition:
                return False
        return True
        
        
    def putOnline(self):
        ScpiDevice.putOnline(self)
        if self.online:
            self.write('ROUT:CHAN:VER:ENAB ON,(@1102:1138)') #TODO: take minimum an maximum of switchMapping
            self.write('ROUTe:RMODule:BANK:LED:DRIVe:ENABle ON,ALL,(@1100)') #enables LED drive for all channels
            self.write('ROUTe:RMODule:BANK:LED:DRIVe:LEVel 0.02,ALL,(@1100)') #...at 20mA drive strength 

        
  
if __name__ == '__main__':
    switchPlatform = AgilentL4490a()
#    switchPlatform['DUT'].openSwitch() #
#    switchPlatform['DUT'].setPosition('SAorVNA')
    
    switchPlatform.setPreset('Prana')

    time.sleep(1)
    switchPlatform.setPreset('coupler')
    time.sleep(1)
    switchPlatform.setPreset('Milmega')
    time.sleep(1)
    switchPlatform.setPreset('RFPA')
    time.sleep(1)
    switchPlatform.setPreset('open')

#    print switchPlatform['DUT'].getPosition()