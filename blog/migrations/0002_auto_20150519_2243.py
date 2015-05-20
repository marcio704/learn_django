# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='authors',
            field=models.ManyToManyField(to='blog.Author'),
        ),
    ]
