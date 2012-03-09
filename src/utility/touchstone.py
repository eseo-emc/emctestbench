import numpy
import matplotlib.pyplot as pyplot
import re
from utility.conversion import *

class s1pFile():
    def __init__(self,s1pPath,delay=0.0):
        assert s1pPath.endswith('.s1p')
        self.title = re.split('/',s1pPath)[-1]
        self.frequencies = [] # in Hz
        self.s11Values = [] # as complex, linear values
        
        touchstoneFileHandle = open(s1pPath,'r',1)
        for line in touchstoneFileHandle:
            if line[0] == '!':
                pass # comment, ignore for the moment
            elif line[0] == '#':
                assert line.endswith('hz S db R 50\n')
            else: # should be a data line
                splittedLine = re.split('\s+',line)
                floatItems = []
                for item in splittedLine:
                    try:
                        floatItems.append(float(item))
                    except ValueError:
                        pass
                
                assert len(floatItems) == 3 # we only support S1P files for the moment
                self.frequencies.append(floatItems[0])
                
                s11angle = numpy.exp(numpy.complex(0,numpy.deg2rad(floatItems[2])))
                s11magnitude = 10.0**(floatItems[1]/20.0)
                
                self.s11Values.append(s11magnitude*s11angle)
        
        self.frequencies = numpy.array(self.frequencies)
        self.s11Values = numpy.array(self.s11Values)
        # compensate electrical delay
        self.s11Values = numpy.exp(numpy.complex(0,1)*2*2*numpy.pi*self.frequencies*delay) * self.s11Values
        
    def plotImpedance(self):
        # pyplot.plot(frequencies,abs(s11Values))
        # pyplot.plot(frequencies,dB(abs(s11Values)))
        pyplot.plot(self.frequencies,dB(abs(stoz(self.s11Values,50.0))),label=self.title)
        pyplot.xscale('symlog')
        pyplot.xlabel('Frequency (Hz)')
        pyplot.ylabel('Impedance (dBohm)')

if __name__ == '__main__':
    s1pFile('Z:/ADS/Fixture_tests_prj/misc/eco35Cal_1pFC.s1p').plotImpedance()
    s1pFile('Z:/ADS/Fixture_tests_prj/misc/mathCal_1pF_calkitA_5.s1p').plotImpedance()
                            
    pyplot.legend()
    pyplot.show()