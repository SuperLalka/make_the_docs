from django.views.generic import RedirectView
from django.conf.urls import url
from django.urls import path
from . import views


app_name = 'documentation'
urlpatterns = [
    url(r'^article/(?P<pk>\d+)$', views.index, name='index'),
    url(r'^$', RedirectView.as_view(url='article/1', permanent=True)),
    
]
