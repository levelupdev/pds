from django.conf.urls.defaults import patterns, include, url

from views import List

urlpatterns = patterns('',
    # Examples:
    url(r'^$', List.as_view(), name='list'),
)
