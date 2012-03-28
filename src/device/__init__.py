__all__ = ['multimeter','rfgenerator','wattmeter','switch']


from device import Device,ScpiDevice
from generator import Generator

from agilent33 import Agilent33220A,Agilent33250A
from agilente4419b import AgilentE4419b
from agilentn5181a import AgilentN5181a
from agilentn9010a import AgilentN9010a
from agilent53220a import Agilent53220a
from hp54520a import Hp54520a
from hp8591a import Hp8591a
from agilentl4411a import AgilentL4411a
from newportesp300 import NewportEsp300
from milmegaas01043030 import MilmegaAS0104_30_30
from agilentl4490a import AgilentL4490a
from agilentn6700b import AgilentN6700b
from agilent86100a import Agilent86100a
from pranaap32dt120 import PranaAP32DT120

knownDevices = { \
    'lfGenerator0' : Agilent33250A(), 
    'lfGenerator1' : Agilent33220A('TCPIP0::172.20.1.204::inst0::INSTR','Agilent 33220 LF Generator top'),
    'lfGenerator2' : Agilent33220A('TCPIP0::172.20.1.205::inst0::INSTR','Agilent 33220 LF Generator bottom'),
    'rfGenerator' : AgilentN5181a(),
    'switchPlatform' : AgilentL4490a(),
    'powerSupply' : AgilentN6700b(),
    'oscilloscope1' : Agilent86100a(),
    'oscilloscope2' : Hp54520a(),
    'wattMeter' : AgilentE4419b(),
    'multimeter' : AgilentL4411a(),
    'frequencyCounter' : Agilent53220a(),
    'spectrumAnalyzer0' : AgilentN9010a(),
    'spectrumAnalyzer1' : Hp8591a(),
    'amplifier1' : MilmegaAS0104_30_30(),    
    'amplifier0' : PranaAP32DT120(),
    'positioner' : NewportEsp300(),
}

from test.simpledpi import knownDevices