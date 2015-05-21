# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_author_personal_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=8000)),
                ('date', models.DateTimeField(verbose_name=b'date published')),
                ('author', models.ForeignKey(blank=True, to='blog.Author', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField(verbose_name=b'date creation')),
                ('blocked', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(verbose_name=b'date login')),
            ],
        ),
    ]
