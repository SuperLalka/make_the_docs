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
from .models import Article, Section
from .utils import add_anchor, get_anchor_list, get_search_context, fetch_pdf_resources, search_formatting
from make_the_docs import settings


def index(request):
    list_articles = Article.objects.filter(version=request.session.get('content_version', None)).order_by("-priority")
    if not list_articles:
        return redirect('/docs/article_page_404', permanent=True)

    article = (list_articles.first()).content.filter(language=request.LANGUAGE_CODE).first()
    if article is None:
        article = (list_articles.first()).content.filter(language=settings.LANGUAGE_CODE).first()

    section_qs = Section.objects.order_by("-priority")
    list_section = [item.content.filter(language=request.LANGUAGE_CODE) for item in section_qs if item.content.filter(language=request.LANGUAGE_CODE)]
    if not list_section:
        list_section = [item.content.filter(language=settings.LANGUAGE_CODE) for item in section_qs]

    err_form, search_form = ErrorForm(), SearchForm()
    version_list = set([item.version for item in Article.objects.all()])
    return render(
        request,
        'index.html',
        context={'list_articles': list_articles,
                 'title': article.title,
                 'body': article.body,
                 'list_section': list_section,
                 'err_form': err_form,
                 'search_form': search_form,
                 'version_list': version_list}
    )


def article_abs(request, *args, **kwargs):
    list_articles = Article.objects.filter(version=request.session.get('content_version', None)).order_by("-priority")
    article = (Article.objects.filter(address=kwargs['address']).first()).content.filter(
        language=kwargs['lang']).first()
    article.body = add_anchor(article.body)
    anchor_list = get_anchor_list(article.body)
    err_form, search_form = ErrorForm(), SearchForm()

    list_section = [item.content.filter(language=request.LANGUAGE_CODE) for item in
                    Section.objects.order_by("-priority")]
    if not list_section:
        list_section = [item.content.filter(language=settings.LANGUAGE_CODE) for item in
                        Section.objects.order_by("-priority")]
    return render(
        request,
        'index.html',
        context={'list_articles': list_articles,
                 'title': article.title,
                 'body': article.body,
                 'anchor_list': anchor_list,
                 'list_section': list_section,
                 'err_form': err_form,
                 'search_form': search_form}
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

    def get_queryset(self):
        self.queryset = Article.objects.filter(version=self.request.session.get('content_version', None))
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object.content.filter(language=self.request.LANGUAGE_CODE).first()
        if article is None:
            article = self.object.content.filter(language=settings.LANGUAGE_CODE).first()
        context['title'] = article.title
        context['body'] = add_anchor(article.body)
        context['list_articles'] = self.queryset.order_by("-priority")
        context['list_section'] = [item.content.filter(language=self.request.LANGUAGE_CODE) for item in
                                   Section.objects.order_by("-priority") if item.content.filter(language=self.request.LANGUAGE_CODE)]
        if bool(context['list_section']) is False:
            context['list_section'] = [item.content.filter(language=settings.LANGUAGE_CODE) for item in
                                       Section.objects.order_by("-priority")]
        context['anchor_list'] = get_anchor_list(context['body'])
        context['version_list'] = set([item.version for item in Article.objects.all()])
        context['err_form'] = ErrorForm()
        context['search_form'] = SearchForm()
        return super().get_context_data(**context)


def article_404(request):
    list_articles = Article.objects.filter(version=request.session.get('content_version', None)).order_by("-priority")
    version_list = set([item.version for item in Article.objects.all()])

    list_section = [item.content.filter(language=request.LANGUAGE_CODE) for item in
                    Section.objects.order_by("-priority")]
    if not list_section:
        list_section = [item.content.filter(language=settings.LANGUAGE_CODE) for item in
                        Section.objects.order_by("-priority")]
    return render(
        request,
        'article_404.html',
        context={'list_articles': list_articles,
                 'list_section': list_section,
                 'version_list': version_list}
    )


def article_search(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        key = form.cleaned_data.get("search_key")
        results = search_formatting(
            [(item.content.filter(Q(title__icontains=key) | Q(body__icontains=key))) for item in Article.objects.all()
             if (item.content.filter(Q(title__icontains=key) | Q(body__icontains=key)))], key=key)
        results, count_num = get_search_context(results, key=key)
        list_articles = Article.objects.filter(version=request.session.get('content_version', None)).order_by(
            "-priority")
        err_form, search_form = ErrorForm(), SearchForm()

        list_section = [item.content.filter(language=request.LANGUAGE_CODE) for item in
                        Section.objects.order_by("-priority")]
        if not list_section:
            list_section = [item.content.filter(language=settings.LANGUAGE_CODE) for item in
                            Section.objects.order_by("-priority")]
    else:
        return HttpResponseRedirect(request)
    return render(
        request,
        'search_results.html',
        context={'results': results,
                 'count_num': count_num,
                 'key': key,
                 'list_articles': list_articles,
                 'list_section': list_section,
                 'err_form': err_form,
                 'search_form': search_form}
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
    context = {}
    articles_qs = Article.objects.filter(version=request.session.get('content_version', None))
    context['list_articles'] = [item.content.filter(language=kwargs['lang']) for item in articles_qs]
    context['list_section'] = Section.objects.all()
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(html.encode('UTF-8'), result, encodind='UTF-8', link_callback=fetch_pdf_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def change_version(request, **kwargs):
    if kwargs['version'] == 'None':
        del request.session['content_version']
    else:
        request.session['content_version'] = kwargs['version']
    return HttpResponseRedirect('/docs/')
