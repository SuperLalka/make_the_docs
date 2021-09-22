# Generated by Django 3.0.6 on 2020-07-16 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-priority'], 'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
        migrations.AlterModelOptions(
            name='articlescontent',
            options={'ordering': ['-article__priority'], 'verbose_name': 'ArticlesContent', 'verbose_name_plural': 'ArticlesContents'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['-priority'], 'verbose_name': 'Section', 'verbose_name_plural': 'Sections'},
        ),
        migrations.AlterModelOptions(
            name='sectioncontent',
            options={'ordering': ['-section__priority'], 'verbose_name': 'SectionContent', 'verbose_name_plural': 'SectionsContents'},
        ),
    ]