from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=100, help_text="Enter a titles article")
    body = models.TextField(help_text="Enter a text article")
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
    #def get_absolute_url(self):
        #return reverse('article', args=[str(self.id)])


class Section(models.Model):
    section = models.CharField(max_length=30, help_text="Enter a sections of articles")

    def __str__(self):
        return self.section
