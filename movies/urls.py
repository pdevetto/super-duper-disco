from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<movie_id>[0-9]+)/$', views.movie, name='movie'),
    url(r'^update/', views.update, name='update'),
    url(r'^clear/', views.clear, name='clear'),
    url(r'^process/', views.process, name='process'),
]
