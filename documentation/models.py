from django.db import models
from tinymce.models import HTMLField
from .utils import transliterate


class Article(models.Model):
    title = models.CharField(max_length=100, help_text="Enter a titles article")
    body = HTMLField(help_text="Enter a text article")
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True)
    priority = models.IntegerField(default=0, null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id is None:
            self.address = transliterate(self.title)
        return super().save(*args, **kwargs)


class Section(models.Model):
    section = models.CharField(max_length=30, help_text="Enter a sections of articles")
    priority = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.section
