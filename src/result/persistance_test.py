import unittest

from xml.dom.minidom import getDOMImplementation,parseString

class XmlTest(unittest.TestCase):
    def setUp(self):
        self.document = getDOMImplementation().createDocument(None,'EmcTestbench',None)
    def assertLoopThrough(self,resultClass):
        self.result.asDom(self.document.documentElement)
        xml = self.document.toprettyxml(encoding='utf-8')
        print xml
#        raise Exception
        parsedDom = parseString(xml)
        resultElement = parsedDom.documentElement.getElementsByTagName(resultClass.__name__)[0]
        parsedResult = resultClass.fromDom(resultElement)
#        print parsedResult.data
        self.assertEqual(self.result,parsedResult)
