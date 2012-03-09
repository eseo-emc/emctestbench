import mwavepy
import pylab

openSimulation = mwavepy.Network('../data/cstSimulation_open_lumped.s1p','cstSimulation_open_lumped.s1p')
shortSimulation = mwavepy.Network('../data/cstSimulation_short_lumped.s1p','cstSimulation_short_lumped.s1p')
openSimulation.plot_s_smith(m=0,n=0)
shortSimulation.plot_s_smith(m=0,n=0)

middlePoint = (openSimulation.s[:,0,0] + shortSimulation.s[:,0,0])/2.
pylab.plot(middlePoint.real,middlePoint.imag,label='Middle point')

pylab.show()