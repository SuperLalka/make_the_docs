# Generated by Django 3.0.6 on 2020-06-18 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0002_article_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='priority',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='priority',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
