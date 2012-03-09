#__all__ = ['agilent33','hp54520a']


from device import Device,ScpiDevice
from generator import Generator

from agilent33 import Agilent33
from agilente4419b import AgilentE4419b
from agilentn5181a import AgilentN5181a
from agilentn9010a import AgilentN9010a
from hp54520a import Hp54520a
from hp8591a import Hp8591a
from agilentl4411a import AgilentL4411a
from newportesp300 import NewportEsp300
from milmegaas01043030 import MilmegaAS0104_30_30
from agilentl4490a import AgilentL4490a
from agilentn6700b import AgilentN6700b
from agilent86100a import Agilent86100a
from pranaap32dt120 import PranaAP32DT120

knownDevices = [ \
    Agilent33('GPIB1::10::INSTR','33250 LF Generator'), 
    Agilent33('TCPIP0::172.20.1.204::inst0::INSTR','33220 LF Generator top'),
    Agilent33('TCPIP0::172.20.1.205::inst0::INSTR','33220 LF Generator bottom'),
    AgilentN5181a('TCPIP0::172.20.1.202::inst0::INSTR'),
    AgilentL4490a('TCPIP0::172.20.1.201::inst0::INSTR'),
    AgilentN6700b('TCPIP0::172.20.1.203::inst0::INSTR'),
    Agilent86100a('GPIB1::7::INSTR'),
    Hp54520a('GPIB1::7::INSTR'),
    AgilentE4419b('GPIB1::13::INSTR'),
    AgilentL4411a('TCPIP0::172.20.1.207::inst0::INSTR'),
    AgilentN9010a('TCPIP0::172.20.1.209::inst0::INSTR'),
    Hp8591a('GPIB1::18::INSTR'),
    MilmegaAS0104_30_30('GPIB1::6::INSTR'),    
    PranaAP32DT120('GPIB1::5::INSTR'),
    NewportEsp300('GPIB1::1::INSTR'),
]
