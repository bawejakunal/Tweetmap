from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^wordsearch$', views.wordsearch, name='wordsearch'),
    url(r'^fetchtweet$', views.fetchtweet, name='fetchtweet'),
    url(r'^geosearch$', views.geosearch, name='geosearch'),
]