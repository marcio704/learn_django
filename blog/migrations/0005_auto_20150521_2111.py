# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, to='blog.Post', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'users', blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, to='blog.User', null=True),
        ),
    ]
