import mwavepy
import pylab

adapter = mwavepy.Network('../data/cstSimulation_smdFixture.s2p')
measured = mwavepy.Network('../../../../ADS/Fixture_tests_prj/misc/eco35Cal_L_1pFC.s1p','measured 1 pF')

measured = measured.interpolate(adapter.frequency)
measured.z0 = 50.

# adapter = adapter.interpolate(measured.frequency)
# adapter.z0 = 50.
 
dutEstimate = adapter.inv ** measured

dutEstimate.plot_s_smith(m=0,n=0)


pylab.show()