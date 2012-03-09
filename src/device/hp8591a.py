from device import ScpiDevice
from spectrumanalyzer import SpectrumAnalyzer
from utility.quantities import Power

class Hp8591a(SpectrumAnalyzer,ScpiDevice):
    defaultName = 'HP8591A Spectrum Analyzer'
    visaIdentificationStartsWith = 'HP8591A'
    documentation = {'Programmers Manual':'http://cp.literature.agilent.com/litweb/pdf/08590-90235.pdf'}
        
    def askIdentity(self):
        return self.deviceHandle.ask('ID?')
            
    def powerAt(self,frequency):
        self.deviceHandle.write('MKF %EHZ' % frequency)
        dBmPower = float(self.deviceHandle.ask('MKA?'))
        return Power(dBmPower,'dBm')
        
if __name__ == '__main__':
    test = Hp8591a()
    print test.powerAt(10e6).dBm()
