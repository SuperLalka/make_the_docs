from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


LANG_STATUS = (
        ('ru', 'russian'),
        ('en', 'english'),
    )


class Article(models.Model):
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.SmallIntegerField(default=0, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    version = models.SmallIntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse('documentation:article_page', args=[self.address])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.version is not None:
            if self.version not in [item.version for item in Article.objects.filter(address=self.address)]:
                Article_latest = Article.objects.create(section=self.section, priority=self.priority, address=self.address)
                for item in self.content.all():
                    ArticlesContent.objects.create(article=Article_latest, title=item.title, body=item.body, language=item.language)
        return super(Article, self).save()

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')


class ArticlesContent(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='content', null=True, blank=True)
    title = models.CharField(max_length=100, help_text="Enter a titles article")
    body = HTMLField(help_text="Enter a text article")
    language = models.CharField(max_length=2, choices=LANG_STATUS, default='en', help_text='check language')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('documentation:article_abs_page', args=[self.article, self.language])

    class Meta:
        verbose_name = _('Articles Content')
        verbose_name_plural = _('Articles Contents')


class Section(models.Model):
    title = models.CharField(max_length=30, help_text="Enter a sections of articles")
    priority = models.SmallIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')


class SectionContent(models.Model):
    section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='content', null=True, blank=True)
    title = models.CharField(max_length=100, help_text="Enter a section name")
    language = models.CharField(max_length=2, choices=LANG_STATUS, default='en', help_text='check language')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Section Content')
        verbose_name_plural = _('Sections Contents')
