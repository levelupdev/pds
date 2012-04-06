from django.conf.urls.defaults import patterns, include, url

from views import List, MovieDetails, Add, BasicInfoEdit

urlpatterns = patterns('',
    # Examples:
    url(r'^$', List.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', MovieDetails.as_view(), name='details'),
    url(r'^add/$', Add.as_view(), name='add'),
    url(r'^basic_info/(?P<pk>\d+)/$', BasicInfoEdit.as_view(), name='edit_basic_info'),
    url(r'^rating_and_genre/(?P<pk>\d+)/$', BasicInfoEdit.as_view(), name='edit_rating_and_genre'),
    url(r'^crew_and_cast/(?P<pk>\d+)/$', BasicInfoEdit.as_view(), name='edit_crew_and_cast'),
    url(r'^sales_info/(?P<pk>\d+)/$', BasicInfoEdit.as_view(), name='edit_sales_info'),
    url(r'^art/(?P<pk>\d+)/$', BasicInfoEdit.as_view(), name='edit_art'),
    url(r'^feature_and_trailer/(?P<pk>\d+)/$', BasicInfoEdit.as_view(), name='edit_feature_and_trailer'),
)
