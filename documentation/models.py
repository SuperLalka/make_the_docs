from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100, help_text="Enter a titles article")
    body = models.TextField(help_text="Enter a text article")

    def __str__(self):
        return self.title

