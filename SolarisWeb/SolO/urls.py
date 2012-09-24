from django.conf.urls import patterns, include, url
from SolO.settings import PROJECT_PATH
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SolO.views.home', name='home'),
    # url(r'^SolO/', include('SolO.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'SolO.hostinfo.views.index' ),
    url(r'^svcs$', 'SolO.svcs.views.index' ),
    url(r'^svcs/smf$', 'SolO.svcs.views.show' ),
) 

urlpatterns += staticfiles_urlpatterns()
