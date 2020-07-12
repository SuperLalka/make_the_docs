from django.contrib import admin
from .models import Article, ArticlesContent, Section, SectionContent


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('address', 'section', 'priority', 'version')
    list_filter = ('address', 'section', 'priority', 'version')


class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0


@admin.register(ArticlesContent)
class ArticlesContentAdmin(admin.ModelAdmin):
    list_display = ('article', 'title', 'language')
    list_filter = ('article','language')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority')
    list_filter = ('title', 'priority')
    inlines = [ArticleInline]


@admin.register(SectionContent)
class ArticlesContentAdmin(admin.ModelAdmin):
    list_display = ('section', 'name', 'language')
    list_filter = ('section','language')