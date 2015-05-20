# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150519_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='personal_page',
            field=models.CharField(null=True, blank=True, max_length=2000),
        ),
    ]
