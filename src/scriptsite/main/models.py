from django.db import models
from datetime import datetime

from django.contrib.auth.models import User

class TestScript(models.Model):
    """ A Test script document """
    revision = models.CharField(max_length = 15)
    script_file = models.FileField(upload_to='uploaded_scripts/%y%m%d%H%M%S/')
    date_uploaded = models.DateTimeField(default = datetime.now(), editable = False)
    flavour = models.CharField(max_length = 20, editable = False, default = "NOTSET")
    
    approved = models.BooleanField(default = False)
    upload_user = models.ForeignKey(User, related_name = "upload_user", blank=True, null=True)
    approved_user = models.ForeignKey(User, related_name = "approved_user", blank=True, null=True)
    
    version_of_software = models.TextField(blank = True, null = True)
    software_environment = models.TextField(blank = True, null = True)
    
    class Meta:
        permissions = (
            ('can_approve', 'Can approve a test script'),
        )
    
class TestRun(models.Model):
    """ A particular test run, of a given script """
    date_started = models.DateTimeField()
    test_script = models.ForeignKey(TestScript)
    
    def get_passed(self):
        passed = 0
        for group in self.testgroup_set.all():
            passed += len(group.singletest_set.filter(passed = True))
        return passed
    
    def get_failed(self):
        failed = 0
        for group in self.testgroup_set.all():
            failed += len(group.singletest_set.filter(passed = False))
        return failed
            
    def get_incomplete(self):
        incomplete = 0
        for group in self.testgroup_set.all():
            incomplete += len(group.singletest_set.filter(passed = None))
        return incomplete
        
class TestGroup(models.Model):
    """ A group of tests, for a particular category of test """
    test_script = models.ForeignKey(TestScript)
    test_run = models.ForeignKey(TestRun)
    name = models.CharField(max_length = 50)
    
class SingleTest(models.Model):
    """ A single test, which is linked to a group """
    test_group = models.ForeignKey(TestGroup)
    name = models.CharField(max_length = 50, blank = True, null = True)
    story_id = models.CharField(max_length = 50, blank = True, null = True)
    steps = models.TextField(blank = True, null = True)
    expected_results = models.TextField(blank = True, null = True)
    automated_test_id = models.TextField(blank = True, null = True)
    actual_result = models.TextField(blank = True, null = True)
    passed = models.NullBooleanField(blank = True, null = True)
    
    def get_status_as_string(self):
        """ Used in template to work around broken if tag behaviour with nullbooleanfields """
        
        if self.passed == True:
            return 'True'
        elif self.passed == False:
            return 'False'
        else:
            return 'None'

    def get_status_as_friendly_string(self):
        """ Turn True/False into Pass/Fail """
        if self.passed:
            return "Pass"
        elif self.passed == False:
            return "Fail"
        else:
            return ''

    