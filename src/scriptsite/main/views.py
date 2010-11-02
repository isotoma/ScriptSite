from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from scriptsite.main.forms import ScriptForm
from scriptsite.main.models import TestScript, TestRun, SingleTest

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
        if request.POST.get('view', None):
            return HttpResponseRedirect(reverse('view_run', kwargs = {'run_id': test_run.id}))
        if request.POST.get('edit', None):
            return HttpResponseRedirect(reverse('edit_run', kwargs = {'run_id': test_run.id}))
    
    data['run'] = test_run
    data['groups'] = test_run.testgroup_set.all()
    passed = failed = incomplete = 0
    for group in test_run.testgroup_set.all():
        passed += len(group.singletest_set.filter(passed = True))
        failed += len(group.singletest_set.filter(passed = False))
        incomplete += len(group.singletest_set.filter(passed = None))
    data['passed'] = passed
    data['failed'] = failed
    data['incomplete'] = incomplete
    
    
    return render_to_response('run.html', data, context_instance = RequestContext(request))

def view_run(request, run_id, view):
    
    data = {}
    
    try:
        test_run = TestRun.objects.get(id = run_id)
    except:
        return HttpResponseRedirect(reverse('test_run_home'))
    
    if request.method == 'POST':
        update_data(request.POST, test_run)
        return HttpResponseRedirect(reverse('test_run', kwargs={'run_id': run_id}));
    
    data['run'] = test_run
    data['groups'] = test_run.testgroup_set.all()
    data['view'] = view
    
    return render_to_response('view_run.html', data, context_instance = RequestContext(request))

def update_data(data, test_run):
    for d in data.iteritems():
        split = d[0].split('/')
        if len(split) < 3: 
            return 
        group = test_run.testgroup_set.get(name = split[0])
        test = group.singletest_set.get(name = split[1])
        
        if split[2] == 'actual':
            test.actual_result = d[1]
            
        if split[2] == 'passfail':
            if d[1] == 'pass':
                test.passed = True
            elif d[1] == 'fail':
                test.passed = False
            else:
                test.pased = None
        
        test.save()