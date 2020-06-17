from django.contrib import admin
from .models import Article, Section


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'section')
    list_filter = ('title', 'section')


class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]
