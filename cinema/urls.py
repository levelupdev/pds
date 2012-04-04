from django.conf.urls.defaults import patterns, include, url

from views import List, MovieDetails, Edit

urlpatterns = patterns('',
    # Examples:
    url(r'^$', List.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', MovieDetails.as_view(), name='details'),
    url(r'^edit/(?P<pk>\d+)/$', Edit.as_view(), name='details'),
)
