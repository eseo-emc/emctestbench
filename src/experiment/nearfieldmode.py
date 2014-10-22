"""
Quick test to scan a single tone along the X-axis in nearfield

Manual:
- power on the preamp (12V/0.5A)
- route the preamp to the VSA
- set the VSA to basic I/Q
- center the VSA on the tone

preamp
http://www.everythingrf.com/rf-microwave-amplifiers/p/Planar-Monolithics-Industries-82_PEC_60_0R14R0_5R0_10_12_SFF

@author: Sjoerd Op 't Land
"""
import numpy
import time
from matplotlib import pyplot


import device
from utility.quantities import Amplitude,Voltage,Current,Position
import device

class NearFieldMode:
    def __init__(self):
#        self.analyzer = device.AgilentN9010a()
        self.analyzer = device.knownDevices['networkAnalyzer']
        self.robot = device.knownDevices['positioner']
        
        self.powerSupply = device.knownDevices['powerSupply']
        self.powerSupply.setChannelParameters(4,Voltage(12.0,'V'),Current(0.7,'A'))
        
        self.switchPlatform = device.knownDevices['switchPlatform']
#        self.switchPlatform.closeSwitch('DUTtoSAorVNA')
        

    def sweep(self):
        self.powerSupply.turnChannelOn(4)
#        self.analyzer.align()
        
        zPosition = 28.9
#        # Demo A v2
#        (xGrid,yGrid) = numpy.meshgrid(numpy.linspace(197,173,11),numpy.linspace(-86,-2,21))           
        # Demo C v2
        (xGrid,yGrid) = numpy.meshgrid(numpy.linspace(173,197,41),numpy.linspace(-95,0,20))   
        
        #try:
        for corner in [(0,0),(-1,0),(-1,-1),(0,-1)]:
            self.robot.setLocation(Position(numpy.array([xGrid[corner],yGrid[corner],zPosition]),'mm'))
        
        
#        xRange = numpy.hstack((xRange,xRange[::-1]))
        complexVoltages = []
        startTime = time.clock()
        for (xPosition,yPosition) in zip(xGrid.flat,yGrid.flat):
            self.robot.setLocation(Position(numpy.array([xPosition,yPosition,zPosition]),'mm'),
                                   highSpeed=True)
#            self.analyzer.waitUntilReady()
#            time.sleep(1)
            complexVoltages.append(self.analyzer.measure(1,0).s[-1,0,0])
#            complexVoltages.append(self.analyzer.averageComplexVoltage())
        print 'Sweep took {0:.1f}s'.format(time.clock()-startTime)
        
        #finally:
        print 'Shutting down...'
        self.powerSupply.turnChannelOff(4)  
        self.robot.setLocation(Position(numpy.array([xGrid[0,0],yGrid[0,0],zPosition]),'mm'),highSpeed=True)
        self.robot.setLocation(Position(numpy.array([0,0,0]),'mm'),highSpeed=True)
                       
        complexVoltagesGrid = numpy.array(complexVoltages).reshape(xGrid.shape)                     
        return (xGrid,yGrid,complexVoltagesGrid)
        
 
if __name__ == '__main__':
    print 'Start mode scan'
    test = NearFieldMode()
    (xGrid,yGrid,complexVoltagesGrid) = test.sweep()

    import tables
    nfsFile = tables.openFile('D1C-common-50Ohm-3GHz-sticker.h5', mode='w', title="Near-Field Scan")
    root = nfsFile.root
    nfsFile.createArray(root,"voltage_dB",20.0*numpy.log10(numpy.abs(complexVoltagesGrid)))
    nfsFile.createArray(root,"voltage",complexVoltagesGrid)
    nfsFile.createArray(root,"xCoords",xGrid)
    nfsFile.createArray(root,"yCoords",yGrid)
    nfsFile.close()
    
    print "Done"




  
## show magnitude
#pyplot.plot(numpy.real(voltages[0,:]),numpy.abs(voltages[1,:]),label='Open')
##pyplot.plot(numpy.real(voltages_load[0,:]),numpy.abs(voltages_load[1,:]),label='Loaded')
#pyplot.ylabel('Transfer magnitude (1)')
#pyplot.xlabel('x position (mm)')
#pyplot.legend()
#pyplot.show()
#    
## show phase
#pyplot.plot(numpy.real(voltages[0,:]),numpy.rad2deg(numpy.angle(voltages[1,:])),label='Open')
##pyplot.plot(numpy.real(voltages_load[0,:]),numpy.rad2deg(numpy.angle(voltages_load[1,:])),label='Loaded')
#pyplot.ylabel('Phase (degrees)')
#pyplot.xlabel('x position (mm)')
#pyplot.legend()
#pyplot.show()
