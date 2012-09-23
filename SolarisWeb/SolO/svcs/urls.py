#!/usr/bin/env python
from django.conf.urls.defaults import *
urlpatterns = patterns("testsites.acctr.views",
    (r'^$', "index"),
    (r'^smf/$', "show"),
)
