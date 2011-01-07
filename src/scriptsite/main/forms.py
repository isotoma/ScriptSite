from django import forms

from scriptsite.main.models import TestScript

class ScriptForm(forms.ModelForm):
    class Meta:
        model = TestScript
        exclude = ('approved', 'upload_user', 'approved_user', 'version_of_software', 'software_environment')
        
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