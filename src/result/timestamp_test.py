import unittest

from persistance_test import XmlTest
from timestamp import Timestamp
from datetime import datetime

class TimestampXml_test(XmlTest):
    def setUp(self):
        XmlTest.setUp(self)
    def test_now(self):
        self.result = Timestamp()
        self.assertLoopThrough(Timestamp)
    def test_array(self):
        self.result = Timestamp()
        self.result = self.result.append(Timestamp())
        self.assertLoopThrough(Timestamp)
    def assertEqual(self,one,other):
        unittest.TestCase.assertTrue(self,(one == other).all())
        

        
if __name__ == '__main__':
     import nose
#     nose.run(argv=['-w','../test','-v'])
     nose.run(defaultTest=__name__)
#    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Power_test)
#    unittest.TextTestRunner(verbosity=2).run(suite)