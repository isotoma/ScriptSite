from django import forms

from scriptsite.main.models import TestScript

class ScriptForm(forms.ModelForm):
    class Meta:
        model = TestScript
        
class SubversionForm(forms.Form):
    """ Subversion connection / retrieval details """
    subversion_url = forms.URLField()
    revision_number = forms.CharField(max_length = 20)
    username = forms.CharField(max_length = 50)
    password = forms.CharField(widget = forms.PasswordInput)
    flavour = forms.CharField(max_length = 20)