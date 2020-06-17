from django.views.generic import RedirectView
from django.conf.urls import url
from django.urls import path
from . import views


app_name = 'documentation'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^article/(?P<pk>\d+)$', views.article, name='article'),
    
]
