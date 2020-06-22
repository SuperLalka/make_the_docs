from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import Article, Section
from .utils import get_anchor_list


def index(request):
    list_articles = Article.objects.order_by("-priority")
    article = Article.objects.order_by("id").first()
    list_section = Section.objects.all()
    return render(
        request,
        'index.html',
        context={'list_articles':list_articles,'article':article,'list_section':list_section}
    )


class ArticleView(generic.DetailView):
    model = Article
    template_name = 'index.html'
    slug_field = 'address'
    slug_url_kwarg = 'address'

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect('/docs/article_page_404', request=None, permanent=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_articles'] = Article.objects.order_by("-priority")
        context['list_section'] = Section.objects.all()
        context['anchor_list'] = get_anchor_list(self.object.body)
        return super().get_context_data(**context)


def article_404(request):
    list_articles = Article.objects.order_by("-priority")
    list_section = Section.objects.all()
    return render(
        request,
        'article_404.html',
        context={'list_articles':list_articles,'list_section':list_section}
    )