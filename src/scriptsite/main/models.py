from django.db import models
from datetime import datetime

class TestScript(models.Model):
    """ A Test script document """
    revision = models.CharField(max_length = 15)
    script_file = models.FileField(upload_to='uploaded_scripts/%y%m%d%H%M%S/')
    date_uploaded = models.DateTimeField(default = datetime.now(), editable = False)
    
class TestRun(models.Model):
    """ A particular test run, of a given script """
    date_started = models.DateTimeField()
    test_script = models.ForeignKey(TestScript)
        
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


    