from django.conf.urls import patterns, url

from answerer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^update/$', views.update, name='update'),
    url(r'^show/$', views.show, name='show')
)