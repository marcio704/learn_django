# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20150522_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpage',
            name='text',
            field=models.CharField(default='Empty', max_length=8000),
            preserve_default=False,
        ),
    ]
