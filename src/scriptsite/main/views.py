from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from scriptsite.main.forms import ScriptForm

def upload(request):
    data = {}
    
    form = ScriptForm()
    data['form'] = form
    
    if request.method == 'POST':
        form = ScriptForm(request.POST)
        form.save()
        
    
    return render_to_response('upload.html', data, context_instance = RequestContext(request))