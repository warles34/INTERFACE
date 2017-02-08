from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wikiPrueba.views.home', name='home'),
    # url(r'^wikiPrueba/', include('wikiPrueba.foo.urls')),
    (r'^index/$', 'wiki_model.views.index'),
    (r'^index/?question=(([A-Za-z0-9+]+)=ASK$', 'wiki_model.views.result'),
    #(r'^result/([A-Za-z0-9_]+)$', 'wiki_model.views.result'),
    (r'^result/(.+)','wiki_model.views.resultError'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)