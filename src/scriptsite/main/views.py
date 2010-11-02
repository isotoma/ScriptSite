from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from scriptsite.main.forms import ScriptForm
from scriptsite.main.models import TestScript, TestRun

from scriptsite.main.xml_analysis import get_number_of_tests, convert_script_to_models

def upload(request):
    data = {}
    
    form = ScriptForm()
    data['form'] = form
    
    if request.method == 'POST':
        form = ScriptForm(request.POST, request.FILES)
        form.save()
        return HttpResponseRedirect(reverse('script', kwargs = {'script_id':form.instance.id}))
        
    
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
    
    if request.method == 'POST':
        test_run = convert_script_to_models(script)
        return HttpResponseRedirect(reverse('test_run', kwargs = {'run_id': test_run.id}))
      
    return render_to_response('script.html', data, context_instance = RequestContext(request))

def test_run_home(request):
    data = {}
    
    data['runs'] = TestRun.objects.all()
    
    return render_to_response('run_home.html', data, context_instance = RequestContext(request))

def test_run(request, run_id):
    
    data = {}
    
    try:
        test_run = TestRun.objects.get(id = run_id)
    except:
        return HttpResponseRedirect(reverse('test_run_home'))
    
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('view_run', kwargs = {'run_id': test_run.id}))
    
    data['run'] = test_run
    data['groups'] = test_run.testgroup_set.all()
    
    return render_to_response('run.html', data, context_instance = RequestContext(request))

def view_run(request, run_id):
    
    data = {}
    
    try:
        test_run = TestRun.objects.get(id = run_id)
    except:
        return HttpResponseRedirect(reverse('test_run_home'))
    
    data['run'] = test_run
    data['groups'] = test_run.testgroup_set.all()
    data['view'] = True
    
    return render_to_response('view_run.html', data, context_instance = RequestContext(request))