# based on the 8720c implementation of scikit-rf, thanks Alex!

import numpy

from device import ScpiDevice
from networkanalyzer import NetworkAnalyzer
from utility import quantities

import time
import subprocess

import skrf
from skrf.vi import vna
from visa import vpp43

class Hp8720c(NetworkAnalyzer,ScpiDevice,vna.HP8720):
    defaultName = 'HP8720C Vector Network Analyzer'
    defaultAddress = 'GPIB10::2::INSTR'
    visaIdentificationStartsWith = 'HEWLETT PACKARD,8720C,0,1.04'
    documentation = {'Programmers Manual':'http://na.tm.agilent.com/pna/help/latest/whnjs.htm'}
    
    def __init__(self, visaAddress=None,frontPanelLockout=True,**kwargs):
        ScpiDevice.__init__(self,visaAddress)                
        
        self.ifBandwidth = quantities.Frequency(3000,'Hz')
        # scikit-rf API compatibility
        self.channel=1
        self.port = 1
        self.echo = False
        self.frontPanelLockout = frontPanelLockout
    
    def putOnline(self):
        ScpiDevice.putOnline(self)
        if self._deviceHandle:
            self._deviceHandle.timeout = 20.0
            if not self.frontPanelLockout:
                self.gtl()
            self.write('FORM4;')
            self._setGpibRemote(True)

    
    def write(self,message):

        ScpiDevice.write(self,message)


        
    def _setGpibRemote(self,remote=True):
        if remote:
            vpp43.gpib_control_ren(self._deviceHandle.vi,vpp43.VI_GPIB_REN_ASSERT)
        else:
            vpp43.gpib_control_ren(self._deviceHandle.vi,vpp43.VI_GPIB_REN_DEASSERT)

    
    @property
    def continuous(self):
        raise NotImplementedError
    @continuous.setter
    def continuous(self, continuousValue = True):
        if continuousValue:
            self.write('CONT;')
        elif not continuousValue:
            self.write('HOLD;')
        else:
            raise(ValueError('takes a boolean'))
    
    def measure(self,portB=None,portA=None):
        if portB == None and portA == None:
            s11 = self.measure(0,0).s[:,0,0]
            s12 = self.measure(0,1).s[:,0,0]
            s22 = self.measure(1,1).s[:,0,0]
            s21 = self.measure(1,0).s[:,0,0]
    
            network = skrf.Network()
            network.s = numpy.array(\
                    [[s11,s21],\
                    [ s12, s22]]\
                    ).transpose().reshape(-1,2,2)
            network.frequency= self.frequency
    
            return network            
        else:
            self.initiate(portB,portA)
            return self.fetch(portB,portA)
    
    def initiate(self,portB=0,portA=0):
        self.continuous = False
        self.write('s{bNatural:d}{aNatural:d};'.format(bNatural=portB+1,aNatural=portA+1))
        self.write('IFBW {bandwidth:d} Hz'.format(bandwidth=int(self.ifBandwidth.asUnit('Hz'))))
        self._triggerAndWait()
        
    def fetch(self,portB=0,portA=0):
        s = numpy.array(self.ask_for_values('OUTPDATA'))
        s.shape=(-1,2)
        s =  s[:,0]+1j*s[:,1]
        network = skrf.Network(name='S_{bNatural:d}{aNatural:d}'.format(bNatural=portB+1,aNatural=portA+1))
        network.s = s
        network.frequency = self.frequency
        
        return network
           
    def _triggerAndWait(self):
        #self.continuous = False
        waitTime = analyzer.sweepTime
        self.write('REST;')
        #self.write('SING;')
        time.sleep(waitTime.asUnit('s'))
        while int(self.ask('HOLD?')) == 0:          
            time.sleep(0.5)

    @property
    def sweepTime(self):
        return quantities.Time(float(self.ask('SWET?')))
        
    # scikit-rf API compatibility
    @property
    def s11(self):
        return self.measure(0,0)
    @property
    def s12(self):
        return self.measure(0,1)
    @property
    def s21(self):
        return self.measure(1,0)
    @property
    def s22(self):
        return self.measure(1,1)
        
    @property
    def test(self):
        return None
             
if __name__ == '__main__':
    from utility.quantities import Frequency,PowerRatio   

    import pylab    
    analyzer = Hp8720c()
    analyzer.putOnline()
    analyzer.ifBandwidth = quantities.Frequency(10,'Hz')
    
#    measurement = analyzer.measure(1,0)
   
    measurement = analyzer.measure()
    print 'Done'
    measurement.write_touchstone('8720c-meanderE-NE-(220-short)-10Hz')
    
#    measurement.plot_z_mag() 
#    pylab.gca().set_xscale('log')
#    pylab.gca().set_yscale('log')
    measurement.plot_s_db()
    pylab.show()
    
    