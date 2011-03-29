from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.template import RequestContext

from scriptsite.main.forms import ScriptForm, SubversionForm

@permission_required('main.add_testscript')
def upload_view(request):
    
    data = {}
    
    form = ScriptForm()
    data['form'] = form
    
    subversion_form = SubversionForm()
    data['subversion_form'] = subversion_form
    
    return render_to_response('upload.html', data, context_instance = RequestContext(request))