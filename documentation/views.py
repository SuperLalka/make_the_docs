from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Article


def index(request):
    list_articles = Article.objects.all()
    article = Article.objects.order_by("id").first()
    return render(
        request,
        'index.html',
        context={'list_articles':list_articles,'article':article}
    )


def article(request, pk):
    list_articles = Article.objects.all()
    try:
        article = Article.objects.get(pk=pk)
        return render(
            request,
            'index.html',
            context={'list_articles':list_articles,'article':article}
        )
    except Article.DoesNotExist:
        return index(request)
