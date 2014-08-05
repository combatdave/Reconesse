from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Reconesse.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
	url(r'^admin/', include(admin.site.urls)),

	url(r'^past/', include('past.urls')),
	url(r'^present/', include('present.urls')),
	url(r'^future/', include('future.urls')),

	#url(r'^present/', include('zinnia.urls')),
	#url(r'^comments/', include('django.contrib.comments.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
