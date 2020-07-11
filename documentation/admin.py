from django.contrib import admin
from .models import Article, ArticlesContent, Section


@admin.register(ArticlesContent)
class ArticlesContentAdmin(admin.ModelAdmin):
    list_display = ('article', 'title', 'language')
    list_filter = ('article','language')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('address', 'section', 'priority', 'version')
    list_filter = ('address', 'section', 'priority', 'version')


class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('section', 'priority')
    list_filter = ('section', 'priority')
    inlines = [ArticleInline]
