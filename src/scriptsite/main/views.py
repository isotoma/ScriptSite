from django.http import HttpResponse
from django.shortcuts import render_to_response

from scriptsite.main.forms import ScriptForm

def upload(request):
    data = {}
    
    form = ScriptForm()
    data['form'] = form
    
    return render_to_response('upload.html', data)