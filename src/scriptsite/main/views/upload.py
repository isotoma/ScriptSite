from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect

from scriptsite.main.forms import ScriptForm, SubversionForm

@permission_required('main.add_testscript')
def upload_view(request):
    """ View the upload template, with the forms on to upload a test script """
    
    data = {}
    
    form = ScriptForm()
    data['form'] = form
    
    subversion_form = SubversionForm()
    data['subversion_form'] = subversion_form
    
    return render_to_response('upload.html', data, context_instance = RequestContext(request))

@permission_required('main.add_testscript')
def upload_post(request):
    """ Upload a test script by posting to the page """
    if request.POST.get('upload', None):
        form = ScriptForm(request.POST, request.FILES)
        
        # if we have a valid form, save it and go to the created script
        if form.is_valid():
            form.save()
            form.instance.upload_user = request.user
            form.instance.save()
            return HttpResponseRedirect(reverse('script', kwargs = {'script_id':form.instance.id}))
            
    # if we get here, it wasn't a post
    return HttpResponseRedirect(reverse('upload'))