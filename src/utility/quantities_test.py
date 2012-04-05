import unittest
from quantities import *
import numpy

class Power_test(unittest.TestCase):
    def setUp(self):
        self.testPower = Power(0,'dBm')
    def test_stringify(self):
        self.assertEqual(str(self.testPower),'+0.0 dBm')
    def test_linearFactor(self):
        self.assertAlmostEqual((self.testPower*2.0).dBm(),3.0,1)
        
class PowerRatio_test(unittest.TestCase):
    def setUp(self):
        self.testPower = PowerRatio(-3.0,'dB')
    def test_linear(self):
        self.assertAlmostEqual(self.testPower.linear(),0.5,1)
        
class Power_integration_test(unittest.TestCase):
    def setUp(self):
        self.testPower = Power(30,'dBm')+Power(30,'dBm')
    def test_value(self):
        self.assertAlmostEqual(self.testPower.dBW(),3.0,1)
        
class Power_array_test(unittest.TestCase):
    def setUp(self):
        self.test = Power(numpy.array([0.0,3.0,30.0,27.0]),'dBm')
    def test_linear(self):
        self.assertTrue( all(abs((self.test.watt() / numpy.array([0.001,0.002,1,0.5]))-1) <0.01))
        
if __name__ == '__main__':
     import nose
     nose.run(argv=['-w','../test','-v'])
     nose.run(defaultTest=__name__)
#    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Power_test)
#    unittest.TextTestRunner(verbosity=2).run(suite)
