from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.views import generic

from .forms import ErrorForm, SearchForm
from .models import Article, Section
from .utils import add_anchor, get_anchor_list, render_to_pdf


def index(request):
    list_articles = Article.objects.order_by("-priority")
    article = Article.objects.order_by("id").first()
    list_section = Section.objects.all()
    err_form, search_form = ErrorForm(), SearchForm()
    return render(
        request,
        'index.html',
        context={'list_articles': list_articles,
                 'article': article,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_articles'] = Article.objects.order_by("-priority")
        context['list_section'] = Section.objects.all()
        context['anchor_list'] = get_anchor_list(self.object.body)
        context['err_form'] = ErrorForm()
        context['search_form'] = SearchForm()
        self.object.body = add_anchor(self.object.body)
        return super().get_context_data(**context)


def article_404(request):
    list_articles = Article.objects.order_by("-priority")
    list_section = Section.objects.all()
    return render(
        request,
        'article_404.html',
        context={'list_articles': list_articles,
        'list_section': list_section}
    )


def article_search(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        key = form.cleaned_data.get("search_key")
        results_title = Article.objects.filter(title__icontains=key)
        results_body = Article.objects.filter(body__icontains=key)
        list_articles = Article.objects.order_by("-priority")
        list_section = Section.objects.all()
        err_form, search_form = ErrorForm(), SearchForm()
    else:
        return HttpResponseRedirect(request)
    return render(
        request,
        'search_results.html',
        context={'results_title': results_title,
                 'results_body': results_body,
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


class GeneratePDF(generic.View):
    def get(self, request, *args, **kwargs):
        article = Article.objects.get(address=kwargs['slug'])
        context = {
            "article": article,
        }
        pdf = render_to_pdf('pdf_maker_template.html', context)
        return pdf
