import unittest
import numpy
from resultset import ResultSet,ScalarResult,DictResult
from utility.quantities import Power,Boolean

from persistance_test import XmlTest

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
        
class ResultSetXml_test(XmlTest):
    def setUp(self):
        XmlTest.setUp(self)
        self.result = ResultSet({'frequency':float,'transmittedPower':Power,'generatedPower':Power})
        self.result.append({'frequency':30e3,'transmittedPower':Power(30.,'dBm'),'generatedPower':Power(40.,'dBm')})
        self.result.append({'frequency':40e3,'generatedPower':Power(40.,'dBm')})
    def test_loopthrough(self):
        self.assertLoopThrough(ResultSet)


#class VectorResultXml_test(XmlTest):
#    def setUp(self):
#        XmlTest.setUp(self)
#    def test_bool(self):
#        self.result = Boolean([True, False, True])
#        self.assertLoopThrough(Boolean)
#        
#     
#class ScalarResultXml_test(XmlTest):
#    def setUp(self):
#        XmlTest.setUp(self)
#        self.result = ScalarResult()
#    def test_loopThroughFloat(self):
#        self.result.data = 3.14
#        self.assertLoopThrough(ScalarResult)
#    def test_loopThroughPower(self):
#        self.result.data = Power(2,'W')
#        self.assertLoopThrough(ScalarResult)
#        
#class DictResultXml_test(XmlTest):
#    def setUp(self):
#        XmlTest.setUp(self)
#        self.result = DictResult()
#    def test_loopTroughSimple(self):
#        self.result.data = {'gg':42.42}
#        self.assertLoopThrough(DictResult)
#    def test_loopTroughPower(self):
#        self.result.data = {'Name':'Mohamed','Power':Power(0.001,'W')}
#        self.assertLoopThrough(DictResult)    
        
        
if __name__ == '__main__':
     import nose
#     nose.run(argv=['-w','../test','-v'])
     nose.run(defaultTest=__name__)
#    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Power_test)
#    unittest.TextTestRunner(verbosity=2).run(suite)