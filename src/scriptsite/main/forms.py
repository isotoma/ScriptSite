from django import forms

from scriptsite.main.models import TestScript
from xml_analysis import extract_flavour

class ScriptForm(forms.ModelForm):
    class Meta:
        model = TestScript
        exclude = ('approved', 
                   'upload_user', 
                   'approved_user', 
                   'version_of_software', 
                   'software_environment', 
                   'closed',
                   'test_environment',
                   'browser_version',
                   'trac_milestone',
                   'test_ticket_number')
        
    def save(self, force_insert=False, force_update=False, commit=True):
        instance = super(forms.ModelForm, self).save(commit=False)
        instance.save(force_insert = force_insert, force_update = force_update)
        instance.flavour = extract_flavour(instance.script_file.path)
        instance.save(force_insert = force_insert, force_update = force_update)
        
class SubversionForm(forms.Form):
    """ Subversion connection / retrieval details """
    subversion_url = forms.URLField()
    revision_number = forms.CharField(max_length = 20)
    username = forms.CharField(max_length = 50)
    password = forms.CharField(widget = forms.PasswordInput)
    flavour = forms.CharField(max_length = 20)
    
    
class ScriptReviewForm(forms.Form):
    """ The details entered when a test script is approved by a Lead Developer """
    
    version_of_software = forms.CharField(max_length = 100)
    software_environment = forms.CharField(max_length = 100, widget = forms.Textarea)
    test_environment = forms.CharField(widget = forms.Textarea)
    browser_version = forms.CharField(widget = forms.Textarea)
    trac_milestone = forms.CharField(max_length = 100)
    test_ticket_number = forms.CharField(max_length = 100)