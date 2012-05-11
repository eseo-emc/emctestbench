import unittest

from persistance_test import XmlTest
from utility.quantities import Power

class PowerXml_test(XmlTest):
    def setUp(self):
        XmlTest.setUp(self)
    def test_scalar(self):
        self.result = Power(.001,'W')
        self.assertLoopThrough(Power)
    def test_array(self):
        self.result = Power([0.001,.002,.1,1],'W')
        self.assertLoopThrough(Power)

        
if __name__ == '__main__':
     import nose
#     nose.run(argv=['-w','../test','-v'])
     nose.run(defaultTest=__name__)
#    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Power_test)
#    unittest.TextTestRunner(verbosity=2).run(suite)