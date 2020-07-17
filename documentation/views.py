from django.core.mail import BadHeaderError, send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.views import generic
from io import BytesIO
from xhtml2pdf import pisa

from .forms import ErrorForm, SearchForm
from .models import Article, ArticlesContent, SectionContent
from .utils import add_anchor, get_anchor_list, get_search_context, fetch_pdf_resources, search_formatting
from make_the_docs import settings


def index(request):
    article = ArticlesContent.objects.filter(article__version=request.session.get('content_version', None)).order_by('-article__section__priority').first()
    if not article:
        return redirect('/docs/article_page_404', permanent=True)
    return redirect(f'/docs/article/{article.article.address}')


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

    def get_queryset(self):
        self.queryset = Article.objects.filter(version=self.request.session.get('content_version', None))
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            article = self.object.content.filter(language=self.kwargs['lang']).first()
        except:
            article = self.object.content.filter(language=self.request.LANGUAGE_CODE).first()
        if article is None:
            article = self.object.content.filter(language=settings.LANGUAGE_CODE).first()
        article.body = add_anchor(article.body)
        context.update({
            'title': article.title,
            'body': article.body,
            'anchor_list': get_anchor_list(article.body),
        })
        return super().get_context_data(**context)


def article_404(request):
    return render(
        request,
        'article_404.html'
    )


def article_search(request):
    form = SearchForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect(request)
    key = form.cleaned_data.get("search_key")
    results = search_formatting(ArticlesContent.objects.filter(Q(title__icontains=key) | Q(body__icontains=key)), key=key)
    results, count_num = get_search_context(results, key=key)
    return render(
        request,
        'search_results.html',
        context={'results': results,
                 'count_num': count_num,
                 'key': key,
                 }
    )


def error_send_email(request):
    err_form = ErrorForm(request.POST)
    err_message = err_form['err_name'].value() + "\n" + err_form['err_desc'].value()
    if err_form.is_valid():
        try:
            send_mail('Make-the-docs-site', err_message, 'site@example.com', ['user@example.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/docs/')
    else:
        return HttpResponse('Make sure all fields are entered and valid.')


def pdf_creator(request, **kwargs):
    template = get_template('pdf_creator.html')
    list_articles = ArticlesContent.objects.filter(article__version=request.session.get('content_version', None), language=kwargs['lang'])
    list_section = SectionContent.objects.filter(language=request.LANGUAGE_CODE)
    if list_section is None:
        list_section = SectionContent.objects.filter(language=settings.LANGUAGE_CODE)
    context = {
        'list_articles': list_articles,
        'list_section': list_section,
    }
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(html.encode('UTF-8'), result, encodind='UTF-8', link_callback=fetch_pdf_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")


def change_version(request, **kwargs):
    if kwargs['version'] == 'None':
        del request.session['content_version']
    else:
        request.session['content_version'] = kwargs['version']
    return HttpResponseRedirect('/docs/')
