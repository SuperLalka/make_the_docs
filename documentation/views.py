from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Article

def index(request, pk):
    list_articles = Article.objects.all()
    article = get_object_or_404(Article, pk=pk)
    return render(
        request,
        'index.html',
        context={'list_articles':list_articles,'article':article}
    )


