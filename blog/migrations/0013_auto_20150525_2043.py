# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20150525_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='answer_to',
            field=models.ForeignKey(to='blog.Comment', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='aboutpage',
            name='last_change',
            field=models.DateTimeField(verbose_name='date change'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(verbose_name='date creation'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='creation_date',
            field=models.DateTimeField(verbose_name='date creation'),
        ),
        migrations.AlterField(
            model_name='contactpage',
            name='last_change',
            field=models.DateTimeField(verbose_name='date change'),
        ),
        migrations.AlterField(
            model_name='user',
            name='creation_date',
            field=models.DateTimeField(verbose_name='date creation'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(verbose_name='date login'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='users'),
        ),
    ]
