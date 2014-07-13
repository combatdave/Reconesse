from django.conf.urls import patterns, url

from future import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<articleID>\d+)/$', views.ViewArticle, name='ViewArticle'),
    url('mapdata.json', views.GetMapData, name="GetMapData"),
    url(r'^country/(?P<countryCode>[^/]+)/$', views.GetCountryArticles, name='GetCountryArticles'),
)