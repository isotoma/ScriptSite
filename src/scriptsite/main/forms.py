from django.forms import ModelForm

from scriptsite.main.models import TestScript

class ScriptForm(ModelForm):
    class Meta:
        model = TestScript