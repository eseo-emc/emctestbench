from device import knownDevices
import pylab
import skrf
import numpy

#vna = knownDevices['networkAnalyzer']
#vna.putOnline()
#attenuator = vna.measure()
#attenuator.write_touchstone('Power attenuator.s2p')

attenuator = skrf.Network(file="D:\\User_My_Documents\\Instrument\\My Documents\\EmcTestbench\\Calibration\\Power attenuator.s2p")

pylab.plot(attenuator.f/1e9,-attenuator.s_db[:,1,0],label="measurement")
transferModel = -29.75-0.65*numpy.sin((attenuator.f+2.5e9)/4e9 /(1+attenuator.f/100e9))

pylab.plot(attenuator.f/1e9,-transferModel,label="analytical")
pylab.xticks(range(0,22,2))
pylab.xlim(0,20)
pylab.ylim(28.5,31.5)
pylab.grid()
pylab.xlabel('Frequency (GHz)')
pylab.ylabel('Attenuation (dB)')
pylab.legend()
pylab.show()

#pylab.plot(attenuator.f/1e9,attenuator.s_vswr[:,0,0],label='Input')
#pylab.plot(attenuator.f/1e9,attenuator.s_vswr[:,1,1],label='Output')
#pylab.legend()
#pylab.xticks(range(0,22,2))
#pylab.xlim(0,20)
#pylab.ylim(1,1.5)
#pylab.grid()
#pylab.xlabel('Frequency (GHz)')
#pylab.ylabel('VSWR (:1)')
#pylab.show()

