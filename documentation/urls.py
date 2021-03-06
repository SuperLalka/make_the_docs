from django.conf.urls import url
from django.urls import include, path

from . import views


app_name = 'documentation'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^article/(?P<address>\w+)/(?P<lang>\w+)?$', views.ArticleView.as_view(), name='article_page'),
    url(r'^article_search$', views.article_search, name='article_search'),
    url(r'^article_page_404$', views.article_404, name='article_404'),
    url(r'^typo_feedback$', views.error_send_email, name='error_send_email'),
    url(r'^pdf_creator/(?P<lang>\w+)$', views.pdf_creator, name='pdf_creator'),
]

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
    url(r'^change_version/(?P<version>\w+)$', views.change_version, name='change_version'),
]
