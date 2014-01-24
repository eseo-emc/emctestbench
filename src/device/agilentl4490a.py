from device import ScpiDevice
from switch import SwitchPlatform,Switch

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
                '773D':   1102,
                '86205A': 1103, 
                'Prana':         1105, 
                'Milmega':       1106, 
                'open':          1108 \
            }),
            'DUT':AgilentSwitch(self,{ \
                '773D':   1112,
                '86205A': 1113, 
                'Prana':         1115, 
                'Milmega':       1116, 
                'open':          1118 \
            }),
            'powerMeterIncident':AgilentSwitch(self,{ \
                'aux':           1123,
                'Prana':         1125, 
                'Milmega':       1126, 
                'open':          1128 \
            }),
            'powerMeterReflected':AgilentSwitch(self,{ \
                '773D':   1132,                
                '86205A': 1133, 
                'Prana':         1135, 
                'Milmega':       1136, 
                'open':          1138 \
            })
        })
        
        self._presets = { \
            '86205A'  : {'DUT':'86205A',  'powerMeterReflected':'86205A', 'generator':'86205A'},
            '773D'  : {'DUT':'773D',  'powerMeterReflected':'773D', 'generator':'773D'},
            'Prana'   : {'DUT':'Prana',   'powerMeterIncident':'Prana',   'powerMeterReflected':'Prana',   'generator':'Prana'},
            'Milmega' : {'DUT':'Milmega', 'powerMeterIncident':'Milmega', 'powerMeterReflected':'Milmega', 'generator':'Milmega'} \
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

        
  
if __name__ == '__main__':
    switchPlatform = AgilentL4490a()
#    switchPlatform['DUT'].openSwitch() #
#    switchPlatform['DUT'].setPosition('SAorVNA')
    switchPlatform.setPreset('86205A')
    print switchPlatform['DUT'].getPosition()