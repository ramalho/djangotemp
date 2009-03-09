from django.conf.urls.defaults import *

from django.contrib import admin, databrowse
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^biblio/', include('biblio.foo.urls')),

    (r'^cat/', include('biblio.catalogo.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^db/(.*)', databrowse.site.root),

)
