from django.views.generic import RedirectView
from django.conf.urls import url
from . import views


app_name = 'documentation'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^article/(?P<address>\w+)$', views.ArticleView.as_view(), name='article'),
    
]
