# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('text', models.CharField(max_length=8000)),
                ('resume', models.CharField(max_length=200)),
                ('thumbnail', models.ImageField(upload_to='posts')),
                ('category', models.ForeignKey(to='blog.Category')),
            ],
        ),
    ]
