from device import ScpiDevice
from frequencycounter import FrequencyCounter

class Agilent53220a(FrequencyCounter,ScpiDevice):
    defaultName = 'Agilent 53220A frequency counter'
    defaultAddress = 'TCPIP0::192.168.18.186::inst0::INSTR'
    visaIdentificationStartsWith = 'Agilent Technologies,53220A,'
    
    def measurePeriod(self,channel=1):
        return float(self.ask('MEAS:SPER? (@1)'))
    def measureJitter(self):
        self.write('CONF:SPER (@1)')
        self.write('TRIG:COUN 1')
        self.write('SAMP:COUN 500')
        self.write('SENS:FREQ:GATE:TIME 10e-3')
        self.write('CALC:STAT ON')
        self.write('CALCulate1:AVERage:STATe ON')
        self.write('INIT')
        self.write('*WAI')
        
        averagingResults = self.ask('CALC:AVER:ALL?').split(',')
        average = float(averagingResults[0])
        standardDeviation = float(averagingResults[1])
        minimum = float(averagingResults[2])
        maximum = float(averagingResults[3])
        
        peakToPeakJitter = (maximum-minimum)
        rmsJitter = standardDeviation        
        
        return (rmsJitter,peakToPeakJitter)
    def getCount(self):
        return int(self.ask('CALCulate1:AVERage:COUNt:CURRent?'))
    
if __name__ == '__main__':
    device = Agilent53220a()

    print device.popError()
#    device.drawAttention()    
#    device.reset()
#    print device.measurePeriod()    
#    print device.measureJitter()

    