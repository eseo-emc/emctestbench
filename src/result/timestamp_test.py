import unittest

from persistance_test import XmlTest
from timestamp import TimeStamp

class TimeStampXml_test(XmlTest):
    def setUp(self):
        XmlTest.setUp(self)
    def test_now(self):
        self.result = TimeStamp()
        self.assertLoopThrough(TimeStamp)
        

        
if __name__ == '__main__':
     import nose
#     nose.run(argv=['-w','../test','-v'])
     nose.run(defaultTest=__name__)
#    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Power_test)
#    unittest.TextTestRunner(verbosity=2).run(suite)