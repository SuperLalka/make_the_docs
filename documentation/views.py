from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Article, Section


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_articles'] = Article.objects.order_by("-priority")
        context['list_section'] = Section.objects.all()
        return super().get_context_data(**context)
