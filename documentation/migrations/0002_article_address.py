# Generated by Django 3.0.6 on 2020-06-18 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='address',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
