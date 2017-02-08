from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qa_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^qa_system/', include('answerer.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
