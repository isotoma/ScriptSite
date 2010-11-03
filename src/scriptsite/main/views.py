from datetime import datetime
import cStringIO as StringIO

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.core.urlresolvers import reverse

import ho.pisa as pisa

from scriptsite.main.forms import ScriptForm, SubversionForm
from scriptsite.main.models import TestScript, TestRun, SingleTest

from scriptsite.main.xml_analysis import get_number_of_tests, convert_script_to_models
from scriptsite.main.subversion import get_from_subversion

def upload(request):
    data = {}
    
    form = ScriptForm()
    data['form'] = form
    
    subversion_form = SubversionForm()
    data['subversion_form'] = subversion_form
    
    if request.method == 'POST':
        if request.POST.get('upload', None):
            form = ScriptForm(request.POST, request.FILES)
            form.save()
            return HttpResponseRedirect(reverse('script', kwargs = {'script_id':form.instance.id}))
        if request.POST.get('subversion', None):
            subversion_form = SubversionForm(request.POST)
            if subversion_form.is_valid():
                script = get_from_subversion(subversion_form.cleaned_data['subversion_url'], 
                                    subversion_form.cleaned_data['revision_number'], 
                                    subversion_form.cleaned_data['username'], 
                                    subversion_form.cleaned_data['password'],
                                    subversion_form.cleaned_data['flavour'])
                return HttpResponseRedirect(reverse('script', kwargs = {'script_id': script.id}))
            data['subversion_form'] = subversion_form
        
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
        if request.POST.get('download', None):
            return HttpResponseRedirect(reverse('download_run', kwargs = {'run_id': test_run.id}))
    
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
    
    data['flavour'] = test_run.test_script.flavour
    
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
            continue 

        group = test_run.testgroup_set.get(name = split[0])
        test = group.singletest_set.get(name = split[1])
        
        
        
        if split[2] == 'actual':
            if d[1] and d[1] != 'None':
                test.actual_result = d[1]
            else:
                test.actual_result = ""
            
        if split[2] == 'passfail':
            if d[1] == 'pass':
                test.passed = True
            elif d[1] == 'fail':
                test.passed = False
            else:
                test.passed = None
        
        test.save()
        
def download_run(request, run_id):
    """ Convert a run to PDF in memory and send it to the client """
    
    try:
        test_run = TestRun.objects.get(id = run_id)
    except:
        return HttpResponseRedirect(reverse('test_run_home'))
    
    template_data = {}
    template_data['flavour'] = test_run.test_script.flavour
    template_data['generation_time'] = datetime.now()
    template_data['script_revision'] = test_run.test_script.revision
    template_data['test_run'] = test_run
    
    template = get_template('pdf_template.html')
    context = Context(template_data)
    html = template.render(context)
    result = StringIO.StringIO()
    
    pdf = pisa.CreatePDF(html, result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype = 'application/pdf')
    
    return HttpResponse('foo')
    