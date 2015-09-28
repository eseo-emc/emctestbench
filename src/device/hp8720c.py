# based on the 8720c implementation of scikit-rf, thanks Alex!

import numpy

from device import ScpiDevice
from networkanalyzer import NetworkAnalyzer
from utility import quantities

import time
import subprocess

import skrf
#from skrf.vi import vna
#from visa import vpp43
import pyvisa
from StringIO import StringIO

class Hp8720c(NetworkAnalyzer,ScpiDevice): #,vna.HP8720):
    defaultName = 'HP8720C Vector Network Analyzer'
    defaultAddress = 'GPIB1::2::INSTR'
    visaLibrary = 'agilent'
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
        
        self._lastFrequency = None
        self._lastLearnString = None
        self._hardPresetMethod = None
        
                
    
    def putOnline(self):
        ScpiDevice.putOnline(self)
        if self._deviceHandle:
            self._deviceHandle.timeout = 20000
            if not self.frontPanelLockout:
                self.gtl()
            #self.write('FORM{0:d};'.format(self.dataFormat))
            self._setGpibRemote(True)
            self._gotoNullStatus()            
            if not self._lastLearnString:
                self._obtainLearnString()
            self._restoreLearnString()
            
    def _gotoNullStatus(self):
        for tryNumber in range(10):
            statusByte = self.readStatusByte()

            if statusByte & 0x04:
                self.ask('ESB?')
            elif statusByte & 0x08:
                print self.popError()
            elif statusByte & 0x10:
                self.ask('ESR?')
            elif statusByte & 0x40:
                self.readStatusByte()
            elif statusByte:
                print "Don't know what to do with this status:"
                self.printStatusByte()
            else:
                break
            
            time.sleep(0.5)
        else:
            self.printStatusByte()
            raise IOError, 'Could not get status null'
            
    def beep(self):
        self.write('EMIB')
        
    def _obtainLearnString(self):
        print 'Obtain learn string'
        self._lastLearnString = self.ask_raw('OUTPLEAS')
    def _restoreLearnString(self):
        print 'Restore learn string'
        assert self._lastLearnString, 'No learn string to restore'
        self.write_raw('INPULEAS '+self._lastLearnString)
    
    def _hardPresetAndRestore(self):
        print 'Resetting...'
        self._setGpibRemote(False)
        self._hardPresetMethod()
        time.sleep(10)
        print 'Restoring state'
        self.putOnline()
        
    def _setGpibRemote(self,remote=True):
        visalib = self._deviceHandle.visalib
        
        if remote:
            visalib.gpib_control_ren(self._deviceHandle.session,pyvisa.constants.VI_GPIB_REN_ASSERT)
        else:
            visalib.gpib_control_ren(self._deviceHandle.session,pyvisa.constants.VI_GPIB_REN_DEASSERT)

    
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
    
    def measure(self,*args,**kwargs):
        try:
            return self._measure(*args,**kwargs)
        except (pyvisa.VisaIOError, IOError) as ioError:
            print 'IO Error...',ioError
            if self._hardPresetMethod:
                self._hardPresetAndRestore()
                print 'Trying to measure again...'
                return self._measure(*args,**kwargs)
            else:
                print 'No hard preset method available'
                raise

    
    def _measure(self,portB=None,portA=None,**kwargs):
#        raise IOError
        if portB == None and portA == None:
            s11 = self.measure(0,0,**kwargs).s[:,0,0]
            s12 = self.measure(0,1,**kwargs).s[:,0,0]
            s22 = self.measure(1,1,**kwargs).s[:,0,0]
            s21 = self.measure(1,0,**kwargs).s[:,0,0]
    
            network = skrf.Network()
            network.s = numpy.array(\
                    [[s11,s21],\
                    [ s12, s22]]\
                    ).transpose().reshape(-1,2,2)
            network.frequency= self.frequency
    
            return network            
        else:
            self.initiate(portB,portA,**kwargs)
            return self.fetch(portB,portA,**kwargs)
    
    def initiate(self,portB=0,portA=0,**kwargs):
        self.continuous = False
        self.write('s{bNatural:d}{aNatural:d};'.format(bNatural=portB+1,aNatural=portA+1))
        self.write('IFBW {bandwidth:d} Hz'.format(bandwidth=int(self.ifBandwidth.asUnit('Hz'))))
        self._triggerAndWait()
        
    def fetch(self,portB=0,portA=0,dataFormat=1,**kwargs):
        if dataFormat == 'all':
            return {'FORM1':self.fetch(portB=portB,portA=portA,dataFormat=1),
                    'FORM4':self.fetch(portB=portB,portA=portA,dataFormat=4)}
        else:
            self.write('FORM{0:d};'.format(dataFormat))
            
            if dataFormat == 4:
                s = numpy.array(self.ask_for_values('OUTPDATA'))
                s.shape=(-1,2)
                sValues =  s[:,0]+1j*s[:,1]
            elif dataFormat == 1:
                #http://www.vnahelp.com/tip23.html
                rawData = self.ask_raw('OUTPDATA')
                assert rawData[0] == '#', 'OUTPDATA should start with "#"'
                lengthFromHeader = 4+numpy.frombuffer(rawData[2:4],numpy.dtype('>i2'))[0]
                assert len(rawData) == lengthFromHeader,'Buffer length {0} does not correspond with length {1} announced in the header field'.format(len(rawData),lengthFromHeader)
                
                tupleData = numpy.frombuffer(rawData[4:],numpy.dtype(">i2,>i2,i1,i1"))
                fieldData = numpy.array(tupleData.tolist())
#                assert (fieldData[:,2] == 0).all(),'The fifth byte was supposed to be zero, but is not always. Maybe there is supplementary precision to exploit...'
                sValues = (1.0*fieldData[:,1] + 1.0j*fieldData[:,0]) * (2.0**(fieldData[:,3]-15))
               
            network = skrf.Network(name='S_{bNatural:d}{aNatural:d}'.format(bNatural=portB+1,aNatural=portA+1))
            network.s = sValues

            network.frequency = self.frequency
            return network
    @property
    def frequency(self):
        if self.frontPanelLockout:
            if type(self._lastFrequency) == type(None):
                self._lastFrequency = self._fget()
            return self._lastFrequency
        else:
            return self._fget(self)

    def _fget(self):
        valuesString = self.ask_raw('OUTPLIML')
        valuesStringFile = StringIO(valuesString)
        f = numpy.loadtxt(valuesStringFile,delimiter=',')
        assert f.shape[1] == 4,'OUTPLIML should return a CSV table with 4 columns'
        return skrf.Frequency.from_f(f[:,0],unit='hz')
      
    def _triggerAndWait(self):
#        # Wait by polling for Hold state
#        waitTime = self.sweepTime
#        self.write('REST;')
#        #self.write('SING;')
#        time.sleep(waitTime.asUnit('s'))
#        while int(self.ask('HOLD?')) == 0:          
#            time.sleep(0.5)

#        # Wait for SRQ
#        print 'Before arming'
#        self.printStatusByte()
#        self.printStatusByte()
        self.armServiceRequestOnOperationComplete()
#        print 'After arming'
#        self.printStatusByte()
#        self.printStatusByte()
        self.write('REST; OPC; WAIT;') #OPC raises the OPC bit upon the completion of the following command (at least for the so-called OPC'able commands, see manual)
#        print 'After launching',self.readStatusByte(),self.readStatusByte()        
        self.waitForServiceRequest(poll=True)
#        print 'After SRQ'
#        self.printStatusByte()
#        self.printStatusByte()
#        assert(self._deviceHandle._vpp43.read_stb(self._deviceHandle.vi) & 0x40)
#        assert(not(self._deviceHandle._vpp43.read_stb(self._deviceHandle.vi) & 0x40))
        
#        analyzer.write('REST; OPC; WAIT')
#        analyzer.waitUntilReady()
    def printStatusByte(self):
        statusByteDescription = []
        statusByte = self.readStatusByte()
        if statusByte & 0x01:
            statusByteDescription += ['Waiting for reverse GET']
        if statusByte & 0x02:
            statusByteDescription += ['Waiting for forward GET']
        if statusByte & 0x04:
            statusByteDescription += ['Check event status register B']
        if statusByte & 0x08:
            statusByteDescription += ['Check error queue']
        if statusByte & 0x10:
            statusByteDescription += ['Message in output queue']
        if statusByte & 0x20:
            statusByteDescription += ['Check event status register [A]']
        if statusByte & 0x40:
            statusByteDescription += ['Request service (RQS)']
        if statusByte & 0x80:
            statusByteDescription += ['This bit should never be set!']
        print 'Status: ' + ', '.join(statusByteDescription)

    def popError(self):
        return self.ask('OUTPERRO')

    @property
    def sweepTime(self):
        return quantities.Time(float(self.ask('SWET?')))
        
    @property 
    def attenuatorPort1(self):
        return self._getAttenuator(1)
    @attenuatorPort1.setter
    def attenuatorPort1(self,value):
        self._setAttenuator(1,value)
        
    @property 
    def attenuatorPort2(self):
        return self._getAttenuator(2)
    @attenuatorPort2.setter
    def attenuatorPort2(self,value):
        self._setAttenuator(2,value)
        
    def _getAttenuator(self,port):
        return quantities.PowerRatio(float(self.ask('ATTP{port:d}?'.format(port=port))),unit='dB')
    def _setAttenuator(self,port,value):
        self.write('ATTP{port:d} {attenuation}'.format(port=port,attenuation=value.asUnit('dB')))
        
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

class Hp8753e(Hp8720c):
    defaultName = 'HP8753E Vector Network Analyzer'
    defaultAddress = 'GPIB8::2::INSTR'
    visaIdentificationStartsWith = 'HEWLETT PACKARD,8753E,0,1.04'

class Hp8753c(Hp8720c):
    defaultName = 'HP8753C Vector Network Analyzer'
    defaultAddress = 'GPIB0::8::INSTR' #'GPIB2::8::INSTR'
    visaIdentificationStartsWith = 'HEWLETT PACKARD,8753C,0,4.01'

             
if __name__ == '__main__':
    from utility.quantities import Frequency,PowerRatio   

    import pylab    
    import time
    
    analyzer = Hp8720c()
#    analyzer.putOnline()    

#    from configuration import knownDevices
#    analyzer._hardPresetMethod = knownDevices['positioner'].strobeLowGpio1

    
##    analyzer.ifBandwidth = quantities.Frequency(10,'Hz')
    
#    ## 5th byte test   
#    measurement = analyzer.measure(1,0,dataFormat='all')
#    numpy.testing.assert_almost_equal(measurement['FORM1'].s,measurement['FORM4'].s,err_msg='The FORM1 and FORM4 data do not correspond.')
    
#    ## duration measurement
#    durations = []
#    for tryNumber in range(3):
#        print tryNumber
#        start =time.clock()
#        measurement = analyzer.measure(1,0)#,dataFormat='all')
##        analyzer._deviceHandle.clear()
#        durations += [time.clock()-start]
#    durations = durations[1:]
#    print numpy.mean(durations),numpy.std(durations)
    
#    measurement2 = analyzer.measure(0,0)
#    measurement2.name = 'open'
#    print 'Done'
##    measurement.write_touchstone('Picosecond_5545_114-RF-short2')
    
#    measurement.plot_z_mag() 
#    pylab.gca().set_xscale('log')
#    pylab.gca().set_yscale('log')
#    measurement.plot_s_db()
#    measurement2.plot_s_db()
#    measurement.plot_s_smith()
#    pylab.show()
    
#    for repetition in range(1000):
#        analyzer.write('*CLS; *ESE 1; *SRE 32; HOLD; REST; OPC; WAIT; EMIB;')
#        print repetition
#        analyzer._deviceHandle.wait_for_srq()
#        print "Clean sweep Done, fetching data..."
#        analyzer.ask_for_values('OUTPDATA')
    measurement = analyzer.measure(1,0)
    measurement.plot_s_db()
    pylab.show()