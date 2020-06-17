from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Article, Section


def index(request):
    list_articles = Article.objects.all()
    article = Article.objects.order_by("id").first()
    list_section = Section.objects.all()
    return render(
        request,
        'index.html',
        context={'list_articles':list_articles,'article':article,'list_section':list_section}
    )


def article(request, pk):
    list_articles = Article.objects.all()
    try:
        article = Article.objects.get(pk=pk)
        list_section = Section.objects.all()
        return render(
            request,
            'index.html',
            context={'list_articles':list_articles,'article':article,'list_section':list_section}
        )
    except Article.DoesNotExist:
        return index(request)

"""#Вариант с get_object_or_404
def article(request, pk):
    list_articles = Article.objects.all()
    article = get_object_or_404(Article, pk=pk)
    return render(
        request,
        'index.html',
        context={'list_articles':list_articles,'article':article}
    )
    """
