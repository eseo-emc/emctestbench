
from amplifier import Amplifier

#from device import ScpiDevice
#class PranaAP32DT120(Amplifier,ScpiDevice):
#    defaultName = 'Prana AP32 DT120 Power Amplifier'
#    defaultAddress = 'GPIB0::5::INSTR'
#    visaIdentificationStartsWith = 'AP32 DT120'
#    terminationCharacters = '\r\n' 
#        
#    def _turnRfOn(self):
#        self.write('MHF')
#        self.write('MHF')
#        self.write('MHF')
#        self.write('MHF')
#
#    def _turnRfOff(self):
#        self.write('AHF')
#        self.write('AHF')
#        self.write('AHF')
#        self.write('AHF')

from PyQt4.QtGui import QApplication,QMessageBox
from device import Device

class PranaAP32DT120(Amplifier,Device):
    defaultName = 'Prana AP32 DT120 Power Amplifier Manual Dummy'
        
    def _prompt(self, message):
        QMessageBox.about(QApplication.topLevelWidgets()[0],'Manual Amplifier Control Required',message)
        
    def _turnRfOn(self):
        self._prompt('Turn the Prana amplifier on (RF ON) and click "OK"')
    def _turnRfOff(self):
        self._prompt('Turn the Prana amplifier off (RF OFF) and click "OK"')        
  
if __name__ == '__main__':
    import time

    amplifier = PranaAP32DT120()
#    print amplifier.askIdentity()
    
    amplifier.rfOn = True
    time.sleep(5)
    amplifier.rfOn = False

    