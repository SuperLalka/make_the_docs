from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from .utils import transliterate

class ArticlesContent(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='content', null=True, blank=True)
    title = models.CharField(max_length=100, help_text="Enter a titles article")
    body = HTMLField(help_text="Enter a text article")

    LANG_STATUS = (
        ('ru', 'russian'),
        ('en', 'english'),
    )

    language = models.CharField(max_length=2, choices=LANG_STATUS, default='ru', help_text='check language')

    def __str__(self):
        return self.title
    
class Article(models.Model):
    
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.SmallIntegerField(default=0, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

class Section(models.Model):
    section = models.CharField(max_length=30, help_text="Enter a sections of articles")
    priority = models.SmallIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.section

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')
