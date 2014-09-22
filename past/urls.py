from django.conf.urls import patterns, url

from past import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<slug>[^/]+)/$', views.index, name='index_article'),
    url(r'^/perma/(?P<slug>[^/]+)/$', views.ViewArticle, name='ViewArticle'),
    url('mapdata.json', views.GetMapData, name="GetMapData"),
    url(r'^country/(?P<countryCode>[^/]+)/$', views.GetCountryArticles, name='GetCountryArticles'),
    url(r'^search/$', views.Search, name="Search")
)