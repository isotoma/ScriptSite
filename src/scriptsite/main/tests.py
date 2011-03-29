import os

from mock import Mock
from lxml.etree import _Element
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Permission
from django.http import HttpResponseRedirect

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
        
    def test_extract_flavour(self):
        """ Check that we are extracting the right flavour from our test file """
        
        script = Mock(spec = TestScript)
        script.script_file.path = self.test_file_path
        
        flavour = xml_analysis.extract_flavour(script)
        self.assertTrue(flavour, 'sample')
        
    def test_convert_script_to_dicts(self):
        """ Given the sample xml file, can we convert it to the right dict structure """
        
        script = Mock(spec = TestScript)
        script.script_file.path = self.test_file_path
        
        dicts = xml_analysis.convert_script_to_dicts(script)
        self.assertTrue(dicts.keys() == ['flavour', 'groups'])
        
        self.assertTrue(len(dicts['groups']) == 2)
        
        for group in dicts['groups']:
            for test in group['tests']:
                self.assertTrue(len(test.keys()) == 5)
                for key, value in test.iteritems():
                    self.assertTrue(value != None)
                    
    def test_convert_script_to_models(self):
        """ Give the sample xml file, can we convert it and pop it in the database correctly """
        
        script = TestScript()
        script.set_from_file(self.test_file_path, 'sample.xml')
        script.save()
        
        model = xml_analysis.convert_script_to_models(script)
        
        self.assertTrue(model.get_incomplete() == 4)
        
        self.assertTrue(model.testgroup_set.count() == 2)
        
        for group in model.testgroup_set.all():
            for test in group.singletest_set.all():
                self.assertTrue(test.name != None)
                self.assertTrue(test.story_id != None)
                self.assertTrue(test.steps != None)
                self.assertTrue(test.expected_results != None)
                self.assertTrue(test.automated_test_id != None)
                
    def test_get_value(self):
        
        from lxml import etree
        
        doc = etree.fromstring('<foo><bar>baz</bar></foo>')
        
        ret_val = xml_analysis._get_value(doc, 'bar')
        self.assertTrue(ret_val == 'baz')
        
        ret_val = xml_analysis._get_value(doc, 'quux')
        self.assertIsNone(ret_val)
        
        
        
class ModelsTest(TestCase):
    
    def setUp(self):
        self.test_file_path = os.path.join(os.path.dirname(__file__), '..', 'test_files', 'sample.xml')
        
    
    def test_create_script_from_file(self):
        """ Check we can create a script from an already existing file """
        
        script = TestScript()
        script.set_from_file(self.test_file_path, 'sample.xml')
        script.save()
        
        
class UploadViewsTest(TestCase):
    
    def setUp(self):
        """ Set up the environment for the test """
        # we need an admin user
        u = User()
        u.username = 'upload'
        u.set_password('upload')
        u.is_staff = True
        u.save()
        permission = Permission.objects.get(codename = 'add_testscript')
        u.user_permissions.add(permission)
        
        u.save()
        self.client = Client()
        self.test_file_path = os.path.join(os.path.dirname(__file__), '..', 'test_files', 'sample.xml')
    
    def test_view(self):
        """ Test the upload view """
        
        login_success = self.client.login(username = 'upload', password = 'upload')
        
        self.assertTrue(login_success)
        
        response = self.client.get(reverse('upload'))
        
        self.assertTrue(response.template[0].name == 'upload.html')
        
    def test_view_unauthorized(self):
        """ Test that we're redirected correctly if we're not a valid user """
        
        response = self.client.get(reverse('upload'))
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertTrue(response.status_code == 302)
        
    def test_upload_post_unauthorized(self):
        """ Test that we're redirected correctly if we're not a valid user """
        
        response = self.client.get(reverse('upload_post'))
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertTrue(response.status_code == 302)
        
    def test_upload_post_if_get(self):
        """ If we get this view, it should redirect to upload view """
        
        login_success = self.client.login(username = 'upload', password = 'upload')
        self.assertTrue(login_success)
        response = self.client.get(reverse('upload_post'))
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertTrue(response.status_code == 302)
        
    def test_upload_post(self):
        """ Test that we can post a file to this """
        login_success = self.client.login(username = 'upload', password = 'upload')
        self.assertTrue(login_success)
        
        f = open(self.test_file_path)
        post_data = {'revision': 1, 'script_file': f}
        response = self.client.post(reverse('upload_post'), post_data)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertTrue(response.status_code == 302)
        self.assertTrue('create' in response._headers['location'][1])
