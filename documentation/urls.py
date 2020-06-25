from django.views.generic import RedirectView
from django.conf.urls import url
from . import views


app_name = 'documentation'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^article/(?P<address>\w+)$', views.ArticleView.as_view(), name='article'),
    url(r'^article_search$', views.article_search, name='article_search'),
    url(r'^article_page_404$', views.article_404, name='article_404'),
    url(r'^error_send_email$', views.error_send_email, name='error_send_email'),
    
]
