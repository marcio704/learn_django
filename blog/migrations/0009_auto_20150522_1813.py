# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20150521_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=25)),
                ('message', models.CharField(max_length=8000)),
                ('creation_date', models.DateTimeField(verbose_name=b'date creation')),
            ],
        ),
        migrations.CreateModel(
            name='ContactPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(max_length=100)),
                ('last_change', models.DateTimeField(verbose_name=b'date change')),
            ],
        ),
        migrations.RenameModel(
            old_name='About',
            new_name='AboutPage',
        ),
    ]
