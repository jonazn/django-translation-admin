from django.conf.urls import patterns, include, url
from translationadmin import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<app_name>\w+)/(?P<language_code>\w+)/$', views.edit, name='edit'),
    url(r'^(?P<app_name>\w+)/(?P<language_code>\w+)/post/$', views.edit_post, name='edit_post'),
]