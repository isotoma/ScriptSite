import os

from mock import Mock
from lxml.etree import _Element
from django.test import TestCase

import xml_analysis
from models import TestScript

class XmlAnalysisTest(TestCase):
    
    def setUp(self):
        self.test_file_path = os.path.join(os.path.dirname(__file__), '..', 'test_files', 'sample.xml')

    def test_get_xml_doc(self):
        """
        Test that we can retrieve an xml document from disk
        """
        xml_doc = xml_analysis.get_xml_doc(self.test_file_path)

    def test_get_number_of_tests(self):
        """
        Check that we are loading the right number of tests from our sample test document
        """
        
        script = Mock(spec = TestScript)
        script.script_file.path = self.test_file_path
        
        number = xml_analysis.get_number_of_tests(script)
        self.assertTrue(number == 4)
