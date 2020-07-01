from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Article, Section



@admin.register(Article)
class ArticleAdmin(VersionAdmin, admin.ModelAdmin):
    list_display = ('title', 'section', 'priority')
    list_filter = ('section', 'priority')
    exclude = ['address']
    

class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('section', 'priority')
    list_filter = ('section', 'priority')
    inlines = [ArticleInline]

