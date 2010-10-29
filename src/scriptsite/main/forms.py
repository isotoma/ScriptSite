from django.forms import ModelForm

from scriptsite.main.models import test_script

class ScriptForm(ModelForm):
    class Meta:
        model = test_script