# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_post_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='url',
            field=models.CharField(max_length=200),
        ),
    ]
