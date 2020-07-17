from django.contrib import admin
from .models import Article, ArticlesContent, Section, SectionContent


class ArticlesContentInline(admin.TabularInline):
    model = ArticlesContent
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('address', 'section', 'priority', 'version')
    list_filter = ('address', 'section', 'priority', 'version')
    inlines = [ArticlesContentInline]


class SectionContentInline(admin.TabularInline):
    model = SectionContent
    extra = 0


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority')
    list_filter = ('title', 'priority')
    inlines = [SectionContentInline]
