# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_contactpage_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='title',
        ),
    ]
