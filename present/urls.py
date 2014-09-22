from django.conf.urls import patterns, url

from present import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<entryID>\d+)/$', views.ViewEntry, name='ViewEntry'),
)