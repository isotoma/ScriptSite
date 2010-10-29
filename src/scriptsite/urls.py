
# $Id$

# Urls
__author__ = 'Forename Surname <forename@isotoma.com>'
__docformat__ = 'restructuredtext en'
__version__ = '$Revision$'[11:-2]

from django.conf.urls.defaults import *
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.template.loader import render_to_string

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
        
    # Prevent search engine spiders from generating 404s when looking for a 
    # robots.txt. Obviously remove these if using actual files
    # (This way is less efficient than doing it via server config. 
    # Keeps it in-app though.)
    (r'^robots\.txt$', lambda r: HttpResponse("", mimetype="text/plain")),
	
    # Redirect a request for favicon.ico from the virtual root to where it 
    # actually is. Many user agents (RIM based blackberry browsers, old 
    # versions of IE etc) lazily look in the root first, raising a 404
    (r'^favicon\.ico$', lambda r: HttpResponseRedirect('/static/images/favicon.ico')),
    
    (r'^upload/', 'scriptsite.main.views.upload'),
)

# Serve static content through Django.
# (This way is less efficient than having the web server do it and unless 
# there is a decent caching layer, SERVE_STATIC should be False for production)
if settings.SERVE_STATIC:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT }),
    )

# We can also redirect to templates wherever we like here.
handler404 = '%s.return_404' % (settings.ROOT_URLCONF,)
handler500 = '%s.return_500' % (settings.ROOT_URLCONF,)

def return_404(request):
    return HttpResponseNotFound(render_to_string("errors/404.html"))

def return_500(request):
    return HttpResponseServerError(render_to_string("errors/500.html"))

