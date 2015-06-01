# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20150528_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='is_email_sent',
            field=models.BooleanField(default=False),
        ),
    ]
