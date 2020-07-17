from .forms import ErrorForm, SearchForm
from .models import Article, Section
from make_the_docs import settings


def request(request):

    def add_list_lang(queryset):
        for qs in queryset:
            qs.lang_list = [item.language for item in qs.content.all()]
        return queryset

    list_articles = add_list_lang(Article.objects.filter(version=request.session.get('content_version', None)))
    list_section = add_list_lang(Section.objects.all())
    err_form, search_form = ErrorForm(), SearchForm()
    version_list = set([item.version for item in Article.objects.all()])
    return {
        'list_articles': list_articles,
        'err_form': err_form,
        'search_form': search_form,
        'list_section': list_section,
        'version_list': version_list,
        'settings': settings,
    }
