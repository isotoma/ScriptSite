from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from scriptsite.main.forms import ScriptForm
from scriptsite.main.models import TestScript

from scriptsite.main.xml_analysis import get_number_of_tests

def upload(request):
    data = {}
    
    form = ScriptForm()
    data['form'] = form
    
    if request.method == 'POST':
        form = ScriptForm(request.POST, request.FILES)
        form.save()
        
    
    return render_to_response('upload.html', data, context_instance = RequestContext(request))

def script_home(request):
    data = {}
    
    data['scripts'] = TestScript.objects.all()
    
    return render_to_response('script_home.html', data, context_instance = RequestContext(request))

def script(request, script_id):
    data = {}
    
    try:
        script = TestScript.objects.get(id = script_id)
        data['script'] = script
        data['num_tests'] = get_number_of_tests(script)
    except:
        return HttpResponseRedirect(reverse('script_home'))
    
    
    
    return render_to_response('script.html', data, context_instance = RequestContext(request))