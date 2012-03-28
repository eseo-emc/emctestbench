from device import ScpiDevice
from spectrumanalyzer import SpectrumAnalyzer
from utility.quantities import Power

class Hp8591a(SpectrumAnalyzer,ScpiDevice):
    defaultName = 'HP8591A Spectrum Analyzer'
    defaultAddress = 'GPIB1::18::INSTR'
    visaIdentificationStartsWith = 'HP8591A'
    documentation = {'Programmers Manual':'http://cp.literature.agilent.com/litweb/pdf/08590-90235.pdf'}
        
    def askIdentity(self):
        return self.ask('ID?')
            
    def powerAt(self,frequency):
        self.write('MKF %EHZ' % frequency)
        dBmPower = float(self.ask('MKA?'))
        return Power(dBmPower,'dBm')
        
if __name__ == '__main__':
    test = Hp8591a()
    print test.powerAt(10e6).dBm()
