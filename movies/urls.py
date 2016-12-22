from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^set$', views.isset, name='isset'),
    url(r'^update/', views.update, name='update'),
    url(r'^clear/', views.clear, name='clear'),
    url(r'^process/', views.process, name='process'),
    url(r'^jsondata/', views.jsondata, name='jsondata'),
    url(r'^possible/', views.possible, name='possible'),
    # Acces
    url(r'^movie/(?P<movie>[0-9]*)/$', views.find, name='movie'),
    url(r'^genre/(?P<genre>[0-9]*)/$', views.find, name='genre'),
    url(r'^people/(?P<people>.*)/$', views.find, name='people'),
    url(r'^year/(?P<year>.*)/$', views.find, name='year'),

]
