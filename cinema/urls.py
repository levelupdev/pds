from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import render

urlpatterns = patterns('',
    # Examples:
    url(r'^$', render, name='home', kwargs={'template_name': 'list.html'}),
)
