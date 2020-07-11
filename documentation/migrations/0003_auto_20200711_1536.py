# Generated by Django 3.0.6 on 2020-07-11 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0002_auto_20200710_2025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlescontent',
            options={'verbose_name': 'Articles Content', 'verbose_name_plural': 'Articles Contents'},
        ),
        migrations.AlterField(
            model_name='article',
            name='version',
            field=models.SmallIntegerField(blank=True, default=None, null=True),
        ),
    ]
