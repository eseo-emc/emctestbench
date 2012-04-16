import unittest
import numpy
from resultset import ResultSet
from utility import Power

class ResultSet_test(unittest.TestCase):
    def setUp(self):
        self.theSet = ResultSet({'frequency':float,'transmittedPower':Power,'generatedPower':Power})
        self.theSet.append({'frequency':30e3,'transmittedPower':Power(30.,'dBm'),'generatedPower':Power(40.,'dBm')})
        self.theSet.append({'frequency':40e3,'generatedPower':Power(40.,'dBm')})
        
    def test_floats(self):
        self.assertTrue(all(self.theSet['frequency'] == numpy.array([30.0e3,40.0e3])))
    def test_numpySubClasses(self):
        self.assertTrue( (self.theSet['generatedPower'] == Power([40.,40.],'dBm')).all())
    def test_singleValue(self):
        self.assertTrue(self.theSet['transmittedPower'][0] == Power([1.],'W'))
    def test_nanConversion(self):
        self.assertTrue(numpy.isnan(self.theSet['transmittedPower'][1]))
    
    def test_byRow(self):
        rows = self.theSet.byRow()
        row = rows.next()
        self.assertEqual(row['frequency'] , 30e3 )
        self.assertEqual( row['transmittedPower'] , Power(30.,'dBm') )
        self.assertEqual( row['generatedPower'] , Power(40.,'dBm') )
        
        row = rows.next()
        self.assertEqual( row['frequency'] , 40e3 )
        self.assertTrue( numpy.isnan(row['transmittedPower']) )
        self.assertEqual( row['generatedPower'] , Power(40.,'dBm') )
        
if __name__ == '__main__':
     import nose
#     nose.run(argv=['-w','../test','-v'])
     nose.run(defaultTest=__name__)
#    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Power_test)
#    unittest.TextTestRunner(verbosity=2).run(suite)